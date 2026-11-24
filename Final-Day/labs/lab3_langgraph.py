"""Lab 3 - LangGraph: state, conditional routing, persistence, human-in-the-loop, multi-agent."""
import sqlite3
import operator
from typing import Annotated, TypedDict

from _common import ROOT, save
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from agentkit import guardrails, llm, tools

out: dict = {}


# snippet:graph
class State(TypedDict, total=False):
    tail: str
    status: dict
    stock: dict
    order: dict
    decision: str
    path: Annotated[list[str], operator.add]     # every node appends; LangGraph merges the lists


def look_up(s: State) -> State:
    return {"status": tools.execute("get_aircraft_status", {"tail_number": s["tail"]}), "path": ["look_up"]}


def check_stock(s: State) -> State:
    args = {"part_number": s["status"]["part_needed"], "station": s["status"]["station"]}
    return {"stock": tools.execute("check_part_stock", args), "path": ["check_stock"]}


def no_action(s: State) -> State:
    return {"decision": "no defect: nothing to do", "path": ["no_action"]}


def escalate(s: State) -> State:
    return {"decision": f"not in stock, lead time {s['stock']['lead_days']} days: call the planner", "path": ["escalate"]}


def approval(s: State) -> State:
    order = {"part_number": s["stock"]["part_number"], "station": s["stock"]["station"], "quantity": 1}
    answer = interrupt({"please_approve": order})                 # the graph stops here and saves itself
    if answer.get("approve") and answer.get("role") == "supervisor":
        done = tools.execute("reserve_part", order, role="supervisor", approved=True)
        return {"order": done, "decision": "reserved", "path": ["approval: yes"]}
    return {"decision": "rejected", "path": ["approval: no"]}


def after_look_up(s: State) -> str:
    return "check_stock" if s["status"]["part_needed"] else "no_action"


def after_stock(s: State) -> str:
    return "approval" if s["stock"]["quantity"] > 0 else "escalate"


def build(checkpointer):
    g = StateGraph(State)
    for node in (look_up, check_stock, no_action, escalate, approval):
        g.add_node(node.__name__, node)
    g.add_edge(START, "look_up")
    g.add_conditional_edges("look_up", after_look_up, ["check_stock", "no_action"])
    g.add_conditional_edges("check_stock", after_stock, ["approval", "escalate"])
    for node in ("no_action", "escalate", "approval"):
        g.add_edge(node, END)
    return g.compile(checkpointer=checkpointer)
# end:graph


DB = ROOT / "results" / "checkpoints.sqlite"
DB.unlink(missing_ok=True)


def open_graph():
    conn = sqlite3.connect(DB, check_same_thread=False)
    return build(SqliteSaver(conn)), conn


graph, conn = open_graph()
out["mermaid"] = graph.get_graph().draw_mermaid()

# 1. Conditional routing: three aircraft, three different paths
out["routes"] = []
for tail in ("N789EF", "N123AB", "N456CD"):
    cfg = {"configurable": {"thread_id": f"t-{tail}"}}
    r = graph.invoke({"tail": tail, "path": []}, cfg)
    paused = graph.get_state(cfg).next
    out["routes"].append({"tail": tail, "path": r["path"], "decision": r.get("decision"), "paused_at": list(paused),
                          "asking": [i.value for i in r.get("__interrupt__", [])]})

# 2. Persistence: close everything, open a brand new graph from disk, and resume the paused run
conn.close()
del graph
graph2, conn2 = open_graph()
cfg = {"configurable": {"thread_id": "t-N456CD"}}
saved = graph2.get_state(cfg)
out["after_restart"] = {"still_paused_at": list(saved.next), "remembered": saved.values}
r = graph2.invoke(Command(resume={"approve": True, "role": "supervisor"}), cfg)
out["resumed"] = {"path": r["path"], "decision": r["decision"], "order": r["order"]}
out["history"] = [{"step": h.metadata.get("step"), "next": list(h.next)} for h in graph2.get_state_history(cfg)][::-1]
conn2.close()


# 3. Multi-agent: a supervisor in code sends work to two specialists, then a writer combines it
class Team(TypedDict, total=False):
    tail: str
    minutes: int
    facts: Annotated[dict, operator.or_]
    log: Annotated[list[str], operator.add]
    summary: str
    checks: list[str]


def supervisor(s: Team) -> Team:
    return {"log": [f"supervisor: have {sorted(s.get('facts', {})) or 'nothing'}"]}


def route(s: Team) -> str:
    facts = s.get("facts", {})
    return "parts_agent" if "parts" not in facts else "cost_agent" if "cost" not in facts else "writer"


def parts_agent(s: Team) -> Team:
    status = tools.execute("get_aircraft_status", {"tail_number": s["tail"]})
    stock = tools.execute("check_part_stock", {"part_number": status["part_needed"], "station": status["station"]})
    return {"facts": {"parts": {**status, **stock}}, "log": ["parts_agent: 2 tools"]}


def cost_agent(s: Team) -> Team:
    return {"facts": {"cost": tools.execute("estimate_delay_cost", {"minutes": s["minutes"]})}, "log": ["cost_agent: 1 tool"]}


def writer(s: Team) -> Team:
    reply = llm.complete([{"role": "system", "content": "Write two short sentences for the duty manager using ONLY these facts. "
                           "Do not add numbers. Do not say if the aircraft may fly."}, {"role": "user", "content": str(s["facts"])}])
    return {"summary": reply.text.strip(), "checks": guardrails.check_output(reply.text, "", [s["facts"]]), "log": ["writer: 1 model call"]}


team = StateGraph(Team)
for node in (supervisor, parts_agent, cost_agent, writer):
    team.add_node(node.__name__, node)
team.add_edge(START, "supervisor")
team.add_conditional_edges("supervisor", route, ["parts_agent", "cost_agent", "writer"])
team.add_edge("parts_agent", "supervisor")
team.add_edge("cost_agent", "supervisor")
team.add_edge("writer", END)
t = team.compile().invoke({"tail": "N123AB", "minutes": 45, "facts": {}, "log": []})
out["team"] = {k: t[k] for k in ("log", "facts", "summary", "checks")}

for r in out["routes"]: print(r)
print(out["after_restart"]["still_paused_at"], out["resumed"]); print(out["team"]["log"], out["team"]["summary"], out["team"]["checks"])
save("lab3", out)
