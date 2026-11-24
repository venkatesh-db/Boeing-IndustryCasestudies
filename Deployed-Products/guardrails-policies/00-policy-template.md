---
policy_id: <PRODUCT>-GR
product: <product name>
version: 1.0.0
status: draft            # draft | reviewed | active | retired
effective_date: YYYY-MM-DD
review_cycle: quarterly
owners:
  business: <name, role>
  risk_compliance: <name, role>
  engineering: <name, role>
  on_call: <team / rotation>
risk_tier: high          # low | medium | high (drives eval depth and approval)
---

# <Product> — Guardrail Policy

## 1. Purpose and scope

**Business outcome:** <what must improve, with a number>
**Users:** <who uses it, with roles>
**In scope:** <the jobs it does>
**Out of scope — MUST NEVER:** <the lines it never crosses, one per line>

## 2. Definitions

| Term | Meaning in this policy |
|---|---|
| Grounded answer | Every factual sentence cites an approved source shown to the model |
| Refusal | A polite no **plus** a next step (link, handoff, form) |
| Handoff | Transfer to a human with the conversation and reason attached |

## 3. Input rules (before the model)

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| XX-IN-001 | MUST block prompt-injection patterns in user text | `<function>` | refuse + log `injection_blocked` | `inj_direct_01` | Eng |
| XX-IN-002 | MUST redact <sensitive data types> before logging or model call | `<function>` | redact, continue | `pii_01` | Eng |
| XX-IN-003 | MUST route <forbidden intent> away from the model | `<router>` | fixed reply + next step | `route_01` | Risk |

## 4. Data and retrieval rules

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| XX-DATA-001 | MUST only index approved, current documents | ingestion pipeline | reject document | `ingest_01` | Content owner |
| XX-DATA-002 | MUST filter retrieval by user role / entitlement before search | `<retriever>` | drop chunk | `acl_01` | Eng |
| XX-DATA-003 | MUST treat retrieved text as data, never as instructions | `sanitize_chunk` | strip + warn | `inj_indirect_01` | Eng |

## 5. Output rules (after the model, before the user)

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| XX-OUT-001 | MUST cite at least one source that was actually given | `check_answer` | replace with no-answer reply | `cite_01` | Eng |
| XX-OUT-002 | MUST NOT contain <forbidden content> | `check_answer` | block + log | `out_01` | Risk |
| XX-OUT-003 | If no source supports the answer, MUST say so and hand off | `NO_ANSWER` | — | `noans_01` | Product |

## 6. Action and tool rules

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| XX-ACT-001 | Agent MAY ONLY call tools on the allowlist | `check_tool` | block + audit | `tool_01` | Eng |
| XX-ACT-002 | Any write action MUST be a draft until a human approves | approval API | reject | `approve_01` | Business |
| XX-ACT-003 | Safe mode MUST make the system read-only with one switch | env flag | — | `safe_01` | On-call |

## 7. Human-in-the-loop

| Situation | Who | SLA | Channel |
|---|---|---|---|
| <decision AI may not make> | <role> | <time> | <queue> |

## 8. Response templates (fixed, reviewed text — not generated)

| Template ID | Used when | Text |
|---|---|---|
| T-REFUSE-01 | forbidden request | "I can't help with that here. <next step>." |
| T-NOANSWER-01 | no source | "I couldn't find this in <approved sources>, so I won't guess. <handoff>." |

## 9. Logging, audit and privacy

- MUST log: time, user role, rule IDs triggered, sources cited, model + prompt version, latency.
- MUST NOT log: raw sensitive data (log the redacted text only).
- Retention: <N days>, access: <roles>.

## 10. Evals and release gate

| Suite | Size | Pass bar | Blocks release? |
|---|---|---|---|
| Rule tests (one per rule ID) | <n> | 100% | yes |
| Grounded-answer set | <n> | ≥ <x>% | yes |
| **Held-out set (never tuned on)** | <n> | ≥ <x>% | yes |
| Red-team / injection set | <n> | 100% blocked | yes |

## 11. Monitoring and alerts

| Signal | Threshold | Action |
|---|---|---|
| Refusal rate | > <x>% / hour | page on-call |
| No-citation answers | > 0 | page on-call |
| Injection blocks | spike > <x>× baseline | security review |
| Thumbs-down rate | > <x>% / day | product review |

## 12. Incident response

1. Turn on **safe mode** (`XX-ACT-003`) if users could be harmed.
2. Capture the conversation, rule IDs, sources, versions.
3. Add a failing eval case **before** fixing.
4. Fix, prove on dev **and held-out**, release, close incident.

## 13. Change log

| Version | Date | Change | Approved by |
|---|---|---|---|
| 1.0.0 | YYYY-MM-DD | First release | <names> |
