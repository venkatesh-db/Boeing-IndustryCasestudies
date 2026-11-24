"""A fictional bank's support assistant: guardrails -> retrieval -> LLM -> output checks (training sample).

Uses the same OpenAI-compatible API as AeroGuard. Local default: Ollama + llama3.
"""
from __future__ import annotations

import os
import re
import time
from pathlib import Path

from openai import OpenAI
from rank_bm25 import BM25Okapi

import bank_guard as guard

HERE = Path(__file__).parent
MODEL = os.getenv("CHAT_MODEL", "llama3")
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "ollama"),
                 base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"))

SYSTEM = """ROLE: You are the support assistant of a bank. You answer customers' questions about fees, cards and disputes.
CONSTRAINTS:
- Use ONLY the numbered policy lines. Cite each fact like [P1].
- If the policy lines do not contain the answer, reply exactly: NOT_FOUND
- Never give investment advice. Never ask for a full card number, PIN or password.
- Answer in at most 3 short sentences, in a friendly tone."""


def _load_lines() -> list[tuple[str, str]]:
    """Every bullet of every policy becomes one searchable line, tagged with its document id."""
    lines = []
    for path in sorted((HERE / "policies").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        doc_id = re.search(r"^doc_id: (.+)$", text, re.MULTILINE).group(1)
        lines += [(doc_id, ln[2:].strip()) for ln in text.splitlines() if ln.startswith("- ")]
    return lines


LINES = _load_lines()
_bm25 = BM25Okapi([re.findall(r"[a-z0-9]+", t.lower()) for _, t in LINES])
RETRIEVAL = os.getenv("RETRIEVAL", "hybrid")   # v1 was "keyword"; the eval showed why that is not enough
_vectors = None


def _embed(texts: list[str]) -> list[list[float]]:
    data = _client.embeddings.create(model=os.getenv("EMBED_MODEL", MODEL), input=texts).data
    return [d.embedding for d in data]


def _cosine_ranking(question: str) -> list[int]:
    global _vectors
    if _vectors is None:
        _vectors = _embed([t for _, t in LINES])
    q = _embed([question])[0]
    norm = lambda v: sum(x * x for x in v) ** 0.5
    sims = [sum(a * b for a, b in zip(q, v)) / (norm(q) * norm(v)) for v in _vectors]
    return sorted(range(len(LINES)), key=lambda i: sims[i], reverse=True)


TOP_K = int(os.getenv("TOP_K", "4"))   # v1 used 3; the eval showed the right line ranked #4


def retrieve(question: str, k: int = TOP_K) -> list[tuple[str, str]]:
    scores = _bm25.get_scores(re.findall(r"[a-z0-9]+", question.lower()))
    keyword = [i for i in sorted(range(len(LINES)), key=lambda i: scores[i], reverse=True) if scores[i] > 0]
    if RETRIEVAL == "keyword":
        return [LINES[i] for i in keyword[:k]]
    fused: dict[int, float] = {}                    # hybrid: reciprocal rank fusion, as in AeroGuard (k=60)
    for ranking in (keyword, _cosine_ranking(question)):
        for rank, i in enumerate(ranking):
            fused[i] = fused.get(i, 0.0) + 1.0 / (60 + rank + 1)
    return [LINES[i] for i in sorted(fused, key=fused.get, reverse=True)[:k]]


def handle(question: str) -> dict:
    """The whole production flow for one customer message."""
    start = time.perf_counter()
    clean, redacted = guard.redact_pii(question)                 # 1. personal data never travels further
    route, reason = guard.route(clean)                           # 2. decide the route before any LLM call
    result = {"question": question, "seen_by_llm": None, "redacted": redacted, "route": route, "reason": reason,
              "sources": [], "llm_called": False, "problems": []}
    if route != "answer":                                        # 3. fixed, safe replies: no LLM, no tokens
        result.update(answer=guard.FIXED[route], answered=False)
    else:
        sources = retrieve(clean)                                # 4. ground the answer in policy lines
        numbered = "\n".join(f"[P{i}] ({d}) {t}" for i, (d, t) in enumerate(sources, start=1))
        user = f"Policy lines:\n{numbered or '(none)'}\n\nCustomer: {clean}"
        reply = _client.chat.completions.create(model=MODEL, temperature=0, messages=[
            {"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]).choices[0].message.content or ""
        result.update(seen_by_llm=clean, sources=[d for d, _ in sources], llm_called=True)
        problems = [] if "NOT_FOUND" in reply else guard.check_answer(reply, len(sources))   # 5. output checks
        if "NOT_FOUND" in reply or problems:
            result.update(answer=guard.NO_ANSWER, answered=False, problems=problems, raw=reply)
        else:
            result.update(answer=reply.strip(), answered=True)
    result["latency_ms"] = round((time.perf_counter() - start) * 1000, 1)
    return result


if __name__ == "__main__":
    import sys
    print(handle(" ".join(sys.argv[1:]) or "How much is the fee for paying by card abroad?"))
