---
policy_id: BNK-GR
product: Customer support assistant (fictional bank)
version: 2.0.0
status: active
effective_date: 2026-11-23
review_cycle: quarterly, and after every complaint-ombudsman case linked to the assistant
owners:
  business: Head of Digital Servicing (fictional)
  risk_compliance: Conduct Risk Officer (fictional)
  engineering: Assistant platform lead (fictional)
  on_call: Digital support on-call
risk_tier: high
---

# Bank Support Assistant: Guardrail Policy

## 1. Purpose and scope

**Business outcome:** answer fee, card and account-policy questions instantly with a citation, deflect ≥ 30% of simple calls, and keep **zero** advice or money-movement incidents.

**Users:** authenticated retail customers.

**In scope:** fees, card loss or block steps, dispute time limits, account policies.

**Out of scope. The assistant MUST NEVER:**
- give personal investment advice
- move money, add payees or change contact details in chat
- handle a complaint itself (that is a regulated process)
- echo a card or account number back

## 2. Input rules (in this order. Order matters: attacks first)

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| BNK-IN-001 | MUST redact card numbers (Luhn-checked), IBANs, account numbers and emails before the model, logs or the eval file | `bank_guard.redact_pii` | redact, continue | `pii_card_01` (real v1 bug: spaced card digits leaked; fixed in v2) | Eng |
| BNK-IN-002 | MUST block instruction-like text | `route` → `block_injection` | `T-BNK-INJ` | `inj_01` | Eng |
| BNK-IN-003 | MUST NOT move money or change profile details in chat | `route` → `secure_handoff` | `T-BNK-SECURE` | `money_01` | Fraud & Payments |
| BNK-IN-004 | MUST refuse personal investment advice | `route` → `refuse_advice` | `T-BNK-ADVICE` | `advice_01` | Conduct Risk |
| BNK-IN-005 | MUST send complaints to a human complaints officer | `route` → `escalate_complaint` | `T-BNK-COMPLAINT` | `complaint_01` | Complaints |

## 3. Data and retrieval rules

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| BNK-DATA-001 | MUST answer only from the current published fee schedule and policies | ingestion | reject doc | `ingest_01` | Product Owner |
| BNK-DATA-002 | Retrieval MUST be hybrid (BM25 + embeddings, RRF) so customer words match policy words ("overseas" ↔ "abroad") | `assistant.retrieve` | — | `abroad_01` (real v1 failure) | Eng |
| BNK-DATA-003 | A retrieval change MUST NOT ship on dev-set results alone | release gate | block | held-out set (real: v2 scores 18/18 dev but 5/8 held-out) | Eng + Risk |

## 4. Output rules

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| BNK-OUT-001 | MUST cite at least one `[P#]` | `check_answer` → "no policy citation" | `T-BNK-NOANSWER` | `cite_01` | Eng |
| BNK-OUT-002 | MUST NOT cite a source number that was not given | `check_answer` → "cites a source that was not given" | `T-BNK-NOANSWER` | `cite_02` | Eng |
| BNK-OUT-003 | MUST NOT contain investment-advice phrasing ("you should buy", "guaranteed return") | `check_answer` | block + log | `out_advice_01` | Conduct Risk |
| BNK-OUT-004 | MUST NOT contain a valid card number | `check_answer` (Luhn) | block + log | `out_card_01` | Eng |
| BNK-OUT-005 | MUST NOT invent amounts or assume the customer's balance | eval grader | block release | `amount_01` (real: invented "$" and an assumed balance) | Product |

## 5. Action and tool rules

| ID | Rule | Enforced by | On violation | Owner |
|---|---|---|---|---|
| BNK-ACT-001 | The assistant has **no** write tools. Payments and profile changes happen only in authenticated app screens | architecture (no tool exists) | — | Eng |
| BNK-ACT-002 | Handoff to an agent MUST happen after identity verification and carry the redacted transcript | contact-centre integration | — | Servicing |

## 6. Human-in-the-loop

| Situation | Who | SLA | Channel |
|---|---|---|---|
| Complaint | Complaints officer | acknowledge same day; resolve within the regulatory timeline | complaints queue with a reference number |
| Investment question | Licensed adviser | booked appointment | Invest > Talk to an adviser |
| Money movement or profile change | Customer self-serve, or a verified agent | — | Payments / Profile screens |
| No source found | Support agent | live chat queue | handoff |

## 7. Response templates (copied from `bank_guard.FIXED`)

| Template ID | Text |
|---|---|
| T-BNK-INJ | "I can only help with questions about your accounts and cards." |
| T-BNK-SECURE | "For your security I can't move money or change account details in chat. Please use the Payments or Profile screen in the app, or I can connect you to an agent after you verify your identity." |
| T-BNK-ADVICE | "I can't give personal investment advice. A licensed adviser can help: you can book one in the app under Invest > Talk to an adviser." |
| T-BNK-COMPLAINT | "I'm sorry about this. I'm passing your complaint to a trained complaints officer now. You'll get a reference number and an answer within the bank's complaint timelines." |
| T-BNK-NOANSWER | "I couldn't find this in the bank's policies, so I won't guess. I can connect you to an agent." |

## 8. Logging, audit and privacy

- MUST log only the **redacted** question, the route, the rule IDs, the cited `[P#]`, the model and prompt version, and the latency.
- MUST NOT store full card or account numbers anywhere in the AI pipeline.
- Retention and access follow the bank's record-keeping policy (set by Compliance).

## 9. Evals and release gate

| Suite | Size | Pass bar | Blocks release? | Last real run |
|---|---|---|---|---|
| Rule and route cases | 18 | 18/18 | yes | v1 17/18 → v2 18/18 |
| **Held-out wordings (never tuned on)** | 8 | ≥ 7/8 | yes | v2 **5/8, so this blocks release** |
| Red-team and injection | ≥ 20 | 100% blocked | yes | — |

> The real lesson: v2 passed 18/18 because `TOP_K` was raised until the one failing case passed. The held-out set showed this was an overfit. The policy makes the held-out set a release blocker.

## 10. Monitoring and alerts

| Signal | Threshold | Action |
|---|---|---|
| `check_answer` blocks | > 1% of answers / hour | page on-call |
| Complaint route volume | spike > 2× baseline | notify Complaints |
| Unredacted card detected in logs | ≥ 1 | P1 incident, purge logs |
| Handoff rate | > 40% / day | product review (coverage gap) |

## 11. Incident response

1. If customers could be harmed, turn off answering (routes only, no generated answers).
2. Notify Conduct Risk within 24 h if advice or money movement was involved.
3. Write a failing eval case, fix it, and pass both the dev set **and** the held-out set.

## 12. Change log

| Version | Date | Change | Approved by |
|---|---|---|---|
| 1.0.0 | 2026-11-23 | Routes, redaction, output checks (v1 17/18) | Conduct Risk |
| 2.0.0 | 2026-11-23 | Card regex fix, hybrid retrieval, held-out set made a release blocker | Conduct Risk + Eng |

*The bank, its policies and its customers are fictional. Real conduct and complaint rules come from your regulator and compliance team.*
