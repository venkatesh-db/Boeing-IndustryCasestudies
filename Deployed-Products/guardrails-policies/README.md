# Guardrail Policies — Production Format

Guardrails in production are **policy as code**: written rules, owned by named people, versioned like software, enforced by code (not by the prompt), and proven by evals before every release.

> A prompt is a *request* to the model. A guardrail is a *control* the model cannot talk its way past.

## Files in this folder

| File | What it is |
|---|---|
| [00-policy-template.md](00-policy-template.md) | The blank, reusable format. Copy it for every new AI product. |
| [aviation-maintenance-assistant.md](aviation-maintenance-assistant.md) | AeroGuard (course project). Rules mapped to real code in `aeroguard/aeroguard/security.py` and `rag/guardrails.py`. |
| [banking-support-assistant.md](banking-support-assistant.md) | Fictional bank. Rules mapped to real code in `Eval-Guardrails/banking_lab/bank_guard.py`. |
| [health-plan-assistant.md](health-plan-assistant.md) | Fictional Harbor Health. Rules born from the real wrong-hospital failure in `Deployed-Products/labs`. |
| [release-gate-checklist.md](release-gate-checklist.md) | The sign-off sheet a release must pass before it goes live. |

## The 7 layers every policy file covers

1. **Scope**: what the assistant is for and, more importantly, what it is never for.
2. **Input rules**: what is blocked, rerouted or redacted *before* the model sees it.
3. **Data and retrieval rules**: which documents may be used, by whom, which version.
4. **Output rules**: what is checked *after* the model answers, before the user sees it.
5. **Action and tool rules**: what the system may *do*, not just say.
6. **Human-in-the-loop**: who approves what, and when the AI hands over.
7. **Monitoring, audit and incidents**: how you know it still works and what happens when it does not.

## How a rule is written (one rule = one row)

```
ID | Rule (MUST / MUST NOT) | Enforced by (code, not prompt) | On violation | Eval case | Owner
```

- **ID** is stable forever (`BNK-IN-003`). Evals, logs and incident reports reference it.
- **MUST / MUST NOT** only. "Should try to" is not a rule.
- **Enforced by** names the actual function or service. If the answer is "the system prompt", it is not enforced.
- **Eval case** proves the rule works. A rule without a test is a wish.

## Lifecycle

`draft → reviewed (Risk + Legal + Product + Eng) → enforced in code → eval green → released → monitored → incident → new rule/test`

All organisations, people and data in these files are fictional training samples. Real regulatory obligations must come from your own compliance and legal teams.
