# Final Day: build an agent you can trust

Open `index.html` for the experience, or run the live app:

```bash
./run_local.sh            # http://127.0.0.1:8088   demo supervisor code: 2468
```

Needs Ollama with `llama3`, and the AeroGuard virtual environment (or `pip install -r requirements-labs.txt`).

| Topic | Code | Run it |
|---|---|---|
| Function and tool calling | `agentkit/tools.py` | `labs/lab1_tool_calling.py` |
| Agent patterns, stops, safe mode | `agentkit/agent.py` | `labs/lab2_agent_patterns.py` |
| LangGraph: state, routing, persistence, approval, team | `labs/lab3_langgraph.py` | same file |
| LangChain: tools, retriever tool, create_agent | `labs/lab4_langchain.py` | same file |
| MCP: server, client, raw messages | `mcp_basic/` | `labs/lab5_mcp.py` |
| AGP idea: agent gateway | `agentkit/gateway.py` | `labs/lab6_gateway.py` |
| Guardrails | `agentkit/guardrails.py` | `labs/lab7_guardrails.py` |
| Evals | `agentkit/evals.py`, `data/eval_cases.json` | `labs/lab8_eval.py v3` |
| Cost and pricing | `agentkit/pricing.py`, `data/prices.json` | `labs/lab9_cost.py` |
| Observability | `agentkit/tracing.py` | `results/traces.jsonl` |
| Full stack | `app/` | `./run_local.sh` |

Run a lab from this folder: `../aeroguard/.venv/bin/python labs/lab1_tool_calling.py`
Tests: `../aeroguard/.venv/bin/python -m pytest -q tests`
Refresh prices: `python3 data/fetch_prices.py` · Rebuild the page: `python3 build_page.py`

## Recorded results (llama3 8B, 24 November 2026)

| Version | Dev (10) | Held-out (12) | Fresh (8) |
|---|---|---|---|
| v1 first try | 6 | 4 | - |
| v2 tuned on dev only | 10 | 7 | - |
| v3 fixes incidents H07 and H11 | 10 | 9 (seen by now) | 7 |

Small sets: demonstrations, not statistics. `eval_v1/2/3.json` are the recorded first runs; lab 8 writes to `*_rerun.json`.

## Known limits

- Word-list guards still miss "may it leave at 9?" and "pretend the rules are off".
- The LangChain policy question still fails (word search: "holding" vs "held").
- The team summary left out a fact; there is no completeness check.
- The Docker files were not built (Docker was not running). No real login, HTTPS or database: local lesson only.
- Reservations are demo replies and do not change the stock file.
- Prices are list prices on the fetch date; model quality was measured on llama3 only.
