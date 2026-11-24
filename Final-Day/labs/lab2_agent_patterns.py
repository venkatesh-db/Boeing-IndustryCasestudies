"""Lab 2 - Agent patterns: the loop, planner-executor, stop criteria, safe mode."""
from _common import run_dict, save
from pydantic import BaseModel, ValidationError

from agentkit import llm, tools
from agentkit.agent import Decision, V1, V3, approve, run_agent

out: dict = {}
Q = "N123AB has a defect. Which part does it need, and is it in stock at its station?"

# 1. The ReAct-style loop: the first version, then the version with guards
out["loop_v1"] = run_dict(run_agent(Q, config=V1))
out["loop_v3"] = run_dict(run_agent(Q, config=V3))


# 2. Planner-executor: plan everything first, then run the plan without asking the model again
class Plan(BaseModel):
    steps: list[str]


NEEDS = {"get_aircraft_status": 0, "check_part_stock": 1, "estimate_delay_cost": 1}   # what depends on what, in code


def planner_executor(question: str, tail: str, order_in_code: bool) -> dict:
    reply = llm.complete([{"role": "system", "content": "Choose which tools are needed, in order. Tools: "
                           "get_aircraft_status, check_part_stock, estimate_delay_cost. Use as few as possible. "
                           'Reply with JSON only: {"steps": ["<tool>"]}'}, {"role": "user", "content": question}], json_mode=True)
    try:
        plan = [s for s in Plan.model_validate(llm.parse_json(reply.text)).steps if s in tools.TOOLS]
    except (ValidationError, ValueError):
        plan = ["get_aircraft_status"]
    if order_in_code:
        plan = sorted(plan, key=NEEDS.get)
    known, done = {"tail_number": tail}, []
    for step in plan:
        need = tools.TOOLS[step].args.model_fields           # the executor fills arguments from known facts
        known["part_number"] = known.get("part_number") or known.get("part_needed")
        args = {k: known[k] for k in need if known.get(k) is not None}
        try:
            result = tools.execute(step, args)
            known |= result
            done.append({"step": step, "args": args, "result": result})
        except (ValueError, LookupError) as err:
            done.append({"step": step, "args": args, "skipped": str(err).splitlines()[0]})
    return {"raw_plan": reply.text, "plan": plan, "done": done, "llm_calls": 1, "tokens_in": reply.tokens_in, "tokens_out": reply.tokens_out}


out["planner_raw"] = planner_executor(Q, "N123AB", order_in_code=False)
out["planner"] = planner_executor(Q, "N123AB", order_in_code=True)


# 3. Stop criteria, tested with scripted "bad models" so each stop fires every time
def endless(run, messages):      # always asks for something new
    n = len(run.events) + 1
    return Decision(action="tool", tool="estimate_delay_cost", arguments={"minutes": n})


def stubborn(run, messages):     # repeats the same call
    return Decision(action="tool", tool="check_part_stock", arguments={"part_number": "HP-2201", "station": "FRA"})


def greedy(run, messages):       # burns tokens
    run.tokens_in += 4000
    return Decision(action="tool", tool="estimate_delay_cost", arguments={"minutes": len(run.events) + 1})


out["stops"] = []
for label, model, q in [("step limit", endless, "delay 1 2 3 4 5 6 7 8 9 10 11"), ("repeated call", stubborn, "HP-2201 at FRA"),
                        ("token budget", greedy, "delay 1 2 3 4 5 6 7 8 9 10 11")]:
    run = run_agent(q, decide=model)
    out["stops"].append({"label": label, "stopped": run.stopped, "events": run.events, "answer": run.answer})

# 4. Safe mode and approval: same request, three outcomes
W = "Reserve 1 of HP-2201 at FRA"
safe, normal = run_agent(W, safe_mode=True), run_agent(W)
out["safe_mode"], out["approval_wait"] = run_dict(safe), run_dict(normal)
try:
    approve(normal, "planner")
except PermissionError as err:
    out["planner_approves"] = str(err)
approve(normal, "supervisor")
out["supervisor_approves"] = run_dict(normal)

print("v1:", out["loop_v1"]["answer"]); print("v3:", out["loop_v3"]["answer"])
print("plan:", out["planner"]["plan"], [d.get("result", d.get("skipped")) for d in out["planner"]["done"]])
for s in out["stops"]: print(s["label"], "->", s["stopped"])
print(safe.stopped, "|", out["planner_approves"], "|", normal.answer)
save("lab2", out)
