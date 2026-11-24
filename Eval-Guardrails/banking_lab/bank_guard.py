"""Guardrails for a fictional bank's support assistant (training sample, not a real bank's rules).

Input guards decide the ROUTE before any LLM call; output guards check the answer after it.
"""
from __future__ import annotations

import re

# ---------------- input: personal data (redact before anything else sees it)
_CARD = re.compile(r"\b\d(?:[ -]?\d){12,18}\b")  # v2: digits with optional single separators; never eats trailing space
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}(?: ?[A-Z0-9]{1,3})?\b")
_ACCOUNT = re.compile(r"\b(account(?: number| no\.?)?[:#\s]*)(\d{8,12})\b", re.IGNORECASE)
_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")


def luhn_ok(digits: str) -> bool:
    """Card numbers carry a check digit (Luhn). Using it avoids redacting harmless reference numbers."""
    total, parity = 0, len(digits) % 2
    for i, ch in enumerate(digits):
        d = int(ch)
        if i % 2 == parity:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
    return total % 10 == 0


def redact_pii(text: str) -> tuple[str, list[str]]:
    found: list[str] = []

    def card(m: re.Match) -> str:
        digits = re.sub(r"\D", "", m.group())
        if 13 <= len(digits) <= 19 and luhn_ok(digits):
            found.append("CARD")
            return "[CARD]"
        return m.group()

    text = _CARD.sub(card, text)
    if _IBAN.search(text):
        found.append("IBAN")
        text = _IBAN.sub("[IBAN]", text)
    if _ACCOUNT.search(text):
        found.append("ACCOUNT")
        text = _ACCOUNT.sub(lambda m: m.group(1) + "[ACCOUNT]", text)
    if _EMAIL.search(text):
        found.append("EMAIL")
        text = _EMAIL.sub("[EMAIL]", text)
    return text, found


# ---------------- input: what kind of request is this?
_INJECTION = re.compile(r"ignore (all |any )?(previous|prior|above) (instructions|rules)|you are now|system prompt"
                        r"|reveal (your|the) (instructions|prompt)|pretend (to be|you are)", re.IGNORECASE)
_MONEY_OR_PROFILE = re.compile(r"\b(transfer|send|wire|move)\b.{0,40}\b(to|into)\b|\bpay\b.{0,30}\bto\b"
                               r"|\bchange my (address|phone|email|name)\b|\bincrease my (limit|credit)", re.IGNORECASE)
_ADVICE = re.compile(r"\bshould i (buy|sell|invest|put)\b|\bwhich (stock|share|fund|crypto|coin)s?\b"
                     r"|\bbest (investment|stock|fund|crypto)\b|\bgood investment\b|\binvest (my|in)\b", re.IGNORECASE)
_COMPLAINT = re.compile(r"\b(complain|complaint|unacceptable|ombudsman|disgusted|furious|worst bank)\b", re.IGNORECASE)

ROUTES = ("block_injection", "secure_handoff", "refuse_advice", "escalate_complaint", "answer")


def route(question: str) -> tuple[str, str]:
    """Order matters: attacks first, then actions, advice, complaints; everything else may be answered."""
    if _INJECTION.search(question):
        return "block_injection", "instruction-like text"
    if _MONEY_OR_PROFILE.search(question):
        return "secure_handoff", "moves money or changes account details"
    if _ADVICE.search(question):
        return "refuse_advice", "asks for personal investment advice"
    if _COMPLAINT.search(question):
        return "escalate_complaint", "complaint: a trained officer must handle it"
    return "answer", "policy question"


FIXED = {
    "block_injection": "I can only help with questions about your accounts and cards.",
    "secure_handoff": ("For your security I can't move money or change account details in chat. Please use the "
                       "Payments or Profile screen in the app, or I can connect you to an agent after you verify your identity."),
    "refuse_advice": ("I can't give personal investment advice. A licensed adviser can help: you can book one "
                      "in the app under Invest > Talk to an adviser."),
    "escalate_complaint": ("I'm sorry about this. I'm passing your complaint to a trained complaints officer now. "
                           "You'll get a reference number and an answer within the bank's complaint timelines."),
}
NO_ANSWER = "I couldn't find this in the bank's policies, so I won't guess. I can connect you to an agent."

# ---------------- output: check the answer before the customer sees it
_ANSWER_ADVICE = re.compile(r"\byou should (buy|sell|invest)\b|\bi recommend (buying|investing)\b"
                            r"|\bguaranteed (return|profit)", re.IGNORECASE)


def check_answer(answer: str, n_sources: int) -> list[str]:
    problems = []
    if _ANSWER_ADVICE.search(answer):
        problems.append("investment advice in the answer")
    if any(luhn_ok(re.sub(r"\D", "", m.group())) for m in _CARD.finditer(answer)):
        problems.append("a card number in the answer")
    cited = {int(n) for n in re.findall(r"\[P(\d+)\]", answer)}
    if not cited:
        problems.append("no policy citation")
    elif any(n < 1 or n > n_sources for n in cited):
        problems.append("cites a source that was not given")
    return problems
