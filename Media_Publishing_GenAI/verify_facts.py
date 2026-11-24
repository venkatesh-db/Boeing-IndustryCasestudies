"""Fact-level check: does each fact's key evidence appear in the cited page text?

For every fact with a source, this script extracts its "anchors": numbers (e.g. 41, 77, 99%)
and quoted phrases (e.g. "hidden gem"). It fetches the cited page, strips the HTML, and
checks whether each anchor appears there, or failing that, on another source for the same product.

Writes data/fact_check.json. Result per fact:
  verified      every anchor found on the cited page
  verified-alt  every anchor found, but on another source for the same product
  partial       some anchors found
  not-found     page loaded but no anchor found -> must be reviewed by a human
  no-anchor     no number or quote to match; keyword overlap with the source text is 50% or more
  low-overlap   no number or quote, and under 50% keyword overlap -> must be reviewed by a human
  blocked       page blocks automated access (403/429/timeout) -> human-reviewed only
"""
import concurrent.futures as cf
import html
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
EV = json.loads((HERE / "data" / "media_evidence.json").read_text())


def fetch(url: str) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (fact-check)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read().decode("utf-8", "ignore")
    except Exception:
        return None
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return re.sub(r"\s+", " ", text).lower().replace("’", "'").replace("“", '"').replace("”", '"')


def anchors(fact: str) -> list[str]:
    quoted = [q.lower() for q in re.findall(r'"([^"]{4,60})"', fact)]
    nums = [n.rstrip(".,") for n in re.findall(r"\b\d[\d,.]*%?", fact)]
    nums = [n for n in nums if len(n.strip("%")) >= 2 and not re.fullmatch(r"20[12]\d", n)]
    return quoted + nums


STOP = set("about after against also among another because before being between could during every first from have into itself later least more most other over said since some still such than that their them then there these they this those through under until were what when where which while with within would""".split())


def overlap(fact: str, texts: list) -> int:
    words = {w for w in re.findall(r"[a-z]{5,}", fact.lower()) if w not in STOP}
    if not words or not texts:
        return -1
    return round(100 * sum(1 for w in words if any(w in t for t in texts)) / len(words))


def main() -> None:
    urls = sorted({s[1] for p in EV["products"] for s in p["sources"]} | {s[1] for s in EV["studies"][0]["sources"]})
    with cf.ThreadPoolExecutor(10) as ex:
        pages = dict(zip(urls, ex.map(fetch, urls)))
    results, items = [], [(p["id"], p["sources"], st, p[st]) for p in EV["products"] for st in ("pre", "post", "outcome")]
    items += [(s["id"], s["sources"], "facts", s["facts"]) for s in EV["studies"]]
    for pid, srcs, stage, facts in items:
        for text, ref in facts:
            if ref == 0:
                continue
            a = anchors(text)
            page = pages.get(srcs[ref - 1][1])
            others = [pages.get(s[1]) for i, s in enumerate(srcs) if i != ref - 1 and pages.get(s[1])]
            if not a:
                status, missing = "no-anchor", []
            elif page is None and not others:
                status, missing = "blocked", a
            else:
                on_page = [x for x in a if page and x in page]
                elsewhere = [x for x in a if x not in on_page and any(x in o for o in others)]
                missing = [x for x in a if x not in on_page and x not in elsewhere]
                if not missing and not elsewhere:
                    status = "verified"
                elif not missing:
                    status = "verified-alt"
                elif on_page or elsewhere:
                    status = "partial"
                else:
                    status = "blocked" if page is None else "not-found"
            score = overlap(text, [x for x in [page, *others] if x])
            if status == "no-anchor" and score >= 0 and score < 50:
                status = "low-overlap"
            results.append({"overlap": score, "id": pid, "stage": stage, "ref": ref, "fact": text, "anchors": a, "missing": missing, "status": status})
    (HERE / "data" / "fact_check.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    from collections import Counter
    print(Counter(r["status"] for r in results))
    for r in results:
        if r["status"] in ("partial", "not-found", "low-overlap"):
            print(f"{r['id']}.{r['stage']} [S{r['ref']}] {r['status']} missing={r['missing']} :: {r['fact'][:90]}")


if __name__ == "__main__":
    main()
