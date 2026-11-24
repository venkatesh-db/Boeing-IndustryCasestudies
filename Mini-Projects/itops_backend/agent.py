"""The real agent: LangGraph controls, LangChain talks to the model, MCP reaches the systems."""
import asyncio
import json
import operator
import os
import re
import sys
import time
from pathlib import Path
from typing import Annotated, Literal, TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from pydantic import BaseModel, Field, ValidationError

HERE = Path(__file__).parent
SERVICES = {"checkout": 1200, "payroll": 300, "email": 2500}
CLEAN = {
    "checkout": {"health": {"errors_percent": 38, "memory_percent": 55, "status": "failing"}, "change": {"release": "4.2", "when": "20 minutes ago", "previous": "4.1"}, "ticket": {"key": "OPS-77", "title": "Checkout returns errors", "reports": 46}},
    "payroll": {"health": {"errors_percent": 2, "memory_percent": 97, "status": "slow"}, "change": {"release": "2.8", "when": "3 weeks ago", "previous": "2.7"}, "ticket": {"key": "OPS-81", "title": "Payroll very slow", "reports": 9}},
    "email": {"health": {"errors_percent": 0, "memory_percent": 40, "status": "healthy"}, "change": {"release": "9.0", "when": "2 months ago", "previous": "8.9"}, "ticket": {"key": "none", "title": "No open ticket", "reports": 0}}}
llm = ChatOpenAI(model="llama3", base_url="http://localhost:11434/v1", api_key="ollama", temperature=0, seed=7)
llm_json = llm.bind(response_format={"type": "json_object"})


class Understood(BaseModel):
    service: Literal["checkout", "payroll", "email", "unknown"]
    intent: Literal["problem", "access", "other"]
    summary: str = Field(min_length=3)


class Proposal(BaseModel):
    action: Literal["roll_back_release", "restart_service", "none"]
    reason: str = Field(min_length=3)


class State(TypedDict, total=False):
    request: str
    understood: dict
    facts: dict
    proposal: dict
    impact: dict
    decision: str
    outcome: str
    report: str
    blocked: list
    tries: int
    events: Annotated[list, operator.add]


@tool
def estimate_impact(service_name: str) -> dict:
    """How many people use a service, and how risky a change is."""
    users = SERVICES[service_name]
    return {"people": users, "risk": "high" if users > 1000 else "medium"}


def event(layer: str, title: str, detail, start: float, ok: bool = True) -> dict:
    return {"layer": layer, "title": title, "detail": detail, "ms": round((time.perf_counter() - start) * 1000), "ok": ok}


async def ask_json(system: str, human: str, schema, **values):
    chain = ChatPromptTemplate.from_messages([("system", system), ("human", human)]) | llm_json | StrOutputParser()
    tries = []
    for _ in range(2):
        text = await chain.ainvoke(values)
        tries.append(text)
        try:
            return schema.model_validate_json(re.search(r"\{.*\}", text, re.S).group(0)), tries
        except (ValidationError, AttributeError):
            continue
    return None, tries


async def understand(s: State):
    t = time.perf_counter()
    out, tries = await ask_json("Read an IT request. Reply with JSON only: service (checkout, payroll, email or unknown), intent (problem = something is "
                                "broken or slow; access = wants permission, a password or a role; other), summary (a few words). Use unknown if no service is named.",
                                "{request}", Understood, request=s["request"])
    u = out.model_dump() if out else {"service": "unknown", "intent": "other", "summary": "not understood"}
    named = [n for n in SERVICES if n in s["request"].lower()]
    if u["service"] == "unknown" and len(named) == 1:   # a fact in the text beats the model's guess
        u["service"] = named[0]
    return {"understood": u, "events": [event("chain", "Understand the request", {"model_wrote": tries[-1], "checked": u}, t, bool(out))]}


def after_understand(s: State):
    u = s["understood"]
    return "refuse" if u["intent"] == "access" else "clarify" if u["service"] == "unknown" else "gather"


async def refuse(s: State):
    t = time.perf_counter()
    return {"outcome": "refused", "events": [event("graph", "Decision: stop", "Access requests are never handled by the agent. A person must do it.", t)]}


async def clarify(s: State):
    t = time.perf_counter()
    return {"outcome": "needs detail", "events": [event("graph", "Decision: ask", "No service was named. Please say checkout, payroll or email.", t)]}


async def call_mcp(config, name: str, service: str):
    t = time.perf_counter()
    try:
        r = await config["configurable"]["tools"][name].ainvoke({"service_name": service})
        text = r[0]["text"] if isinstance(r, list) else r
        try:
            return json.loads(text), t, True
        except ValueError:                       # the adapter returns a tool error as plain text
            return {"error": text.split(": ", 1)[-1][:120]}, t, False
    except Exception as err:
        return {"error": str(err).split(": ", 1)[-1][:120]}, t, False


async def gather(s: State, config):
    svc, facts, ev = s["understood"]["service"], {}, []
    for name, title in [("service_health", "Monitoring"), ("recent_change", "GitHub"), ("open_ticket", "Jira")]:
        facts[name], t, ok = await call_mcp(config, name, svc)
        ev.append(event("mcp", f"Read from {title}", facts[name], t, ok))
    t = time.perf_counter()
    blob = await config["configurable"]["client"].get_resources("ops", uris=["docs://runbook"])
    facts["runbook"] = blob[0].as_string()
    ev.append(event("mcp", "Read from Documents", facts["runbook"], t))
    t = time.perf_counter()
    impact = estimate_impact.invoke({"service_name": svc})
    ev.append(event("tool", "Function: estimate impact", impact, t))
    return {"facts": facts, "impact": impact, "events": ev}


async def propose(s: State):
    t = time.perf_counter()
    out, tries = await ask_json("Choose one action using ONLY the facts and the runbook. Reply with JSON only: action (roll_back_release, restart_service or none), reason (one sentence).",
                                "Facts: {facts}{feedback}", Proposal, facts=json.dumps(s["facts"]),
                                feedback=f"\nAlready rejected, not supported by the evidence: {s['blocked']}. Compare every number with the runbook and choose another." if s.get("blocked") else "")
    p = out.model_dump() if out else {"action": "none", "reason": "no valid proposal"}
    f, safe = s["facts"], p["action"]
    h, c = f["service_health"], f["recent_change"]
    allowed = {"none"}
    if h.get("memory_percent", 0) > 90:
        allowed.add("restart_service")
    if h.get("errors_percent", 0) > 10 and "minutes" in str(c.get("when", "")):
        allowed.add("roll_back_release")
    ev = [event("chain", "The model proposes", {"model_wrote": tries[-1], "checked": p}, t, bool(out))]
    t = time.perf_counter()
    bad = safe not in allowed
    if bad:
        p = {"action": "none", "reason": f"The proposal {safe} is not supported by the evidence, so it was blocked."}
    ev.append(event("graph", "Decision: check the evidence", {"allowed_by_evidence": sorted(allowed), "result": p["action"]}, t, not bad))
    return {"proposal": p, "blocked": s.get("blocked", []) + ([safe] if bad else []), "tries": s.get("tries", 0) + 1, "events": ev}


def after_propose(s: State):
    if s["blocked"] and s["tries"] < 2:
        return "propose"                          # one more try, with the reason
    return "approval" if s["proposal"]["action"] != "none" else "report"


async def approval(s: State):
    answer = interrupt({"action": s["proposal"]["action"], "service": s["understood"]["service"], "reason": s["proposal"]["reason"], "impact": s["impact"]})
    t = time.perf_counter()
    return {"decision": answer, "events": [event("graph", f"Person said: {answer}", "The graph was paused and saved until this answer came.", t)]}


def after_approval(s: State):
    return "act" if s["decision"] == "approve" else "report"


async def act(s: State, config):
    svc, name = s["understood"]["service"], s["proposal"]["action"]
    done, t, ok = await call_mcp(config, name, svc)
    ev = [event("mcp", "Do it: " + name.replace("_", " "), done, t, ok)]
    health, t, ok2 = await call_mcp(config, "service_health", svc)
    good = ok and ok2 and health.get("status") == "healthy"
    ev.append(event("mcp", "Check again with Monitoring", health, t, good))
    return {"outcome": "solved" if good else "not fixed", "events": ev}


async def report(s: State):
    t = time.perf_counter()
    outcome = s.get("outcome") or ("rejected" if s.get("decision") == "reject" else "no change made")
    facts = {"request": s["request"], "facts": {k: v for k, v in s.get("facts", {}).items() if k != "runbook"}, "proposal": s.get("proposal"), "person_decided": s.get("decision", "not needed"), "outcome": outcome}
    chain = ChatPromptTemplate.from_messages([("system", "Write a final incident report in at most 4 short plain sentences: what was asked, what was found, what was decided, the outcome. Use ONLY the data. Never claim a change that did not happen."), ("human", "{data}")]) | llm | StrOutputParser()
    text = (await chain.ainvoke({"data": json.dumps(facts)})).strip()
    return {"outcome": outcome, "report": text, "events": [event("chain", "Write the report", text, t)]}


def build(saver):
    g = StateGraph(State)
    for fn in (understand, refuse, clarify, gather, propose, approval, act, report):
        g.add_node(fn.__name__, fn)
    g.add_edge(START, "understand")
    g.add_conditional_edges("understand", after_understand, ["refuse", "clarify", "gather"])
    g.add_edge("gather", "propose")
    g.add_conditional_edges("propose", after_propose, ["propose", "approval", "report"])
    g.add_conditional_edges("approval", after_approval, ["act", "report"])
    g.add_edge("act", "report")
    for n in ("report", "refuse", "clarify"):
        g.add_edge(n, END)
    return g.compile(checkpointer=saver)


async def run(label: str, request: str, decision: str | None, env: dict) -> dict:
    tmp = HERE / f"_state_{label}.json"
    db = HERE / f"_cp_{label}.sqlite"
    db.unlink(missing_ok=True)
    tmp.write_text(json.dumps(CLEAN))
    client = MultiServerMCPClient({"ops": {"transport": "stdio", "command": sys.executable, "args": [str(HERE / "server.py")], "env": {"PATH": os.environ["PATH"], "ITOPS_STATE": str(tmp), **env}}})
    tools = {t.name: t for t in await client.get_tools()}
    cfg = {"configurable": {"thread_id": label, "tools": tools, "client": client}}
    try:
        async with AsyncSqliteSaver.from_conn_string(str(db)) as saver:
            r = await build(saver).ainvoke({"request": request, "events": []}, cfg)
            ask = [i.value for i in r.get("__interrupt__", [])]
        restored = None
        if ask:                      # everything above is closed: a new graph reads the pause back from disk
            async with AsyncSqliteSaver.from_conn_string(str(db)) as saver:
                g2 = build(saver)
                snap = await g2.aget_state(cfg)
                restored = {"next": list(snap.next), "events_remembered": len(snap.values["events"])}
                r = await g2.ainvoke(Command(resume=decision), cfg)
        return {"label": label, "request": request, "decision": decision, "ask": ask[0] if ask else None, "restored": restored, "understood": r["understood"], "events": r["events"], "outcome": r["outcome"], "report": r.get("report")}
    finally:
        tmp.unlink(missing_ok=True)
        db.unlink(missing_ok=True)


CASES = [("checkout_approve", "Customers get errors in checkout since this morning!", "approve", {}), ("checkout_reject", "Customers get errors in checkout since this morning!", "reject", {}),
         ("checkout_fails", "Customers get errors in checkout since this morning!", "approve", {"REPAIR_FAILS": "1"}), ("checkout_github", "Customers get errors in checkout since this morning!", "approve", {"GITHUB_DOWN": "1"}),
         ("payroll_approve", "Payroll is painfully slow today", "approve", {}), ("payroll_reject", "Payroll is painfully slow today", "reject", {}), ("payroll_fails", "Payroll is painfully slow today", "approve", {"REPAIR_FAILS": "1"}), ("payroll_github", "Payroll is painfully slow today", "approve", {"GITHUB_DOWN": "1"}),
         ("email", "I think email is a bit odd", "approve", {}), ("access", "Please give me admin access to payroll", "approve", {}), ("vague", "Nothing works, please help", "approve", {})]


async def main():
    out = {}
    for c in CASES:
        out[c[0]] = x = await run(*c)
        print(c[0], x["understood"], "|", x["ask"] and x["ask"]["action"], "|", x["outcome"], "|", [e["title"] for e in x["events"] if not e["ok"]], "|", x["report"])
    (HERE / "recorded.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
