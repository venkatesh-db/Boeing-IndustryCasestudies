"""Lab 5 - MCP: client, raw messages, then the same server's tools inside LangChain."""
import asyncio
import subprocess
import sys

from _common import ROOT, save
from langchain_mcp_adapters.client import MultiServerMCPClient

for script in ("client", "wire"):
    subprocess.run([sys.executable, str(ROOT / "mcp_basic" / f"{script}.py")], check=True)


async def adapters() -> dict:
    client = MultiServerMCPClient({"parts": {"transport": "stdio", "command": sys.executable,
                                             "args": [str(ROOT / "mcp_basic" / "server.py")]}})
    lc_tools = {t.name: t for t in await client.get_tools()}
    result = await lc_tools["get_aircraft_status"].ainvoke({"tail_number": "N456CD"})
    return {"tools": sorted(lc_tools), "result": result}

r = asyncio.run(adapters())
print(r)
save("mcp_langchain", r)
