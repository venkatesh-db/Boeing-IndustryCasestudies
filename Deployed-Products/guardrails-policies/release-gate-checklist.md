# Release Gate Checklist: GenAI Guardrails

Copy this sheet into every release ticket. **Any unchecked "blocker" item means no release.**

**Product:** ____________ **Policy ID & version:** ____________ **Release:** ____________ **Date:** ____________

## A. Policy (blockers)
- [ ] Policy file is `status: active`, reviewed by Business, Risk/Compliance and Engineering
- [ ] Every MUST / MUST NOT rule has an **Enforced by** that is code, not the prompt
- [ ] Every rule ID has at least one eval case
- [ ] Out-of-scope list is reviewed and the refusal templates are approved word-for-word

## B. Data (blockers)
- [ ] Only approved, current documents are indexed; superseded versions are excluded
- [ ] Every chunk has metadata (owner, version or year, access label, plan or tenant where relevant)
- [ ] Retrieval filters on metadata **before** search
- [ ] De-duplication run; no two documents give conflicting answers for the same scope

## C. Evals (blockers)
- [ ] Rule tests: 100% pass
- [ ] Grounded-answer set: at or above the bar
- [ ] **Held-out set: at or above the bar. Nobody tuned on it.** Results recorded: ____ / ____
- [ ] Red-team and injection set: 100% blocked (direct **and** inside documents)
- [ ] Results are compared with the last release. Any regression is explained.

## D. Actions and humans (blockers)
- [ ] Tool allowlist reviewed; no write tool without human approval
- [ ] Approver roles tested (a non-approver gets 403)
- [ ] Safe mode / kill switch tested in staging in the last 7 days

## E. Operations
- [ ] Audit log captures rule IDs, sources, versions and approvals
- [ ] Logs contain redacted text only (spot-check 20 rows)
- [ ] Alerts are wired and the on-call rotation knows the runbook
- [ ] Rollback plan: the previous model, prompt and index versions can be restored in < 15 min

## Sign-off

| Role | Name | Decision | Date |
|---|---|---|---|
| Business owner | | ☐ Go ☐ No-go | |
| Risk / Compliance | | ☐ Go ☐ No-go | |
| Engineering | | ☐ Go ☐ No-go | |

> **Real example of a correct No-go:** the bank assistant v2 scored 18/18 on its eval set but 5/8 on held-out wordings (bar: 7/8). Item C3 fails, so the release is blocked until retrieval is fixed without tuning on the eval.
