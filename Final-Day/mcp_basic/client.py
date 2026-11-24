"""A basic MCP client: start the server, see what it offers, use all three kinds of things."""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labs"))
from _common import save  # noqa: E402
from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402


# snippet:mcp_client
async def main() -> dict:
    out: dict = {}
    server = StdioServerParameters(command=sys.executable, args=[str(ROOT / "mcp_basic" / "server.py")])
    async with stdio_client(server) as (read, write), ClientSession(read, write) as session:
        hello = await session.initialize()                              # 1. shake hands
        out["server"], out["protocol"] = hello.serverInfo.name, hello.protocolVersion
        out["tools"] = [t.name for t in (await session.list_tools()).tools]          # 2. discover
        out["resources"] = [str(r.uri) for r in (await session.list_resources()).resources]
        out["prompts"] = [p.name for p in (await session.list_prompts()).prompts]
        out["calls"] = []                                                # 3. use
        for name, args in [("check_part_stock", {"part_number": "HP-2201", "station": "FRA"}),
                           ("check_part_stock", {"part_number": "HP-2201", "station": "LHR"}),
                           ("reserve_part", {"part_number": "HP-2201", "station": "FRA", "quantity": 1})]:
            r = await session.call_tool(name, args)
            out["calls"].append({"tool": name, "args": args, "is_error": r.isError, "text": r.content[0].text})
        out["resource"] = (await session.read_resource("parts://stock")).contents[0].text
        out["prompt"] = (await session.get_prompt("triage", {"tail_number": "N123AB"})).messages[0].content.text
    return out
# end:mcp_client


if __name__ == "__main__":
    result = asyncio.run(main())
    for k, v in result.items():
        print(k, "->", v)
    save("mcp_client", result)
