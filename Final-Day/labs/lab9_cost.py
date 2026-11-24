"""Lab 9 - Cost: routing, caching, batching, token trimming. Tokens and times are measured here; prices come from vendors' pages."""
import json
import re
import time

from _common import ROOT, save
from agentkit import llm, tools
from agentkit.agent import V1, V3, run_agent
from agentkit.pricing import SHEET, cost

out: dict = {}
Q = "How many HP-2201 are at FRA?"


def ask(system: str, question: str, cache=False):
    return llm.complete([{"role": "system", "content": system}, {"role": "user", "content": question}], json_mode=True, use_cache=cache)


# 1. Token trimming: the same four tools described three ways
JSON_RULE = '\nPick one tool. Reply with JSON only: {"tool": "<name>", "arguments": {"<name>": "<value>"}}'
full = json.dumps([tools.openai_schema(t) for t in tools.TOOLS.values()])
one = "\n".join(l for l in tools.menu().splitlines() if "check_part_stock" in l)
out["trim"] = []
for label, text in [("full JSON schemas, 4 tools", full), ("short menu, 4 tools", tools.menu()), ("short menu, only the relevant tool", one)]:
    r = ask(text + JSON_RULE, Q)
    try:
        call = llm.parse_json(r.text)
        good = call.get("tool") == "check_part_stock" and call.get("arguments") == {"part_number": "HP-2201", "station": "FRA"}
    except ValueError:
        good = False
    out["trim"].append({"label": label, "tokens_in": r.tokens_in, "tokens_out": r.tokens_out, "ms": r.ms, "correct": good})

# 2. Caching: exact same question twice
a, b = ask(tools.menu() + JSON_RULE, Q, cache=True), None
start = time.perf_counter(); b = ask(tools.menu() + JSON_RULE, Q, cache=True)
out["cache"] = {"first_ms": a.ms, "second_ms": round((time.perf_counter() - start) * 1000, 2), "second_cached": b.cached}

# 3. Batching: label five notes one by one, or all in one request
NOTES = [("Coffee maker in forward galley leaks", "cabin"), ("Hydraulic pump pressure low on system A", "hydraulic"),
         ("Brake wear pin flush on wheel 3", "brake"), ("Seat 14C will not recline", "cabin"), ("Hydraulic fluid drip at actuator", "hydraulic")]
RULE = "Label the defect note as exactly one of: cabin, hydraulic, brake. "
single, t0 = [], time.perf_counter()
for note, _ in NOTES:
    single.append(ask(RULE + 'JSON only: {"label": "<label>"}', note))
t_single = time.perf_counter() - t0
t0 = time.perf_counter()
multi = ask("Label each numbered defect note as exactly one of: cabin, hydraulic, brake. "
            'JSON only: {"1": "<label>", "2": "<label>", ...}', "\n".join(f"{i}. {n}" for i, (n, _) in enumerate(NOTES, 1)))
t_multi = time.perf_counter() - t0


def label(text, key):
    try:
        return str(llm.parse_json(text).get(key, "")).lower()
    except ValueError:
        return ""


out["batch"] = {"single": {"calls": 5, "tokens_in": sum(r.tokens_in for r in single), "tokens_out": sum(r.tokens_out for r in single),
                           "s": round(t_single, 2), "correct": sum(label(r.text, "label") == w for r, (_, w) in zip(single, NOTES))},
                "together": {"calls": 1, "tokens_in": multi.tokens_in, "tokens_out": multi.tokens_out, "s": round(t_multi, 2),
                             "correct": sum(label(multi.text, str(i)) == w for i, (_, w) in enumerate(NOTES, 1))}}


# 4. Routing: simple questions answered by code, everything else by the agent
def route(q: str):
    m = re.fullmatch(r"(?:what does |cost of )?a? ?(\d+) minutes? delay(?: cost)?\??", q.strip().lower())
    return tools.execute("estimate_delay_cost", {"minutes": int(m.group(1))}) if m else None


out["route"] = []
for q in ["What does a 45 minute delay cost?", "Cost of a 30 minute delay?", "How many HP-2201 are at FRA?", "Is N123AB airworthy?"]:
    t0 = time.perf_counter()
    fast = route(q)
    if fast:
        out["route"].append({"q": q, "path": "code rule", "tokens": 0, "s": round(time.perf_counter() - t0, 4), "answer": f"${fast['total_usd']:,}"})
    else:
        r = run_agent(q)
        out["route"].append({"q": q, "path": "guard (no model)" if r.llm_calls == 0 else "agent", "tokens": r.tokens_in + r.tokens_out,
                             "s": round(time.perf_counter() - t0, 2), "answer": r.answer})

# 5. Cost per SUCCESSFUL task, from the recorded evals
out["versions"] = []
for v in ("v1", "v2", "v3"):
    e = json.loads((ROOT / "results" / f"eval_{v}.json").read_text())
    rows = e["dev"]["rows"] + e["held-out"]["rows"]          # the same 22 cases for every version
    out["versions"].append({"version": v, "passed": sum(r["pass"] for r in rows), "total": len(rows),
                            "tokens_in": sum(r["tokens_in"] for r in rows), "tokens_out": sum(r["tokens_out"] for r in rows),
                            "llm_calls": sum(r["llm_calls"] for r in rows), "dev": e["dev"]["passed"], "held": e["held-out"]["passed"]})
v3 = out["versions"][2]
out["per_task"] = {"tokens_in": round(v3["tokens_in"] / v3["total"]), "tokens_out": round(v3["tokens_out"] / v3["total"])}
out["sheet"] = []
for row in SHEET["rows"]:
    c = cost(row, out["per_task"]["tokens_in"], out["per_task"]["tokens_out"])
    out["sheet"].append({"vendor": row["vendor"], "model": row["model"], "usd_per_1000_tasks": round(c * 1000, 4)})
print(json.dumps({k: out[k] for k in ("trim", "cache", "batch", "route", "versions", "per_task")}, indent=1))
for s in out["sheet"]: print(s)
save("lab9", out)
