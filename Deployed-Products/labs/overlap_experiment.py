"""Overlapping health-plan documents: does hybrid search hand a STANDARD member the PLUS plan's answer?
Fictional insurer and hospitals (training sample). Run: python overlap_experiment.py"""
import json, os, re
from pathlib import Path
from openai import OpenAI
from rank_bm25 import BM25Okapi

HERE = Path(__file__).parent
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "ollama"), base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"))
MODEL = os.getenv("CHAT_MODEL", "llama3")
LINES = []
for p in sorted((HERE / "health_policies").glob("*.md")):
    t = p.read_text()
    meta = dict(re.findall(r"^(doc_id|plan|year): (.+)$", t, re.M))
    LINES += [{**meta, "text": ln[2:]} for ln in t.splitlines() if ln.startswith("- ")]
tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
emb = lambda xs: [d.embedding for d in client.embeddings.create(model=MODEL, input=xs).data]
VEC = emb([l["text"] for l in LINES])
cos = lambda a, b: sum(x * y for x, y in zip(a, b)) / ((sum(x * x for x in a) ** .5) * (sum(y * y for y in b) ** .5))


def search(q, k=3, plan=None, year=None):
    idx = [i for i, l in enumerate(LINES) if (plan is None or l["plan"] == plan) and (year is None or l["year"] == year)]
    bm = BM25Okapi([tok(LINES[i]["text"]) for i in idx]); s = bm.get_scores(tok(q))
    kw = [idx[j] for j in sorted(range(len(idx)), key=lambda j: -s[j]) if s[j] > 0]
    qv = emb([q])[0]; vec = sorted(idx, key=lambda i: -cos(qv, VEC[i]))
    f = {}
    for r in (kw, vec):
        for n, i in enumerate(r): f[i] = f.get(i, 0) + 1 / (61 + n)
    return [(LINES[i], round(f[i], 4)) for i in sorted(f, key=f.get, reverse=True)[:k]]


def answer(q, hits):
    src = "\n".join(f"[P{n}] ({h['doc_id']}) {h['text']}" for n, (h, _) in enumerate(hits, 1))
    msg = [{"role": "system", "content": "You answer health-plan coverage questions using ONLY the numbered lines. Cite [P#]. Two sentences max."},
           {"role": "user", "content": f"{src}\n\nMember question: {q}"}]
    return client.chat.completions.create(model=MODEL, temperature=0, messages=msg).choices[0].message.content


Q = "Can I get cardiac surgery at Mercy Heart Institute covered?"
out = {}
for label, kw in [("no_filter", {}), ("plan_filter", {"plan": "STANDARD"}), ("plan_and_year_filter", {"plan": "STANDARD", "year": "2026"})]:
    hits = search(Q, **kw)
    out[label] = {"hits": [{"doc": h["doc_id"], "text": h["text"], "score": s} for h, s in hits], "answer": answer(Q, hits)}
    print(f"\n== {label} (member is on STANDARD 2026)")
    for h, s in hits: print(f"  {s:.4f}  {h['doc_id']:44s} {h['text'][:70]}")
    print("  ANSWER:", out[label]["answer"])
json.dump({"question": Q, "member": "STANDARD plan, 2026", **out}, open(HERE / "overlap_results.json", "w"), indent=1)
