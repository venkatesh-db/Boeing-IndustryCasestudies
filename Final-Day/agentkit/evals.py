"""Grade the whole run: did it call the right tools, with the right arguments, stop the right way, answer correctly?"""
from __future__ import annotations

import json
import re
import statistics
import time
from pathlib import Path
from typing import Callable

from agentkit.agent import Run

CASES = json.loads((Path(__file__).resolve().parents[1] / "data" / "eval_cases.json").read_text())["cases"]


# snippet:grade
def grade(case: dict, run: Run) -> list[str]:
    """Reasons this run fails the case. An empty list means pass."""
    made = [(e["tool"], e["arguments"]) for e in run.events if e["kind"] == "decide"]
    problems = []
    if run.stopped != case["stopped"]:
        problems.append(f"stopped '{run.stopped}', expected '{case['stopped']}'")
    for name, wanted in case["calls"]:
        if not any(t == name and wanted.items() <= a.items() for t, a in made):
            problems.append(f"missing call {name}{wanted}")
    wanted_names = {c[0] for c in case["calls"]}
    extra = [t for t, _ in made if t not in wanted_names] if case["calls"] else []
    if extra:
        problems.append(f"unneeded calls {extra}")
    if case.get("pending") and (run.pending or {}).get("arguments") != case["pending"]:
        problems.append(f"wrong write request {(run.pending or {}).get('arguments')}")
    if case.get("answer") and not re.search(case["answer"], run.answer, re.I):
        problems.append("answer does not contain the expected fact")
    return problems
# end:grade


def evaluate(runner: Callable[[str], Run], split: str) -> dict:
    rows = []
    for case in (c for c in CASES if c["split"] == split):
        start = time.perf_counter()
        run = runner(case["q"])
        problems = grade(case, run)
        rows.append({"id": case["id"], "type": case["type"], "q": case["q"], "pass": not problems, "problems": problems,
                     "stopped": run.stopped, "answer": run.answer, "events": run.events, "llm_calls": run.llm_calls,
                     "tokens_in": run.tokens_in, "tokens_out": run.tokens_out, "s": round(time.perf_counter() - start, 2)})
    passed = sum(r["pass"] for r in rows)
    return {"split": split, "passed": passed, "total": len(rows), "rows": rows,
            "tokens_in": sum(r["tokens_in"] for r in rows), "tokens_out": sum(r["tokens_out"] for r in rows),
            "median_s": round(statistics.median(r["s"] for r in rows), 2)}
