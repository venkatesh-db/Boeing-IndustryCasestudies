"""Build index.html from recorded results and real source code. Nothing on the page is typed by hand as a result.

    python3 build_page.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
RES = HERE / "results"
NEEDED = ["lab1", "lab2", "lab3", "lab4", "lab4_first_try", "mcp_client", "mcp_wire", "mcp_langchain", "lab6", "lab7",
          "eval_v1", "eval_v2", "eval_v3", "lab9"]


def snippets() -> dict[str, dict[str, str]]:
    """Every '# snippet:name ... # end:name' block in the project, so the page always shows the code that ran."""
    found: dict[str, dict[str, str]] = {}
    for path in sorted([*HERE.glob("agentkit/*.py"), *HERE.glob("labs/*.py"), *HERE.glob("mcp_basic/*.py")]):
        for m in re.finditer(r"# snippet:(\w+)\n(.*?)\n# end:\1", path.read_text(), re.S):
            found[m.group(1)] = {"file": str(path.relative_to(HERE)), "code": m.group(2)}
    return found


def one_trace() -> list[dict]:
    """The last recorded v3 run of the two-step question, as spans."""
    path = RES / "traces.jsonl"
    spans = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    roots = [s for s in spans if s["name"] == "agent" and s.get("config") == "v3" and s.get("question", "").startswith("N123AB has a defect")]
    return [s for s in spans if roots and s["trace"] == roots[-1]["trace"]]


def main() -> None:
    missing = [n for n in NEEDED if not (RES / f"{n}.json").exists()]
    assert not missing, f"run the labs first, missing: {missing}"
    data = {n: json.loads((RES / f"{n}.json").read_text()) for n in NEEDED}
    saved = RES / "sample_trace.json"
    trace = one_trace()
    if trace:
        saved.write_text(json.dumps(trace, indent=1))
    data["trace"] = json.loads(saved.read_text())
    data["prices"] = json.loads((HERE / "data" / "prices.json").read_text())
    data["code"] = snippets()
    html = (HERE / "template.html").read_text()
    assert "/*__DATA__*/null" in html
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")       # never close the script tag early
    (HERE / "index.html").write_text(html.replace("/*__DATA__*/null", payload))
    print(f"OK: {len(data['code'])} code snippets, {len(data['trace'])} trace spans, {len(payload) // 1024} KB of data")


if __name__ == "__main__":
    main()
