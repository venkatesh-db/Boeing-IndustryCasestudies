"""Lab 4 - LangChain: wrap existing functions as tools, use a ready-made retriever tool, run create_agent on llama3."""
import json
import uuid

from _common import ROOT, save
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_community.retrievers import BM25Retriever
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import StructuredTool, ToolException, create_retriever_tool
from langchain_core.utils.function_calling import convert_to_openai_tool

from agentkit import llm, tools

out: dict = {}


# snippet:wrap
def as_langchain(tool: tools.Tool) -> StructuredTool:
    """Existing function -> LangChain tool. Our execute() still does every safety check."""
    def run(**kwargs) -> dict:
        try:
            return tools.execute(tool.name, kwargs)
        except (LookupError, PermissionError, ValueError) as err:
            raise ToolException(str(err)) from err          # the agent sees the error instead of crashing
    return StructuredTool.from_function(name=tool.name, description=tool.description, args_schema=tool.args,
                                        func=run, handle_tool_error=True)
# end:wrap


lc_tools = [as_langchain(t) for t in tools.TOOLS.values() if not t.writes]     # read-only tools only

# A ready-made component: BM25 search over three policy notes, turned into a tool in one line
NOTES = ["Policy P1: a reservation needs supervisor approval.", "Policy P2: parts are held for 48 hours, then released.",
         "Policy P3: the duty manager owns the delay cost report."]
retriever = BM25Retriever.from_texts(NOTES, k=1)
lc_tools.append(create_retriever_tool(retriever, "search_policy", "Search parts-desk policy notes: approvals, holding time, who owns reports."))
out["tools"] = [convert_to_openai_tool(t)["function"]["name"] for t in lc_tools]
out["policy"] = lc_tools[-1].invoke({"query": "how long are parts held"})


# snippet:adapter
class JsonToolModel(BaseChatModel):
    """Gives a model without native tool calls the interface create_agent expects."""
    specs: list[dict] = []

    @property
    def _llm_type(self) -> str:
        return "json-tool-model"

    def bind_tools(self, tools, **kwargs):
        return self.model_copy(update={"specs": [convert_to_openai_tool(t)["function"] for t in tools]})

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        menu = "\n".join(f"- {s['name']}({', '.join(k + ': ' + v.get('description', '') for k, v in s['parameters']['properties'].items())})"
                         f" -> {s['description']}" for s in self.specs)
        convo = [{"role": "system", "content": f"Tools:\n{menu}\n- final_answer(answer)\nReply with JSON only: "
                  '{"tool": "<name>", "arguments": {"<name>": "<value from the question>"}}. When a tool result answers the question, use final_answer.'}]
        for m in messages:
            if isinstance(m, SystemMessage):
                convo[0]["content"] += "\n" + m.text
            elif isinstance(m, ToolMessage):
                convo.append({"role": "user", "content": f"Result of {m.name}: {m.text}"})
            elif isinstance(m, AIMessage):
                convo.append({"role": "assistant", "content": 
                              json.dumps({"tool": m.tool_calls[0]["name"], "arguments": m.tool_calls[0]["args"]}) if m.tool_calls else m.text})
            else:
                convo.append({"role": "user", "content": m.text})
        reply = llm.complete(convo, json_mode=True)
        data = llm.parse_json(reply.text)
        if data.get("tool") in {s["name"] for s in self.specs}:
            msg = AIMessage("", tool_calls=[{"name": data["tool"], "args": data.get("arguments") or {}, "id": uuid.uuid4().hex[:8]}])
        else:
            msg = AIMessage(str((data.get("arguments") or {}).get("answer") or data.get("answer") or reply.text))
        return ChatResult(generations=[ChatGeneration(message=msg)])
# end:adapter


# snippet:create_agent
agent = create_agent(JsonToolModel(), lc_tools, system_prompt="You are a parts-desk assistant. Never guess an argument.",
                     middleware=[ModelCallLimitMiddleware(run_limit=5), ToolCallLimitMiddleware(run_limit=4)])
# end:create_agent
out["runs"] = []
for q in ["How many HP-2201 are at FRA?", "How long are parts held?"]:
    try:
        r = agent.invoke({"messages": [{"role": "user", "content": q}]})
        steps = [{"type": m.type, "text": m.text[:300], "tool_calls": [{"name": c["name"], "args": c["args"]} for c in getattr(m, "tool_calls", [])]}
                 for m in r["messages"]]
        out["runs"].append({"q": q, "steps": steps})
    except Exception as err:
        out["runs"].append({"q": q, "error": f"{type(err).__name__}: {err}"[:300]})
for r in out["runs"]:
    print(r["q"], r.get("error"))
    for s in r.get("steps", []): print("   ", s)
save("lab4", out)
