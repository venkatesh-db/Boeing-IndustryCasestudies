"""MCP server in front of fictional company systems. State lives in a JSON file chosen by the caller."""
import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

mcp = FastMCP("it-operations", log_level="ERROR")
STATE = Path(os.environ["ITOPS_STATE"])


def load() -> dict:
    return json.loads(STATE.read_text())


def service(name: str) -> dict:
    data = load()
    if name not in data:
        raise ToolError(f"unknown service {name}")
    return data[name]


@mcp.tool()
def service_health(service_name: str) -> dict:
    """Monitoring system: error rate and memory of one service."""
    return service(service_name)["health"]


@mcp.tool()
def recent_change(service_name: str) -> dict:
    """GitHub: the most recent release of one service."""
    if os.getenv("GITHUB_DOWN"):
        raise ToolError("GitHub is not answering")
    return service(service_name)["change"]


@mcp.tool()
def open_ticket(service_name: str) -> dict:
    """Jira: the open ticket for one service."""
    return service(service_name)["ticket"]


@mcp.resource("docs://runbook")
def runbook() -> str:
    """When to roll back and when to restart."""
    return ("Roll back when errors started after a release. Restart when memory is above 90 percent. "
            "If health is normal, do nothing. Every change needs approval.")


def change(name: str, action: str) -> dict:
    data = load()
    if name not in data:
        raise ToolError(f"unknown service {name}")
    if not os.getenv("REPAIR_FAILS"):
        data[name]["health"] = {"errors_percent": 0, "memory_percent": 41, "status": "healthy"}
        STATE.write_text(json.dumps(data))
    return {"done": action, "service": name}


@mcp.tool()
def roll_back_release(service_name: str) -> dict:
    """Change: return a service to its previous release."""
    return change(service_name, "rolled back")


@mcp.tool()
def restart_service(service_name: str) -> dict:
    """Change: restart a service."""
    return change(service_name, "restarted")


if __name__ == "__main__":
    mcp.run()
