"""See the real messages: speak JSON-RPC to the server by hand, with no MCP library on the client side."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labs"))
from _common import save  # noqa: E402

log: list[dict] = []
proc = subprocess.Popen([sys.executable, str(ROOT / "mcp_basic" / "server.py")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)


def send(message: dict, expect_reply: bool = True) -> None:
    log.append({"from": "client", "message": message})
    proc.stdin.write(json.dumps(message) + "\n")
    proc.stdin.flush()
    if expect_reply:
        log.append({"from": "server", "message": json.loads(proc.stdout.readline())})


send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "by-hand", "version": "0.1"}}})
send({"jsonrpc": "2.0", "method": "notifications/initialized"}, expect_reply=False)
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
send({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "check_part_stock", "arguments": {"part_number": "HP-2201", "station": "FRA"}}})
send({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "reserve_part", "arguments": {"part_number": "HP-2201", "station": "FRA", "quantity": 1}}})
send({"jsonrpc": "2.0", "id": 5, "method": "tools/fly", "params": {}})
proc.stdin.close()
proc.wait(timeout=10)
for m in log:
    print(m["from"], json.dumps(m["message"])[:200])
save("mcp_wire", log)
