"""A basic MCP server: 3 tools, 1 resource, 1 prompt. Run by a client over stdio, or by hand for HTTP:
    python mcp_basic/server.py            (stdio)
    python mcp_basic/server.py http       (http://127.0.0.1:8090/mcp)
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.server.fastmcp.exceptions import ToolError  # noqa: E402

from agentkit import tools  # noqa: E402

# snippet:mcp_server
mcp = FastMCP("parts-desk", log_level="ERROR", host="127.0.0.1", port=8090)
ROLE = os.getenv("PARTS_ROLE", "planner")        # set by whoever starts the server, never by the model


def call(name: str, **arguments) -> dict:
    try:
        return tools.execute(name, arguments, role=ROLE)
    except (PermissionError, LookupError, ValueError) as err:
        raise ToolError(str(err)) from err


@mcp.tool()
def check_part_stock(part_number: str, station: str) -> dict:
    """Quantity on the shelf and lead days for one part at one station (BLR, FRA or SEA)."""
    return call("check_part_stock", part_number=part_number, station=station)


@mcp.tool()
def get_aircraft_status(tail_number: str) -> dict:
    """Model, station, open defect and needed part for one aircraft."""
    return call("get_aircraft_status", tail_number=tail_number)


@mcp.tool()
def reserve_part(part_number: str, station: str, quantity: int) -> dict:
    """Reserve a part. Always refused here: writes need a human approval outside MCP."""
    return call("reserve_part", part_number=part_number, station=station, quantity=quantity)


@mcp.resource("parts://stock")
def stock_list() -> str:
    """The whole stock table as JSON (data to read, not an action)."""
    import json
    return json.dumps(tools.DATA["stock"])


@mcp.prompt()
def triage(tail_number: str) -> str:
    """A reusable prompt template."""
    return f"Check {tail_number}: read its status, then the stock of the needed part at its station. Do not judge airworthiness."


if __name__ == "__main__":
    mcp.run(transport="streamable-http" if "http" in sys.argv[1:] else "stdio")
# end:mcp_server
