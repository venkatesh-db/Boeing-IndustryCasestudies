"""One door to the model. Works with any OpenAI-compatible server (default: local Ollama)."""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from dataclasses import dataclass
from functools import lru_cache

from openai import OpenAI

from agentkit.tracing import span

MODEL = os.getenv("FINALDAY_MODEL", "llama3")
BASE_URL = os.getenv("FINALDAY_BASE_URL", "http://localhost:11434/v1")


@dataclass(frozen=True)
class Reply:
    text: str
    tokens_in: int
    tokens_out: int
    ms: float
    cached: bool = False


@lru_cache
def client() -> OpenAI:
    return OpenAI(base_url=BASE_URL, api_key=os.getenv("FINALDAY_API_KEY", "ollama"), timeout=180)


_cache: dict[str, Reply] = {}


def complete(messages: list[dict], json_mode: bool = False, use_cache: bool = False) -> Reply:
    key = hashlib.sha256(json.dumps([MODEL, messages, json_mode]).encode()).hexdigest()
    if use_cache and key in _cache:
        with span("llm", cached=True, tokens_in=0, tokens_out=0):
            hit = _cache[key]
        return Reply(hit.text, 0, 0, 0.0, cached=True)
    extra = {"response_format": {"type": "json_object"}} if json_mode else {}
    start = time.perf_counter()
    with span("llm", model=MODEL, cached=False) as s:
        resp = client().chat.completions.create(model=MODEL, messages=messages, temperature=0, seed=7, **extra)
        s["tokens_in"], s["tokens_out"] = resp.usage.prompt_tokens, resp.usage.completion_tokens
    reply = Reply(resp.choices[0].message.content or "", resp.usage.prompt_tokens, resp.usage.completion_tokens,
                  round((time.perf_counter() - start) * 1000, 1))
    if use_cache:
        _cache[key] = reply
    return reply


def parse_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("no JSON object in the model's reply")
    data = json.loads(match.group(0))
    if not isinstance(data, dict):
        raise ValueError("the reply must be one JSON object")
    return data
