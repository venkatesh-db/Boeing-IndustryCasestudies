"""Lab 6 - AGP idea: one gateway between agents. (The AGNTCY project's AGP repository is now called SLIM.)"""
import secrets
import uuid

from _common import save
from agentkit import tools
from agentkit.gateway import Agent, Gateway, sign

gw = Gateway()
KEYS = {n: secrets.token_hex(16) for n in ("desk_agent", "parts_agent", "cost_agent")}
gw.register("desk_agent", Agent(KEYS["desk_agent"], lambda b: b, may_call=("parts_agent", "cost_agent")))
gw.register("parts_agent", Agent(KEYS["parts_agent"], lambda b: tools.execute("check_part_stock", b)))
gw.register("cost_agent", Agent(KEYS["cost_agent"], lambda b: tools.execute("estimate_delay_cost", b)))


def message(sender="desk_agent", to="parts_agent", task="stock", body=None, secret=None, **extra) -> dict:
    body = body or {"part_number": "HP-2201", "station": "FRA"}
    return {"id": uuid.uuid4().hex[:8], "sender": sender, "to": to, "task": task, "body": body,
            "signature": sign(secret or KEYS[sender], sender, to, task, body), **extra}


good = message()
tests = [("normal: desk asks parts", good), ("normal: desk asks cost", message(to="cost_agent", task="cost", body={"minutes": 45})),
         ("impostor: wrong secret", message(secret="guess")), ("not allowed: parts calls cost", message(sender="parts_agent", to="cost_agent", body={"minutes": 5})),
         ("replay: same message again", good), ("loop: 9 hops", message(hops=9)), ("extra field smuggled in", message(admin=True))]
tampered = message(); tampered["body"] = {"part_number": "HP-2201", "station": "SEA"}
tests.append(("tampered body", tampered))
tests += [(f"flood: message {i + 1}", message()) for i in range(5)]
out = []
for label, msg in tests:
    r = gw.send(msg)
    out.append({"label": label, **r}); print(f"{label:32s} {r['verdict']}", r["reply"] or "")
save("lab6", {"tests": out, "audit": gw.audit, "limits": {"hops": gw.MAX_HOPS, "per_minute": gw.MAX_PER_MINUTE}})
