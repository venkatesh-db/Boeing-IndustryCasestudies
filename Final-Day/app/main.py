"""One local server: the API and the UI together.   uvicorn app.main:app --host 127.0.0.1 --port 8088"""
from __future__ import annotations

import hmac
import logging
import os
import secrets
import sys
import time
import uuid
from collections import OrderedDict, defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi import FastAPI, HTTPException, Request  # noqa: E402
from fastapi.responses import FileResponse, JSONResponse  # noqa: E402
from openai import APIConnectionError, NotFoundError  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from agentkit import llm, tools  # noqa: E402
from agentkit.agent import Run, approve, run_agent  # noqa: E402
from agentkit.tracing import read_traces  # noqa: E402

log = logging.getLogger("uvicorn.error")
CODE = os.getenv("FINALDAY_SUPERVISOR_CODE") or f"{secrets.randbelow(10000):04d}"
MAX_RUNS, PER_MINUTE = 100, 20
runs: OrderedDict[str, Run] = OrderedDict()
recent: dict[str, deque] = defaultdict(deque)

app = FastAPI(title="Final Day: parts-desk agent")
if not os.getenv("FINALDAY_SUPERVISOR_CODE"):
    log.warning("Supervisor code for this session: %s", CODE)


class Ask(BaseModel):
    question: str = Field(min_length=3, max_length=300)
    safe_mode: bool = False


class Approval(BaseModel):
    run_id: str
    code: str = Field(min_length=4, max_length=12)
    approve: bool = True


def view(run_id: str, run: Run) -> dict:
    return {"run_id": run_id, "question": run.question, "answer": run.answer, "stopped": run.stopped, "events": run.events,
            "pending": run.pending, "tokens_in": run.tokens_in, "tokens_out": run.tokens_out, "llm_calls": run.llm_calls}


@app.middleware("http")
async def limit(request: Request, call_next):
    if request.method == "POST":
        window, now = recent[request.client.host if request.client else "?"], time.monotonic()
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= PER_MINUTE:
            return JSONResponse({"error": "Too many requests. Wait a minute."}, status_code=429)
        window.append(now)
    return await call_next(request)


@app.exception_handler(APIConnectionError)
async def model_down(request: Request, err: APIConnectionError):
    return JSONResponse({"error": "The model server is not reachable. Start Ollama, then try again."}, status_code=503)


@app.exception_handler(NotFoundError)
async def model_missing(request: Request, err: NotFoundError):
    return JSONResponse({"error": f"The model '{llm.MODEL}' is not installed on the model server."}, status_code=503)


@app.exception_handler(Exception)
async def unexpected(request: Request, err: Exception):
    log.exception("unhandled error")
    return JSONResponse({"error": "Something went wrong on the server. See the server log."}, status_code=500)


@app.get("/")
def home():
    return FileResponse(Path(__file__).with_name("static") / "index.html")


@app.get("/health")
def health():
    """Ready only if the model server answers: a silent half-working start is worse than a clear failure."""
    try:
        names = [m.id for m in llm.client().with_options(timeout=3).models.list().data]
        ok = any(n.split(":")[0] == llm.MODEL.split(":")[0] for n in names)
        return JSONResponse({"status": "ok" if ok else "model missing", "model": llm.MODEL}, status_code=200 if ok else 503)
    except Exception:
        return JSONResponse({"status": "model server not reachable", "model": llm.MODEL}, status_code=503)


@app.get("/api/tools")
def list_tools():
    return [{"name": t.name, "description": t.description, "writes": t.writes, "schema": t.args.model_json_schema()} for t in tools.TOOLS.values()]


@app.post("/api/run")
def run(ask: Ask):
    result = run_agent(ask.question, safe_mode=ask.safe_mode)
    run_id = uuid.uuid4().hex[:10]
    runs[run_id] = result
    while len(runs) > MAX_RUNS:
        runs.popitem(last=False)
    return view(run_id, result)


@app.post("/api/approve")
def decide(body: Approval):
    found = runs.get(body.run_id)
    if not found or not found.pending:
        raise HTTPException(404, "Nothing is waiting for approval.")
    if not hmac.compare_digest(body.code.encode(), CODE.encode()):
        raise HTTPException(403, "Wrong supervisor code. Nothing was changed.")
    if not body.approve:
        found.log("rejected", by="supervisor")
        found.pending, found.stopped, found.answer = None, "rejected", "The supervisor rejected it. Nothing was changed."
        return view(body.run_id, found)
    try:
        approve(found, "supervisor")
    except (ValueError, LookupError) as err:
        found.log("tool_error", tool="reserve_part", error=str(err))
        found.pending, found.stopped, found.answer = None, "could not reserve", f"Approved, but not possible: {err}."
    return view(body.run_id, found)


@app.get("/api/metrics")
def metrics():
    done = list(runs.values())
    stops: dict[str, int] = defaultdict(int)
    for r in done:
        stops[r.stopped.split(":")[0]] += 1
    return {"runs": len(done), "llm_calls": sum(r.llm_calls for r in done), "tokens_in": sum(r.tokens_in for r in done),
            "tokens_out": sum(r.tokens_out for r in done), "stopped": stops}


@app.get("/api/traces")
def traces(limit: int = 40):
    return read_traces(max(1, min(limit, 200)))
