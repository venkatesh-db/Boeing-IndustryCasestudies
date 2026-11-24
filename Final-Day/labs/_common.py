"""Shared by the labs: import path and saving real results."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def save(name: str, data) -> None:
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / f"{name}.json").write_text(json.dumps(data, indent=1, default=str))
    print(f"saved results/{name}.json")


def run_dict(run) -> dict:
    return {k: getattr(run, k) for k in ("question", "role", "events", "results", "answer", "stopped", "pending",
                                         "tokens_in", "tokens_out", "llm_calls")}
