"""A small agent: decide -> act -> look at the result -> repeat, with hard stops."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from typing import Callable, Literal

from pydantic import BaseModel, Field, ValidationError

from agentkit import guardrails, llm, tools
from agentkit.tracing import span

MAX_STEPS = 5
TOKEN_BUDGET = 6000

SYSTEM_V1 = """You are a parts-desk assistant. Work one step at a time.
Tools:
{menu}

Reply with ONE JSON object and nothing else.
To use a tool: {{"action": "tool", "tool": "check_part_stock", "arguments": {{"part_number": "HP-2201", "station": "BLR"}}}}
To answer:     {{"action": "final", "answer": "one or two plain sentences"}}
Rules: use only numbers returned by tools. Never call the same tool with the same arguments twice.
When the results already answer the question, choose "final"."""


SYSTEM_V2 = """You are a parts-desk assistant. Work one step at a time.
Tools:
{menu}
- final_answer(answer: one or two plain sentences) -> Finish.

Reply with ONE JSON object in exactly this shape:
{{"tool": "<tool name>", "arguments": {{"<name>": <value>}}}}

Rules:
1. Take every argument from the question or from an earlier result. Never guess one.
2. If you know a tail number but not its station or part, call get_aircraft_status first.
3. Call only the tools the question needs: no stock check unless it asks about stock, no cost unless it gives a delay.
4. As soon as the results answer the question, call final_answer. Use only numbers from the results.
5. If a tool returns an error, do not try another tool. Call final_answer and say what was not found.
6. If no tool fits the question, call final_answer and say you can only help with parts, defects and delays."""


@dataclass(frozen=True)
class Config:
    name: str
    system: str
    check_args: bool = False       # arguments must come from the question or a tool result
    need_evidence: bool = False    # no answer about a part or aircraft before a tool was used
    warn_on_repeat: bool = False   # one warning before stopping on a repeated call
    guard_level: int = 1           # 2 = with the fixes from incidents H07 and H11


V1 = Config("v1", SYSTEM_V1)
V2 = Config("v2", SYSTEM_V2, check_args=True, need_evidence=True, warn_on_repeat=True)
V3 = replace(V2, name="v3", guard_level=2)


# snippet:decision
class Decision(BaseModel):
    action: Literal["tool", "final"]
    tool: str | None = None
    arguments: dict = Field(default_factory=dict)
    answer: str | None = None


def read_decision(data: dict) -> Decision:
    """v2 replies are flat: final_answer is just another tool name."""
    if "action" in data:
        return Decision.model_validate(data)
    if data.get("tool") == "final_answer":
        return Decision(action="final", answer=str((data.get("arguments") or {}).get("answer") or ""))
    return Decision.model_validate({"action": "tool", "tool": data.get("tool"), "arguments": data.get("arguments") or {}})
# end:decision


@dataclass
class Run:
    question: str
    role: str
    events: list[dict] = field(default_factory=list)
    results: list[dict] = field(default_factory=list)
    answer: str = ""
    stopped: str = ""
    pending: dict | None = None
    tokens_in: int = 0
    tokens_out: int = 0
    llm_calls: int = 0

    def log(self, kind: str, **data) -> None:
        self.events.append({"kind": kind, **data})


def ask_model(run: Run, messages: list[dict]) -> Decision:
    """One decision. If the JSON is wrong, show the model its error once."""
    convo = list(messages)
    for attempt in range(2):
        reply = llm.complete(convo, json_mode=True)
        run.tokens_in, run.tokens_out, run.llm_calls = run.tokens_in + reply.tokens_in, run.tokens_out + reply.tokens_out, run.llm_calls + 1
        try:
            decision = read_decision(llm.parse_json(reply.text))
            if (decision.action == "tool" and not decision.tool) or (decision.action == "final" and not decision.answer):
                raise ValueError("a tool call needs 'tool'; a final reply needs 'answer'")
            return decision
        except (ValidationError, ValueError) as err:
            run.log("invalid_json", attempt=attempt + 1, error=str(err).splitlines()[0], raw=reply.text[:200])
            convo += [{"role": "assistant", "content": reply.text},
                      {"role": "user", "content": f"Invalid: {err}. Send corrected JSON only."}]
    raise ValueError("the model did not return a valid decision")


# snippet:loop
def run_agent(question: str, role: str = "planner", safe_mode: bool = False,
              decide: Callable[[Run, list[dict]], Decision] = ask_model, config: Config = V3) -> Run:
    run = Run(guardrails.redact(question), role)
    with span("agent", question=run.question, role=role, safe_mode=safe_mode, config=config.name) as s:
        _loop(run, safe_mode, decide, config)
        s["stopped"], s["steps"] = run.stopped, len(run.results)
    return run


def _loop(run: Run, safe_mode: bool, decide: Callable, config: Config) -> None:
    blocked = guardrails.check_input(run.question, config.guard_level)
    if blocked:                                                   # STOP 1: input guard, no model call
        run.answer, run.stopped = guardrails.REPLIES[blocked], f"input guard: {blocked}"
        return
    messages = [{"role": "system", "content": config.system.format(menu=tools.menu())},
                {"role": "user", "content": run.question}]
    seen: set[str] = set()
    for _ in range(MAX_STEPS):                                    # STOP 2: step limit
        if run.tokens_in + run.tokens_out > TOKEN_BUDGET:         # STOP 3: token budget
            run.stopped = "token budget"
            break
        try:
            decision = decide(run, messages)
        except ValueError as err:                                 # STOP 4: unusable model output
            run.stopped = f"bad model output: {err}"
            break
        if decision.action == "final":                            # STOP 5: the normal ending
            if config.need_evidence and _lacks_evidence(run):
                run.log("no_evidence", draft=decision.answer)
                messages += _feedback(decision, "Rejected: use a tool first. The question names a part, aircraft or delay.")
                continue
            _finish(run, decision.answer or "", config.guard_level)
            return
        signature = json.dumps([decision.tool, decision.arguments], sort_keys=True)
        if signature in seen:                                     # STOP 6: going in circles (one warning in v2)
            run.log("repeat", tool=decision.tool, arguments=decision.arguments)
            if config.warn_on_repeat and sum(e["kind"] == "repeat" for e in run.events) == 1:
                messages += _feedback(decision, "Rejected: you already have this result. Call final_answer now.")
                continue
            run.stopped = "repeated the same call"
            break
        seen.add(signature)
        run.log("decide", tool=decision.tool, arguments=decision.arguments)
        invented = guardrails.ungrounded_args(decision.arguments, run.question, run.results, config.guard_level) if config.check_args else []
        if invented:
            run.log("args_blocked", tool=decision.tool, invented=invented)
            messages += _feedback(decision, f"Rejected: {invented} is not in the question or in any result. Do not guess.")
            continue
        tool = tools.TOOLS.get(decision.tool or "")
        if tool and tool.writes:                                  # STOP 7: a human (or safe mode) decides
            _handle_write(run, tool, decision.arguments, safe_mode)
            return
        observation = _act(run, decision)
        messages += _feedback(decision, f"Result: {json.dumps(observation)}", config.name)
    else:
        run.stopped = "step limit"
    run.answer = run.answer or "I stopped before I had a verified answer. Please check with the parts desk."
# end:loop


def _feedback(decision: Decision, text: str, version: str = "v2") -> list[dict]:
    """What the model sees after each step: its own move, then what happened."""
    if version == "v1":
        move = decision.model_dump_json()
    elif decision.action == "final":
        move = json.dumps({"tool": "final_answer", "arguments": {"answer": decision.answer}})
    else:
        move = json.dumps({"tool": decision.tool, "arguments": decision.arguments})
    return [{"role": "assistant", "content": move}, {"role": "user", "content": text}]


def _lacks_evidence(run: Run) -> bool:
    used_a_tool = any(e["kind"] in ("result", "tool_error") for e in run.events)
    return guardrails.names_an_item(run.question) and not used_a_tool


def _act(run: Run, decision: Decision) -> dict:
    try:
        result = tools.execute(decision.tool or "", decision.arguments, run.role)
        run.results.append(result)
        run.log("result", tool=decision.tool, result=result)
        return result
    except (PermissionError, LookupError, ValueError) as err:     # pydantic errors are ValueErrors
        message = "; ".join(e["msg"] for e in err.errors()) if isinstance(err, ValidationError) else str(err)
        run.log("tool_error", tool=decision.tool, error=message)
        return {"error": message}


def _handle_write(run: Run, tool: tools.Tool, arguments: dict, safe_mode: bool) -> None:
    try:
        args = tool.args.model_validate(arguments).model_dump()
    except ValidationError as err:
        run.log("tool_error", tool=tool.name, error="; ".join(e["msg"] for e in err.errors()))
        run.stopped, run.answer = "invalid write request", "The reservation request was not valid, so nothing was changed."
        return
    if safe_mode:
        run.log("safe_mode", tool=tool.name, arguments=args)
        run.stopped, run.answer = "safe mode", "Safe mode is on: I can read and report, but I changed nothing."
        return
    run.pending = {"tool": tool.name, "arguments": args}
    run.log("approval_needed", **run.pending)
    run.stopped, run.answer = "waiting for approval", "This changes stock, so a supervisor must approve it first."


def _finish(run: Run, answer: str, guard_level: int = 2) -> None:
    problems = guardrails.check_output(answer, run.question, run.results, guard_level)
    if problems:
        run.log("output_blocked", draft=answer, problems=problems)
        run.answer, run.stopped = guardrails.REPLIES["ungrounded"], "output guard"
        return
    run.answer, run.stopped = guardrails.redact(answer), "answered"


def approve(run: Run, approver_role: str) -> dict:
    """Only a supervisor can release a pending write."""
    if not run.pending:
        raise ValueError("nothing is waiting for approval")
    if approver_role != "supervisor":
        raise PermissionError("only a supervisor may approve")
    result = tools.execute(run.pending["tool"], run.pending["arguments"], approver_role, approved=True)
    run.log("approved", by=approver_role, result=result)
    run.pending, run.stopped, run.answer = None, "approved and done", f"Done: {result['status']}."
    return result
