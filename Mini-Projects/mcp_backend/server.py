"""A real MCP server over stdio. GitHub and Jira data are fictional samples, so no accounts or tokens are needed."""
import os

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

mcp = FastMCP("developer-assistant", log_level="ERROR")
REPOS = {"checkout": {"name": "checkout", "language": "Python", "open_pull_requests": 2, "tests": "passing",
                      "last_merged": "Fix for PAY-101: stop double charge (pull request 42)", "latest_release": "4.1 (does not include pull request 42)"}}
TICKETS = {"PAY-101": {"key": "PAY-101", "title": "Customers charged twice", "status": "In testing", "priority": "High", "assignee": "Asha"}}
DOCS = {"runbook": "Checkout runbook. To roll back: 1) open the release board, 2) choose the previous version, 3) ask the on-call lead to approve.",
        "release-rules": "Release rules. Release only when tests pass AND the ticket status is Done. No releases on Friday.",
        "architecture": "Checkout architecture. Checkout calls Payments, then Orders. Payments owns all charging."}


@mcp.tool()
def get_repository(name: str) -> dict:
    """GitHub: facts about one code repository, such as the last merged change, tests and release."""
    if name not in REPOS:
        raise ToolError(f"GitHub has no repository called {name}")
    return REPOS[name]


@mcp.tool()
def get_ticket(key: str) -> dict:
    """Jira: title, status, priority and owner of one ticket, such as PAY-101."""
    if os.getenv("JIRA_DOWN"):
        raise ToolError("Jira is not answering")
    if key not in TICKETS:
        raise ToolError(f"Jira has no ticket {key}")
    return TICKETS[key]


@mcp.resource("docs://runbook", description="How to roll back checkout")
def runbook() -> str:
    return DOCS["runbook"]


@mcp.resource("docs://release-rules", description="When a release is allowed")
def release_rules() -> str:
    return DOCS["release-rules"]


@mcp.resource("docs://architecture", description="Which service calls which")
def architecture() -> str:
    return DOCS["architecture"]


if __name__ == "__main__":
    mcp.run()
