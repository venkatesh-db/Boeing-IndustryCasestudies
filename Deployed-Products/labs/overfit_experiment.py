"""Was the banking v2 fix an overfit? Score 4 retrieval set-ups on the ORIGINAL failing question (dev)
and on 8 NEW questions the eval never saw (held-out). Uses Eval-Guardrails/banking_lab. Run: python overfit_experiment.py"""
import json, sys
from pathlib import Path
LAB = Path(__file__).resolve().parents[2] / "Eval-Guardrails" / "banking_lab"
sys.path.insert(0, str(LAB))
import os; os.chdir(LAB)
import assistant as a

DEV = [("How much is the fee for paying by card abroad?", ["2.5"])]
HELD_OUT = [
    ("What do you charge if I use my card overseas?", ["2.5"]),
    ("Is there a fee when I pay in another country?", ["2.5"]),
    ("I'm travelling in Europe, will card payments cost extra?", ["2.5"]),
    ("My card is gone, how do I stop people using it?", ["freeze"]),
    ("How many days do I have to challenge a payment?", ["120"]),
    ("Do you charge for a new card if mine breaks?", ["10", "free"]),
    ("What if I type my PIN wrong three times?", ["block"]),
    ("Is there a monthly charge on my account?", ["4.00", "1,000"]),
]
orig = a.retrieve
SETUPS = {
    "v1: keyword, 3 lines": ("keyword", 3, False),
    "v1 + synonym hack (abroad → foreign)": ("keyword", 3, True),
    "hybrid, 3 lines": ("hybrid", 3, False),
    "v2: hybrid, 4 lines": ("hybrid", 4, False),
}
results = {}
for name, (mode, k, hack) in SETUPS.items():
    a.RETRIEVAL = mode
    a.retrieve = (lambda q, _k=k, _h=hack: orig(q.replace("abroad", "abroad foreign") if _h else q, _k))
    rows = []
    for split, cases in (("dev", DEV), ("held_out", HELD_OUT)):
        for q, must in cases:
            r = a.handle(q)
            ok = r["answered"] and any(m.lower() in r["answer"].lower() for m in must)
            rows.append({"split": split, "q": q, "pass": ok, "answer": r["answer"], "ms": r["latency_ms"]})
            print(f"{name:38s} {split:8s} {'PASS' if ok else 'FAIL'}  {q}")
    d = [x for x in rows if x["split"] == "dev"]; h = [x for x in rows if x["split"] == "held_out"]
    results[name] = {"dev": f"{sum(x['pass'] for x in d)}/{len(d)}", "held_out": f"{sum(x['pass'] for x in h)}/{len(h)}", "rows": rows}
    print(f"--> {name}: dev {results[name]['dev']}  held-out {results[name]['held_out']}\n")
a.retrieve = orig
json.dump(results, open(Path(__file__).parent / "overfit_results.json", "w"), indent=1)
