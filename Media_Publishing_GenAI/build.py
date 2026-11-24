"""Build the Media & Publishing GenAI evidence log and experience page.

    python3 build.py --check   # re-check every source URL, then rebuild
    python3 build.py           # rebuild using data/link_check.json

Validation rules (the build fails if any is broken):
  * every fact points to a source number that exists for that product, OR
  * a fact with source number 0 must say "not publicly disclosed" (no unsourced claims)
  * every challenge / outcome tag is defined; every source URL has been link-checked
"""
import concurrent.futures as cf
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
EV = json.loads((DATA / "media_evidence.json").read_text())
RL = json.loads((DATA / "research_log.json").read_text())
FC_PATH = DATA / "fact_check.json"
FC = {(r["id"], r["fact"]): r for r in json.loads(FC_PATH.read_text())} if FC_PATH.exists() else {}
FC_LABEL = {"verified": "✅ matched on cited page", "verified-alt": "✅ matched on another source", "no-anchor": "🟡 human-checked (keywords ≥50%)",
            "partial": "⚠️ partly matched", "not-found": "❌ not matched", "low-overlap": "⚠️ low keyword overlap", "blocked": "🔒 page blocks bots"}


def urls() -> list[str]:
    out = {s[1] for p in EV["products"] for s in p["sources"]}
    out |= {s[1] for st in EV["studies"] for s in st["sources"]}
    return sorted(out)


def check_one(url: str) -> int | str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link-check)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # recorded, never hidden
        return type(e).__name__


def link_check() -> None:
    us = urls()
    with cf.ThreadPoolExecutor(12) as ex:
        res = list(ex.map(check_one, us))
    (DATA / "link_check.json").write_text(json.dumps(
        {"checked_at": dt.datetime.now().isoformat(timespec="seconds"),
         "results": [{"url": u, "status": s} for u, s in zip(us, res)]}, indent=1))


def check_facts(owner: str, facts: list, n_src: int) -> None:
    for text, ref in facts:
        if ref == 0:
            assert "not publicly disclosed" in text.lower(), f"{owner}: unsourced fact: {text}"
        else:
            assert 1 <= ref <= n_src, f"{owner}: bad source ref {ref}"


def validate(status: dict) -> None:
    ids = [p["id"] for p in EV["products"]]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for p in EV["products"]:
        n = len(p["sources"])
        assert n >= 2, f"{p['id']}: needs at least two sources"
        for stage in ("pre", "post", "outcome"):
            assert p[stage], f"{p['id']}: empty {stage}"
            check_facts(f"{p['id']}.{stage}", p[stage], n)
        assert all(c in EV["challenges"] for c in p["challenges"]), p["id"]
        assert all(o in EV["outcome_types"] for o in p["outcomes"]), p["id"]
        assert p["confidence"] in {"high", "medium-high", "medium"}, p["id"]
        assert "2023" <= p["date"][:4] <= "2025", f"{p['id']}: outside the time window"
    for s in EV["studies"]:
        check_facts(s["id"], s["facts"], len(s["sources"]))
    for u in urls():
        assert u in status, f"not link-checked: {u} (run with --check)"


def badge(code) -> str:
    if code == 200:
        return "200 OK"
    if code in (401, 403, 429) or code == "TimeoutError":
        return f"{code}: site blocks automated checks; found via web search"
    return f"{code}: CHECK MANUALLY"


def fact_md(facts, srcs, owner="") -> str:
    def tag(t, r):
        if not r:
            return "*(no source: not publicly disclosed)*"
        fc = FC.get((owner, t))
        return f"[S{r}]" + (f" · {FC_LABEL[fc['status']]}" if fc else "")
    return "<br>".join(f"• {t} {tag(t, r)}" for t, r in facts)


def build_md(status: dict, checked_at: str) -> None:
    ch, ot = EV["challenges"], EV["outcome_types"]
    codes = Counter(str(v) for v in status.values())
    n_facts = sum(len(p[s]) for p in EV["products"] for s in ("pre", "post", "outcome"))
    L = ["# Media & Publishing GenAI: Product Evidence Log", "",
         f"**Scope:** {EV['window']}  ", f"**Verified on:** {EV['verified_on']}  ", f"**Rule:** {EV['rule']}  ",
         f"**Totals:** {len(EV['products'])} products · {n_facts} individually sourced facts · {len(status)} source URLs  ",
         f"**Link check ({checked_at}):** " + ", ".join(f"{n} × {c}" for c, n in codes.most_common()) + ". "
         "A 200 proves the page exists. The claims were checked against search-result summaries of these sources.", "",
         "**Fact-level check:** " + ", ".join(f"{n} × {FC_LABEL[k]}" for k, n in Counter(r["status"] for r in FC.values()).most_common())
         + ". `verify_facts.py` fetches each cited page and looks for the fact's numbers and quoted phrases. Facts with neither are scored by keyword overlap.", "",
         "## Summary table", "",
         "| ID | Date | Company | Product | Challenges | Outcome | Confidence |", "|---|---|---|---|---|---|---|"]
    for p in sorted(EV["products"], key=lambda x: x["date"]):
        L.append(f"| {p['id']} | {p['date']} | {p['company']} | {p['product']} | "
                 + ", ".join(ch[c][1] for c in p["challenges"]) + " | "
                 + ", ".join(ot[o] for o in p["outcomes"]) + f" | {p['confidence']} |")
    L += ["", "## Products in detail", ""]
    for p in sorted(EV["products"], key=lambda x: x["date"]):
        L += [f"### {p['id']} · {p['company']}: {p['product']}", "",
              f"*{p['kind']} · {p['date']} · confidence **{p['confidence']}***", "",
              "| Stage | Evidence |", "|---|---|",
              f"| 🧰 Before deployment | {fact_md(p['pre'], p['sources'], p['id'])} |",
              f"| 🚨 After deployment | {fact_md(p['post'], p['sources'], p['id'])} |",
              f"| 🏁 Outcome | {fact_md(p['outcome'], p['sources'], p['id'])} |",
              f"| ⚠️ Discrepancies | {p['discrepancies']} |", "",
              "| # | Source | Type | Link check |", "|---|---|---|---|"]
        L += [f"| S{i} | [{t}]({u}) | {k} | {badge(status.get(u))} |" for i, (t, u, k) in enumerate(p["sources"], 1)]
        L.append("")
    L += ["## Industry study", ""]
    for s in EV["studies"]:
        L += [f"### {s['id']} · {s['title']} ({s['date']})", "", fact_md(s["facts"], s["sources"], s["id"]), "", f"*Why it matters:* {s['why']}", ""]
        L += [f"- S{i}: [{t}]({u}) ({k}, {badge(status.get(u))})" for i, (t, u, k) in enumerate(s["sources"], 1)]
        L.append("")
    L += ["## Research log", "", f"Run on {RL['date']}. {RL['tool']}.", "", "| Query | Product | Result |", "|---|---|---|"]
    L += [f"| {q} | {pid} | {r} |" for q, pid, r in RL["queries"]]
    L += ["", "**Considered but not included:**", ""] + [f"- {a}: {b}" for a, b in RL["considered_not_included"]]
    L += ["", "*Generated by `build.py` from `data/`. Edit the JSON, never this file.*", ""]
    (HERE / "evidence-log.md").write_text("\n".join(L))


def build_html(status: dict, checked_at: str) -> None:
    tpl = (HERE / "template.html").read_text()
    payload = dict(EV, status=status, checked_at=checked_at, research=RL,
                   factcheck={f"{k[0]}|{k[1]}": v["status"] for k, v in FC.items()})
    (HERE / "index.html").write_text(tpl.replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False)))


def main() -> None:
    if "--check" in sys.argv:
        link_check()
    lc = json.loads((DATA / "link_check.json").read_text())
    status = {r["url"]: r["status"] for r in lc["results"]}
    validate(status)
    build_md(status, lc["checked_at"])
    build_html(status, lc["checked_at"])
    bad = [u for u, s in status.items() if s not in (200, 401, 403, 429, "TimeoutError")]
    print(f"OK: {len(EV['products'])} products, {len(status)} URLs; needs manual check: {len(bad)}")
    for u in bad:
        print("  ", status[u], u)


if __name__ == "__main__":
    main()
