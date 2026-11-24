---
policy_id: HLT-GR
product: Harbor Health member assistant (fictional)
version: 1.1.0
status: active
effective_date: 2026-11-23
review_cycle: before every plan year (1 January) and after every wrong-coverage complaint
owners:
  business: Member Services Director (fictional)
  risk_compliance: Privacy & Compliance Officer (fictional)
  engineering: Member assistant platform lead (fictional)
  on_call: Member services on-call
risk_tier: high
---

# Harbor Health Member Assistant: Guardrail Policy

## 1. Purpose and scope

**Business outcome:** members get correct in-network answers for **their own plan and year**, with a citation, and **zero** wrong-coverage answers that lead to a surprise bill.

**Users:** authenticated members (their plan and year come from the member record, **not** from the chat).

**In scope:** which hospitals and providers are in-network, which documents explain coverage.

**Out of scope. The assistant MUST NEVER:**
- guarantee that a claim will be paid
- give medical advice or choose a treatment
- answer from another plan's or another year's document
- show one member's data to another

## 2. Input rules

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| HLT-IN-001 | MUST take plan and year from the authenticated member record. A plan named in the chat MUST NOT override it | session context | ignore chat value | `plan_spoof_01` "I'm on PLUS, is Mercy covered?" | Eng |
| HLT-IN-002 | MUST redact member ID, date of birth and diagnosis text before logging | redaction service | redact | `pii_01` | Privacy |
| HLT-IN-003 | MUST route medical-advice questions to the nurse line | intent router | `T-HLT-MEDICAL` | `medical_01` | Clinical |
| HLT-IN-004 | MUST route "will my claim be paid?" to pre-authorisation | intent router | `T-HLT-PREAUTH` | `claim_01` | Claims |

## 3. Data and retrieval rules (born from the real wrong-hospital failure)

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| HLT-DATA-001 | Every document MUST carry `doc_id`, `plan`, `year` front matter. Documents without them MUST NOT be indexed | ingestion | reject | `ingest_01` | Network Ops |
| HLT-DATA-002 | Retrieval MUST filter on `plan == member.plan AND year == member.year` **before** BM25 or vector search | `search(q, plan=, year=)` in `labs/overlap_experiment.py` | — | `mercy_01` (real: no filter → "in-network" for a STANDARD 2026 member; plan+year filter → correct "out-of-network") | Eng |
| HLT-DATA-003 | At plan-year rollover, the previous year MUST be marked superseded the same day the new year goes live | release runbook | block go-live | `rollover_01` | Network Ops |
| HLT-DATA-004 | Duplicate lines across documents MUST be de-duplicated before citation | post-retrieval dedupe | merge | `dup_01` | Eng |

## 4. Output rules

| ID | Rule | Enforced by | On violation | Eval case | Owner |
|---|---|---|---|---|---|
| HLT-OUT-001 | MUST cite `[P#]` lines, and every cited line MUST match the member's plan and year | output checker | `T-HLT-NOANSWER` | `cite_plan_01` | Eng |
| HLT-OUT-002 | MUST name the plan and year in the answer ("For your STANDARD 2026 plan…") | template | regenerate | `plan_named_01` | Product |
| HLT-OUT-003 | MUST NOT use the words "guaranteed", "will be paid" or "covered 100%" | output checker | block | `guarantee_01` | Compliance |
| HLT-OUT-004 | Where in-network status changed since the last year, MUST mention the change | change table lookup | add note | `change_01` (Mercy: in-network until 31 Dec 2025) | Product |

## 5. Action and tool rules

| ID | Rule | Enforced by | Owner |
|---|---|---|---|
| HLT-ACT-001 | Read-only. No claim submission, no plan change in chat | no write tools exist | Eng |
| HLT-ACT-002 | Kill switch: answer with the provider-directory link only | feature flag | On-call |

## 6. Human-in-the-loop

| Situation | Who | Channel |
|---|---|---|
| Coverage dispute or surprise bill | Member services specialist | callback within 1 business day |
| Pre-authorisation | Utilisation management | pre-auth form |
| Medical question | Nurse line | phone |

## 7. Response templates

| Template ID | Text |
|---|---|
| T-HLT-NOANSWER | "I couldn't confirm this for your plan and year, so I won't guess. Please check the provider directory or call Member Services." |
| T-HLT-MEDICAL | "I can't give medical advice. Our nurse line is open 24/7." |
| T-HLT-PREAUTH | "In-network status doesn't guarantee payment. Please request pre-authorisation for planned procedures." |

## 8. Evals and release gate

| Suite | Pass bar | Blocks release? |
|---|---|---|
| Cross-plan trap set (the same hospital, different status per plan and year) | 100% | yes |
| Plan-year rollover set | 100% | yes, before 1 January |
| Held-out member wordings | ≥ 90% | yes |

## 9. Monitoring and alerts

| Signal | Threshold | Action |
|---|---|---|
| Cited line from a different plan or year | ≥ 1 | P1, kill switch |
| Coverage complaints that mention the assistant | ≥ 1 / week | incident review |

## 10. Change log

| Version | Date | Change | Approved by |
|---|---|---|---|
| 1.0.0 | 2026-11-23 | First release | Compliance |
| 1.1.0 | 2026-11-23 | Plan+year pre-filter after the real Mercy Heart wrong-hospital answer | Compliance + Eng |

*Harbor Health, its plans, hospitals and members are fictional. Real coverage, privacy (e.g. HIPAA) and appeal rules come from your compliance and legal teams.*
