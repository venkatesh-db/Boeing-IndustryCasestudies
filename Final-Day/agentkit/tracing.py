"""Observability: every step becomes one line in results/traces.jsonl."""
from __future__ import annotations

import contextvars
import json
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

TRACE_FILE = Path(__file__).resolve().parents[1] / "results" / "traces.jsonl"
_parent: contextvars.ContextVar[str | None] = contextvars.ContextVar("parent", default=None)
_trace: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace", default=None)


# snippet:span
@contextmanager
def span(name: str, **attrs: Any) -> Iterator[dict]:
    """Time a step, link it to its parent, and record whether it failed."""
    span_id, parent = uuid.uuid4().hex[:8], _parent.get()
    trace_id = _trace.get() or uuid.uuid4().hex[:12]
    tokens = (_parent.set(span_id), _trace.set(trace_id))
    record = {"trace": trace_id, "span": span_id, "parent": parent, "name": name, "status": "ok", **attrs}
    start = time.perf_counter()
    try:
        yield record
    except Exception as err:
        record["status"] = f"error: {type(err).__name__}"
        raise
    finally:
        record["ms"] = round((time.perf_counter() - start) * 1000, 1)
        _parent.reset(tokens[0])
        _trace.reset(tokens[1])
        TRACE_FILE.parent.mkdir(exist_ok=True)
        with TRACE_FILE.open("a") as f:
            f.write(json.dumps(record, default=str) + "\n")
# end:span


def read_traces(limit: int = 200) -> list[dict]:
    if not TRACE_FILE.exists():
        return []
    return [json.loads(line) for line in TRACE_FILE.read_text().splitlines()[-limit:]]
