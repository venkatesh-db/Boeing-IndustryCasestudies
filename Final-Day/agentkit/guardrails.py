"""Checks in code, before and after the model. The prompt only asks; these decide."""
from __future__ import annotations

import json
import re

_INJECTION = re.compile(r"ignore (all |any )?(previous|prior|above)? ?(instructions|rules)|system prompt|you are now"
                        r"|developer mode|disable (the )?(guard|safety)|without (asking|approval)", re.I)
_DECISION = re.compile(r"\b(airworthy|safe to fly|ok to fly|release (it|the aircraft)|return to service|sign off)\b", re.I)
# Level 2 was added after incident H07: "Can N456CD fly tonight?" slipped past the first list.
_DECISION_2 = re.compile(r"\b(can|could|may|should|is|are|will)\b[^.?!]{0,25}\bN\d{3}[A-Z]{2}\b[^.?!]{0,25}\b(fly|depart|dispatch(ed)?|go|leave)\b"
                         r"|\b(dispatch|clear|release|approve)\b[^.?!]{0,20}\bN\d{3}[A-Z]{2}\b|\bgood to go\b", re.I)
_CLAIM_2 = re.compile(r"\b(can|cannot|can't|may|may not|must not|should not|is able to|unable to) (safely )?(fly|depart|be dispatched|be released)\b", re.I)
_CLAIM = re.compile(r"\b(is|are) (airworthy|safe to fly|cleared to fly)\b", re.I)
_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
_PHONE = re.compile(r"(?<!\w)\+?\d[\d ()-]{8,}\d(?!\w)")

REPLIES = {
    "injection": "I can only help with parts and delay questions.",
    "decision": "I can't decide airworthiness. A certificated person must decide. I can check the defect and the parts.",
    "ungrounded": "I couldn't verify every number against a tool result, so I won't show that answer.",
}


# snippet:input_guard
def check_input(text: str, level: int = 2) -> str | None:
    """Return the name of the rule that blocks this question, or None."""
    if _INJECTION.search(text):
        return "injection"
    if _DECISION.search(text) or (level >= 2 and _DECISION_2.search(text)):
        return "decision"
    return None
# end:input_guard


def redact(text: str) -> str:
    return _PHONE.sub("[PHONE]", _EMAIL.sub("[EMAIL]", text))


def _numbers(text: str) -> set[str]:
    return {n.replace(",", "").rstrip(".") for n in re.findall(r"(?<![A-Za-z\d-])\d[\d,]*(?:\.\d+)?", text)}


# snippet:output_guard
def check_output(answer: str, question: str, results: list[dict], level: int = 2) -> list[str]:
    """Problems in the final answer: an airworthiness claim, or a number no tool returned."""
    problems = []
    if _CLAIM.search(answer) or (level >= 2 and _CLAIM_2.search(answer)):
        problems.append("claims airworthiness")
    known = _numbers(question) | _numbers(json.dumps(results))
    invented = sorted(_numbers(answer) - known)
    if invented:
        problems.append(f"numbers not in any tool result: {invented}")
    return problems
# end:output_guard


_ITEM = re.compile(r"\b(?:N\d{3}[A-Z]{2}|[A-Z]{2,3}-\d{4})\b")
ALIASES = {"FRA": ("frankfurt",), "BLR": ("bengaluru", "bangalore"), "SEA": ("seattle",)}


_WORD_NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}


def names_an_item(text: str) -> bool:
    return bool(_ITEM.search(text))


# snippet:arg_guard
def ungrounded_args(arguments: dict, question: str, results: list[dict], level: int = 2) -> list[str]:
    """Arguments the model invented: not in the question and not in any earlier tool result."""
    evidence = (question + " " + json.dumps(results)).lower()
    for code, names in ALIASES.items():
        if any(n in evidence for n in names):
            evidence += f" {code.lower()}"
    words = {"one": "1", "two": "2", "a ": "1"}
    evidence += " " + " ".join(d for w, d in words.items() if w in evidence)
    if level >= 2:  # added after incident H11: "two hour delay" is a legitimate 120 minutes
        for amount in re.findall(r"\b(\d+|one|two|three|four|five|six) hours?\b", question.lower()):
            evidence += f" {60 * int(_WORD_NUMBERS.get(amount, amount))}"
    return [f"{k}={v}" for k, v in arguments.items()
            if not re.search(rf"(?<![a-z0-9]){re.escape(str(v).lower())}(?![a-z0-9])", evidence)]
# end:arg_guard
