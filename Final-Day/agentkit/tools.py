"""Custom tools: a typed input, a clear description, a function, and a safety label."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal

from pydantic import BaseModel, ConfigDict, Field

from agentkit.tracing import span

DATA = json.loads((Path(__file__).resolve().parents[1] / "data" / "demo_data.json").read_text())
Station = Literal["BLR", "FRA", "SEA"]


class Args(BaseModel):
    model_config = ConfigDict(extra="forbid")  # an invented argument is an error, not ignored


# snippet:custom_tool
class StockArgs(Args):
    part_number: str = Field(pattern=r"^[A-Z]{2,3}-\d{4}$", description="Part number such as HP-2201")
    station: Station = Field(description="Station code")


def check_part_stock(a: StockArgs) -> dict:
    if a.part_number not in DATA["stock"]:
        raise LookupError(f"unknown part {a.part_number}")
    return {"part_number": a.part_number, "station": a.station,
            "quantity": DATA["stock"][a.part_number][a.station], "lead_days": DATA["lead_days"][a.part_number]}
# end:custom_tool


class AircraftArgs(Args):
    tail_number: str = Field(pattern=r"^N\d{3}[A-Z]{2}$", description="Tail number such as N123AB")


def get_aircraft_status(a: AircraftArgs) -> dict:
    if a.tail_number not in DATA["aircraft"]:
        raise LookupError(f"unknown aircraft {a.tail_number}")
    return {"tail_number": a.tail_number, **DATA["aircraft"][a.tail_number]}


class DelayArgs(Args):
    minutes: int = Field(ge=1, le=1440, description="Delay in minutes, 1 to 1440")


def estimate_delay_cost(a: DelayArgs) -> dict:
    rate = DATA["delay_cost_per_minute_usd"]
    return {"minutes": a.minutes, "usd_per_minute": rate, "total_usd": a.minutes * rate}


class ReserveArgs(Args):
    part_number: str = Field(pattern=r"^[A-Z]{2,3}-\d{4}$", description="Part number such as HP-2201")
    station: Station = Field(description="Station code")
    quantity: int = Field(ge=1, le=2, description="How many to reserve, 1 or 2")


def reserve_part(a: ReserveArgs) -> dict:
    stock = DATA["stock"].get(a.part_number)
    if stock is None:
        raise LookupError(f"unknown part {a.part_number}")
    if stock[a.station] < a.quantity:
        raise ValueError(f"only {stock[a.station]} in stock at {a.station}")
    return {"reserved": a.quantity, "part_number": a.part_number, "station": a.station, "status": "reserved (demo)"}


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    args: type[BaseModel]
    fn: Callable[[Any], dict]
    writes: bool = False          # a write needs human approval
    roles: tuple[str, ...] = ("planner", "supervisor")


# snippet:registry
TOOLS: dict[str, Tool] = {t.name: t for t in (
    Tool("get_aircraft_status", "Model, station, open defect and needed part for one aircraft.",
         AircraftArgs, get_aircraft_status),
    Tool("check_part_stock", "Quantity on the shelf and lead days for one part at one station.",
         StockArgs, check_part_stock),
    Tool("estimate_delay_cost", "Delay cost in USD for a number of minutes.", DelayArgs, estimate_delay_cost),
    Tool("reserve_part", "Reserve a part at a station. Changes stock, so a supervisor must approve it.",
         ReserveArgs, reserve_part, writes=True),
)}
# end:registry


def openai_schema(tool: Tool) -> dict:
    return {"type": "function", "function": {"name": tool.name, "description": tool.description,
                                             "parameters": tool.args.model_json_schema()}}


def menu() -> str:
    """Short text version of the schemas, for models without native tool calling."""
    lines = []
    for t in TOOLS.values():
        props = t.args.model_json_schema()["properties"]
        args = ", ".join(f"{k}: {v.get('description', v.get('type'))}"
                         + (f" (one of {v['enum']})" if "enum" in v else "") for k, v in props.items())
        lines.append(f"- {t.name}({args}) -> {t.description}")
    return "\n".join(lines)


# snippet:execute
def execute(name: str, arguments: dict, role: str = "planner", approved: bool = False) -> dict:
    """The only way a tool runs: allowlist -> role -> schema -> approval -> function."""
    with span("tool", tool=name, role=role):
        if name not in TOOLS:
            raise PermissionError(f"'{name}' is not on the tool allowlist")
        tool = TOOLS[name]
        if role not in tool.roles:
            raise PermissionError(f"role '{role}' may not use {name}")
        args = tool.args.model_validate(arguments)
        if tool.writes and not approved:
            raise PermissionError(f"{name} changes data: human approval required")
        return tool.fn(args)
# end:execute
