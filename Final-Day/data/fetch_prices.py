"""Read prices from each vendor's own page and keep the exact row as evidence. Run again to refresh."""
import datetime as dt
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).with_name("prices.json")
UA = {"User-Agent": "Mozilla/5.0"}


def get(url: str) -> str:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode()


def money(cell: str) -> float | None:
    m = re.search(r"\$([\d.]+)", cell)
    return float(m.group(1)) if m else None


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


rows: list[dict] = []
url = "https://developers.openai.com/api/docs/pricing.md"
text = get(url)
std, batch = text.split("### Batch pricing data")[0], text.split("### Batch pricing data")[1].split("### Flex")[0]
for model in ("gpt-6.2-sol", "gpt-6.1-terra", "gpt-6-luna"):
    s = next(l for l in std.splitlines() if l.startswith(f"| {model} |"))
    b = next(l for l in batch.splitlines() if l.startswith(f"| {model} |"))
    c, d = cells(s), cells(b)
    rows.append({"vendor": "OpenAI", "model": model, "input": money(c[1]), "output": money(c[2]), "cached": money(c[3]),
                 "batch_input": money(d[1]), "batch_output": money(d[2]), "url": url, "evidence": s})
for model in ("gpt-4.1", "gpt-4.1-mini"):
    s = next(l for l in std.splitlines() if l.startswith(f"| {model} |"))
    b = next(l for l in batch.splitlines() if l.startswith(f"| {model} |"))
    c, d = cells(s), cells(b)
    rows.append({"vendor": "OpenAI", "model": model, "input": money(c[1]), "output": money(c[2]), "cached": money(c[3]),
                 "batch_input": money(d[1]), "batch_output": money(d[2]), "url": url, "evidence": s})

url = "https://platform.claude.com/docs/en/about-claude/pricing.md"
text = get(url)
batch = text.split("### Batch processing")[1]
for name in ("Claude Opus 5.5", "Claude Sonnet 5.5", "Claude Haiku 5.5"):
    s = next(l for l in text.splitlines() if l.startswith(f"| {name} ") and l.count("|") == 7)
    b = next(l for l in batch.splitlines() if l.startswith(f"| {name} "))
    c, d = cells(s), cells(b)
    rows.append({"vendor": "Anthropic", "model": name, "input": money(c[1]), "output": money(c[5]), "cached": money(c[4]),
                 "cache_write": money(c[2]), "batch_input": money(d[1]), "batch_output": money(d[2]), "url": url, "evidence": s,
                 "note": "Price for prompts up to 100,000 tokens; higher above that." if "Haiku" in name else ""})

url = "https://ai.google.dev/gemini-api/docs/pricing.md.txt"
text = get(url)
for name in ("Gemini 4 Argon", "Gemini 4 Neon", "Gemini 4 Hydrogen"):
    block = text.split(f"## {name}  ")[1].split("\n## ")[0]
    standard = block.split('tab title="Standard"')[1].split("{% /tab %}")[0]
    batchb = block.split('tab title="Batch"')[1].split("{% /tab %}")[0] if 'tab title="Batch"' in block else ""

    def field(src: str, label: str) -> str:
        m = re.search(rf"\* {re.escape(label)}[^\n]*\n(.*?)\n\s*---", src, re.S)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    i, o, k = field(standard, "Input price"), field(standard, "Output price"), field(standard, "Context caching price")
    later = re.search(r"\$([\d.]+) starting (\w+ \d+, \d{4})", i)
    row = {"vendor": "Google", "model": name, "input": money(i), "output": money(o), "cached": money(k),
           "batch_input": money(field(batchb, "Input price")) if batchb else None,
           "batch_output": money(field(batchb, "Output price")) if batchb else None, "url": url, "evidence": f"Input: {i} | Output: {o} | Cache: {k}"}
    if later:
        o2 = re.search(r"\$([\d.]+) starting", o)
        row |= {"changes_on": later.group(2), "input_after": float(later.group(1)), "output_after": float(o2.group(1)), "note": f"Price changes on {later.group(2)}."}
    rows.append(row)

for region, label in (("eastus2", "Azure East US 2"), ("germanywestcentral", "Azure Germany West Central")):
    flt = f"productName eq 'Azure OpenAI' and armRegionName eq '{region}' and contains(meterName,'gpt 4.1 ')"
    url = "https://prices.azure.com/api/retail/prices?$filter=" + urllib.parse.quote(flt)
    items, nxt = [], url
    while nxt:
        page = json.loads(get(nxt)); items += page["Items"]; nxt = page.get("NextPageLink")
    price = {i["meterName"]: i["retailPrice"] for i in items if i["type"] == "Consumption"}
    for kind, tag in (("glbl", "Global"), ("Data Zone", "Data Zone"), ("regnl", "Regional")):
        def at(meter: str) -> float | None:
            v = price.get(f"gpt 4.1 {meter} {kind} Tokens"); return round(v * 1000, 4) if v is not None else None
        if at("Inp") is None or at("Outp") is None:
            continue
        bk = {"glbl": "glbl", "Data Zone": "Data Zone", "regnl": "regnl"}[kind]
        rows.append({"vendor": "Microsoft Azure", "model": f"GPT-4.1 {tag} ({region})", "input": at("Inp"), "output": at("Outp"), "cached": at("cached Inp"),
                     "batch_input": at("Batch Inp"), "batch_output": at("Batch Outp"), "url": url,
                     "evidence": json.dumps({m: p for m, p in price.items() if kind in m and m.startswith("gpt 4.1 ") and "mini" not in m and "nano" not in m})})

OUT.write_text(json.dumps({"fetched_at": dt.datetime.now().isoformat(timespec="seconds"), "unit": "USD per 1M tokens", "rows": rows}, indent=1))
for r in rows:
    print(f"{r['vendor']:16s} {r['model']:38s} in {r['input']} out {r['output']} cached {r['cached']} batch {r['batch_input']}/{r['batch_output']} {r.get('note', '')}")
