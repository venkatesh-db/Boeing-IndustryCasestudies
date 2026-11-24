# Media_Publishing_GenAI

21 real media and publishing products that shipped GenAI between 2023 and 2025. Each one is traced through **before deployment → after deployment → outcome**, and every fact is tied to a cited source.

## Files

| File | What it is |
|---|---|
| `index.html` | The experience: product explorer with animated three-stage view, challenge filter, pattern charts, lessons linked to cases, and the verification log |
| `evidence-log.md` | The full written log: every product, every fact with its source number and check result, every source with its link status, and the research log |
| `data/media_evidence.json` | The single source of truth (21 products + 1 study) |
| `data/research_log.json` | Every search and page check that was run, with its result |
| `data/link_check.json` | HTTP status of every source URL |
| `data/fact_check.json` | Per-fact check: were the fact's numbers and quotes found on the live page? |
| `verify_facts.py` | Fetches every cited page and checks each fact against its text |
| `build.py` | Validates the data (no unsourced facts allowed), then builds the log and the page |
| `template.html` | Page template that the data is injected into |

## Rebuild

```bash
python3 verify_facts.py      # re-check facts against live pages
python3 build.py --check     # re-check links, validate, rebuild
```

## The "no assumption" rules

1. Every fact has a source number. A fact without one must say **"not publicly disclosed"**, and the build fails otherwise.
2. Dates are given to the day only when a source states the day; otherwise to the month.
3. Company denials and disagreements between sources are recorded in each case's `discrepancies` field.
4. Facts whose numbers or quotes could not be found on the live page were **rewritten to match the page or removed**. Examples: the "403 articles" count and a planned complaint in the Elle Belgium case, a Bloomberg expansion whose page blocks bots, and the BBC "51% → 37%" comparison.
5. **Limit:** about half the facts have no number or quote to match automatically. Those were checked by a person against search summaries and by keyword overlap with the live page. Read the source before quoting one on a slide.
