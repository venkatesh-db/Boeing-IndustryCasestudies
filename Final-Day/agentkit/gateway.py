"""A basic agent gateway: agents never talk directly, every message passes one checkpoint."""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Callable

from pydantic import BaseModel, ConfigDict, Field


# snippet:envelope
class Envelope(BaseModel):
    """What every agent message must look like."""
    model_config = ConfigDict(extra="forbid")
    id: str
    sender: str
    to: str
    task: str = Field(max_length=500)
    body: dict
    hops: int = Field(default=0, ge=0)
    signature: str
# end:envelope


def sign(secret: str, sender: str, to: str, task: str, body: dict) -> str:
    raw = json.dumps([sender, to, task, body], sort_keys=True).encode()
    return hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()


@dataclass
class Agent:
    secret: str
    handler: Callable[[dict], dict]
    may_call: tuple[str, ...] = ()


# snippet:gateway
class Gateway:
    MAX_HOPS, MAX_PER_MINUTE = 3, 5

    def __init__(self) -> None:
        self.agents: dict[str, Agent] = {}
        self.audit: list[dict] = []
        self._recent: dict[str, deque] = defaultdict(deque)
        self._seen: set[str] = set()

    def register(self, name: str, agent: Agent) -> None:
        self.agents[name] = agent

    def send(self, message: dict) -> dict:
        verdict, reply = self._check_and_deliver(message)
        self.audit.append({"id": message.get("id"), "from": message.get("sender"), "to": message.get("to"), "verdict": verdict})
        return {"verdict": verdict, "reply": reply}

    def _check_and_deliver(self, message: dict) -> tuple[str, dict | None]:
        try:
            env = Envelope.model_validate(message)                                   # 1 shape
        except ValueError as err:
            return f"rejected: bad message ({err.error_count()} problem)", None
        sender = self.agents.get(env.sender)
        if not sender or not hmac.compare_digest(env.signature, sign(sender.secret, env.sender, env.to, env.task, env.body)):
            return "rejected: not who it claims to be", None                         # 2 identity
        if env.to not in self.agents or env.to not in sender.may_call:
            return f"rejected: {env.sender} may not call {env.to}", None             # 3 permission
        if env.id in self._seen:
            return "rejected: replayed message", None                                # 4 replay
        if env.hops > self.MAX_HOPS:
            return "rejected: too many hops (loop?)", None                           # 5 loops
        recent, now = self._recent[env.sender], time.monotonic()
        while recent and now - recent[0] > 60:
            recent.popleft()
        if len(recent) >= self.MAX_PER_MINUTE:
            return "rejected: rate limit", None                                      # 6 rate
        recent.append(now)
        self._seen.add(env.id)
        return "delivered", self.agents[env.to].handler(env.body)
# end:gateway
