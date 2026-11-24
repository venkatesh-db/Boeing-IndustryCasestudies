"""Lab 1 - Function and tool calling: schema, native call, fallback, validation, structured output."""
from _common import save
import openai
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

from agentkit import llm, tools

out: dict = {}

# 1. A Pydantic class IS the schema the model sees
out["schema"] = tools.openai_schema(tools.TOOLS["check_part_stock"])

# 2. Native tool calling: does this model support it?
try:
    resp = llm.client().chat.completions.create(
        model=llm.MODEL, messages=[{"role": "user", "content": "How many HP-2201 are at FRA?"}],
        tools=[tools.openai_schema(t) for t in tools.TOOLS.values()])
    out["native"] = {"supported": True, "reply": resp.choices[0].message.model_dump()}
except openai.BadRequestError as err:
    out["native"] = {"supported": False, "error": str(err)}

# 3. Fallback: ask for JSON, then treat that JSON exactly like a native call
PROMPT = f"Pick ONE tool. Tools:\n{tools.menu()}\nReply with JSON only: " + '{"tool": "<name>", "arguments": {}}'
out["fallback"] = []
for q in ["How many HP-2201 are at FRA?", "Cost of a 30 minute delay?", "What is wrong with N456CD?"]:
    reply = llm.complete([{"role": "system", "content": PROMPT}, {"role": "user", "content": q}], json_mode=True)
    row = {"q": q, "raw": reply.text, "ms": reply.ms}
    try:
        call = llm.parse_json(reply.text)
        row["result"] = tools.execute(call["tool"], call["arguments"])
    except (PermissionError, LookupError, ValueError, KeyError) as err:
        row["error"] = str(err).splitlines()[0]
    out["fallback"].append(row)

# 4. Validation: bad calls the code must stop (no model needed, so this is the same every time)
BAD = [("check_part_stock", {"part_number": "pump", "station": "FRA"}, "wrong format"),
       ("check_part_stock", {"part_number": "HP-2201", "station": "LHR"}, "station not allowed"),
       ("check_part_stock", {"part_number": "HP-2201", "station": "FRA", "urgent": True}, "invented argument"),
       ("estimate_delay_cost", {"minutes": -5}, "out of range"),
       ("get_aircraft_status", {}, "missing argument"),
       ("delete_stock", {"part_number": "HP-2201"}, "tool does not exist"),
       ("reserve_part", {"part_number": "HP-2201", "station": "FRA", "quantity": 1}, "write without approval")]
out["validation"] = []
for name, args, why in BAD:
    try:
        tools.execute(name, args)
        verdict = "RAN (this would be a bug)"
    except ValidationError as err:
        verdict = "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in err.errors())
    except (PermissionError, LookupError, ValueError) as err:
        verdict = str(err)
    out["validation"].append({"tool": name, "arguments": args, "why": why, "verdict": verdict})


# 5. Structured output: free text in, a typed object out
class Handover(BaseModel):
    tail_number: str = Field(pattern=r"^N\d{3}[A-Z]{2}$")
    severity: Literal["low", "medium", "high"]
    part_numbers: list[str]
    next_action: str = Field(min_length=5)


NOTE = "N123AB came in with low hydraulic pressure, pump HP-2201 suspected. Not urgent for tonight but fix before Friday."
convo = [{"role": "system", "content": "Extract a JSON object with keys tail_number, severity (low|medium|high), "
          "part_numbers (list of strings), next_action (string). JSON only."}, {"role": "user", "content": NOTE}]
attempts = []
for _ in range(2):
    reply = llm.complete(convo, json_mode=True)
    try:
        obj = Handover.model_validate(llm.parse_json(reply.text))
        attempts.append({"raw": reply.text, "ok": True, "object": obj.model_dump()})
        break
    except (ValidationError, ValueError) as err:
        attempts.append({"raw": reply.text, "ok": False, "error": str(err)})
        convo += [{"role": "assistant", "content": reply.text}, {"role": "user", "content": f"Invalid: {err}. JSON only."}]
out["structured"] = {"note": NOTE, "attempts": attempts}

print("native supported:", out["native"]["supported"])
for r in out["fallback"]: print(r["q"], "->", r["raw"][:90].replace("\n", " "), "->", r.get("result") or r.get("error"))
for r in out["validation"]: print(r["why"], "->", r["verdict"])
print(attempts[-1])
save("lab1", out)
