"""Lab 8 - Evals: re-run one version on every split.   python labs/lab8_eval.py v3"""
import sys

from _common import save
from agentkit.agent import V1, V2, V3, run_agent
from agentkit.evals import evaluate

version = sys.argv[1] if len(sys.argv) > 1 else "v3"
config = {"v1": V1, "v2": V2, "v3": V3}[version]
splits = ("dev", "held-out", "fresh") if version == "v3" else ("dev", "held-out")
out = {s: evaluate(lambda q: run_agent(q, config=config), s) for s in splits}
for s, r in out.items():
    print(f"{version} {s}: {r['passed']}/{r['total']}  median {r['median_s']} s")
    for x in r["rows"]:
        print("   ", "PASS" if x["pass"] else "FAIL", x["id"], x["q"], x["problems"] or "")
save(f"eval_{version}_rerun", out)          # the recorded first runs stay untouched
