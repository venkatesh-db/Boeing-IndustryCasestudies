"""Fast tests with no model. Every one of these protects something that went wrong in a real run."""
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agentkit import guardrails, tools  # noqa: E402
from agentkit.agent import Decision, approve, read_decision, run_agent  # noqa: E402
from agentkit.gateway import Agent, Gateway, sign  # noqa: E402
from agentkit.pricing import SHEET, cost  # noqa: E402


@pytest.fixture(autouse=True)
def private_traces(monkeypatch, tmp_path):
    monkeypatch.setattr("agentkit.tracing.TRACE_FILE", tmp_path / "t.jsonl")


@pytest.mark.parametrize("name,args,error", [
    ("check_part_stock", {"part_number": "pump", "station": "FRA"}, ValidationError),
    ("check_part_stock", {"part_number": "HP-2201", "station": "LHR"}, ValidationError),
    ("check_part_stock", {"part_number": "HP-2201", "station": "FRA", "x": 1}, ValidationError),
    ("check_part_stock", {"part_number": "ZZ-9999", "station": "FRA"}, LookupError),
    ("estimate_delay_cost", {"minutes": 0}, ValidationError),
    ("delete_stock", {}, PermissionError),
    ("reserve_part", {"part_number": "HP-2201", "station": "FRA", "quantity": 1}, PermissionError)])
def test_bad_calls_never_run(name, args, error):
    with pytest.raises(error):
        tools.execute(name, args)


def test_visitor_role_is_refused():
    with pytest.raises(PermissionError):
        tools.execute("check_part_stock", {"part_number": "HP-2201", "station": "FRA"}, role="visitor")


@pytest.mark.parametrize("q", ["Is N123AB airworthy?", "Can N456CD fly tonight?", "May we dispatch N123AB?", "Is N456CD good to go?"])
def test_airworthiness_questions_never_reach_the_model(q):
    run = run_agent(q, decide=lambda *_: pytest.fail("model was called"))
    assert run.stopped == "input guard: decision"


@pytest.mark.parametrize("q", ["We may fly a spare in. How many HP-2201 does SEA have?", "Which station is N456CD at?"])
def test_safe_questions_are_not_blocked(q):
    assert guardrails.check_input(q) is None


def test_invented_station_is_blocked():
    assert guardrails.ungrounded_args({"station": "FRA"}, "HP-2201 at N123AB's station?", [])
    assert not guardrails.ungrounded_args({"station": "FRA"}, "HP-2201 in Frankfurt?", [])
    assert not guardrails.ungrounded_args({"minutes": 120}, "a two hour delay", [])


def test_invented_number_in_answer_is_blocked():
    steps = iter([Decision(action="tool", tool="check_part_stock", arguments={"part_number": "HP-2201", "station": "FRA"}),
                  Decision(action="final", answer="There are 99.")])
    assert run_agent("HP-2201 at FRA?", decide=lambda *_: next(steps)).stopped == "output guard"


def test_answer_without_evidence_is_rejected():
    run = run_agent("How many HP-2201 at FRA?", decide=lambda *_: Decision(action="final", answer="Plenty."))
    assert run.stopped == "step limit" and any(e["kind"] == "no_evidence" for e in run.events)


def test_circles_and_endless_loops_stop():
    same = Decision(action="tool", tool="check_part_stock", arguments={"part_number": "HP-2201", "station": "FRA"})
    assert run_agent("HP-2201 at FRA", decide=lambda *_: same).stopped == "repeated the same call"


def test_write_needs_supervisor_and_safe_mode_blocks_it():
    want = Decision(action="tool", tool="reserve_part", arguments={"part_number": "HP-2201", "station": "FRA", "quantity": 1})
    q = "Reserve 1 of HP-2201 at FRA"
    assert run_agent(q, safe_mode=True, decide=lambda *_: want).stopped == "safe mode"
    run = run_agent(q, decide=lambda *_: want)
    with pytest.raises(PermissionError):
        approve(run, "planner")
    assert approve(run, "supervisor")["reserved"] == 1
    with pytest.raises(ValueError):
        approve(run, "supervisor")                       # cannot be approved twice


def test_flat_decision_is_read():
    assert read_decision({"tool": "final_answer", "arguments": {"answer": "ok"}}).answer == "ok"


def test_gateway_rejects_tampering_and_replay():
    gw = Gateway()
    gw.register("a", Agent("s1", lambda b: b, may_call=("b",)))
    gw.register("b", Agent("s2", lambda b: b))
    msg = {"id": "1", "sender": "a", "to": "b", "task": "t", "body": {"x": 1}, "signature": sign("s1", "a", "b", "t", {"x": 1})}
    assert gw.send(msg)["verdict"] == "delivered"
    assert "replayed" in gw.send(msg)["verdict"]
    assert "not who" in gw.send(msg | {"id": "2", "body": {"x": 2}})["verdict"]


def test_cost_maths():
    row = {"model": "m", "input": 2.0, "output": 10.0, "cached": 0.2, "batch_input": 1.0, "batch_output": 5.0}
    assert cost(row, 1_000_000, 0) == 2.0
    assert cost(row, 1_000_000, 0, cached_in=500_000) == pytest.approx(1.1)
    assert cost(row, 1_000_000, 1_000_000, batch=True) == 6.0
    assert all(r["input"] and r["output"] for r in SHEET["rows"])


def test_api_approval_flow(monkeypatch):
    monkeypatch.setenv("FINALDAY_SUPERVISOR_CODE", "2468")
    from fastapi.testclient import TestClient
    import app.main as m
    monkeypatch.setattr(m, "CODE", "2468")
    want = Decision(action="tool", tool="reserve_part", arguments={"part_number": "HP-2201", "station": "FRA", "quantity": 1})
    monkeypatch.setattr(m, "run_agent", lambda q, safe_mode: run_agent(q, safe_mode=safe_mode, decide=lambda *_: want))
    c = TestClient(m.app)
    r = c.post("/api/run", json={"question": "Reserve 1 of HP-2201 at FRA"}).json()
    assert r["pending"]
    assert c.post("/api/approve", json={"run_id": r["run_id"], "code": "0000"}).status_code == 403
    assert c.post("/api/approve", json={"run_id": r["run_id"], "code": "2468"}).json()["stopped"] == "approved and done"
    assert c.post("/api/approve", json={"run_id": r["run_id"], "code": "2468"}).status_code == 404
    assert c.post("/api/run", json={"question": "x"}).status_code == 422
