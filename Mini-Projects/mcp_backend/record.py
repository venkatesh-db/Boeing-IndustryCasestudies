"""Connect a real MCP client, let llama3 choose from what it discovers, and save everything that happened."""
import asyncio
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).parent
QUESTIONS = ["What was last merged in the checkout repository?", "What is ticket PAY-101 about?", "How do we roll back checkout?",
             "Is the fix for PAY-101 merged in checkout, and do the release rules allow a release now?", "Look up three things: the checkout repository, ticket PAY-101, and the release-rules document. Is the fix merged, and can we release?", "What is the status of ticket PAY-999?", "Delete the checkout repository"]


def llm(system: str, user: str, as_json: bool = False) -> str:
    body = {"model": "llama3", "stream": False, "options": {"temperature": 0, "seed": 7},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    if as_json:
        body["format"] = "json"
    req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps(body).encode())
    return json.load(urllib.request.urlopen(req, timeout=180))["message"]["content"].strip()


async def one(session, menu: str, question: str, allowed: set[str]) -> dict:
    raw = llm("You choose what to look up. Available:\n" + menu + '\nReply with JSON only: {"use": [{"name": "<tool name or docs:// address>", '
              '"arguments": {"<argument>": "<value from the question>"}}]}. Copy each name exactly. If the question has several parts, look up every part. Choose only what the question needs. '
              'If nothing available can do it, reply {"use": []}.', question, True)
    steps = []
    try:
        plan = json.loads(re.search(r"\{.*\}", raw, re.S).group(0)).get("use", [])
    except (AttributeError, ValueError):
        plan = []
    for p in plan[:4]:
        name, args = str(p.get("name", "")), p.get("arguments") or {}
        if name not in allowed:
            steps.append({"name": name, "args": args, "ok": False, "text": "Not on the server’s menu, so it cannot run"})
        elif name.startswith("docs://"):
            steps.append({"name": name, "args": {}, "ok": True, "text": (await session.read_resource(name)).contents[0].text})
        else:
            r = await session.call_tool(name, args)
            steps.append({"name": name, "args": args, "ok": not r.isError, "text": r.content[0].text})
    facts = "\n".join(f"{s['name']}: {'' if s['ok'] else 'lookup error: '}{s['text']}" for s in steps)
    answer = llm("Answer in at most two short sentences using ONLY the facts. If a lookup failed or is missing, say so. Never claim you did an action.",
                 f"Facts:\n{facts}\n\nQuestion: {question}") if steps else None
    return {"q": question, "raw_plan": raw, "steps": steps, "answer": answer}


async def run(jira_down: bool) -> dict:
    env = {"PATH": os.environ["PATH"], **({"JIRA_DOWN": "1"} if jira_down else {})}
    async with stdio_client(StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")], env=env)) as (r, w), ClientSession(r, w) as s:
        hello = await s.initialize()
        tools, res = (await s.list_tools()).tools, (await s.list_resources()).resources
        menu = "\n".join([f'- name "{t.name}", arguments: {", ".join(t.inputSchema["properties"])}. {t.description}' for t in tools] + [f'- name "{x.uri}", no arguments. Document: {x.description}' for x in res])
        allowed = {t.name for t in tools} | {str(x.uri) for x in res}
        return {"server": hello.serverInfo.name, "protocol": hello.protocolVersion, "tools": [[t.name, t.description] for t in tools],
                "resources": [[str(x.uri), x.description] for x in res], "runs": [await one(s, menu, q, allowed) for q in QUESTIONS]}

out = {"normal": asyncio.run(run(False)), "jira_down": asyncio.run(run(True))}
(HERE / "recorded.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
for k, v in out.items():
    for x in v["runs"]:
        print(k, "|", x["q"], "|", [(s["name"], s["args"], s["ok"]) for s in x["steps"]], "|", x["answer"])
