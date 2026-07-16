# Agentic ITSM — reference code

Companion code for **[A Reference Architecture for Agentic ITSM: Wiring GenAI into ServiceNow Without Losing Control](https://vexpose.blog/2026/07/16/agentic-itsm-reference-architecture/)**.

The post's thesis: the moment a GenAI agent can *act* in your system of record, safety is an architecture problem, not a model problem. The durable advantage is the **seam** — a deterministic, auditable, least-privilege layer between what the agent decides and what your systems do.

## Files

| File | Role |
|------|------|
| [`policy_gate.py`](./policy_gate.py) | The seam. A deterministic policy check every proposed action passes through — default-deny, blast-radius classification, confidence-as-a-hint. |
| [`servicenow_adapter.py`](./servicenow_adapter.py) | A thin, scoped adapter exposing only whitelisted ServiceNow operations, backed by a least-privilege account. |
| [`provision_agent_account.yml`](./provision_agent_account.yml) | Ansible to provision the integration account with *only* the roles it needs — permissions as a reviewed diff, not tribal knowledge. |

## Run the gate

```bash
python3 policy_gate.py
```

It runs a few example decisions (allow / require-approval / deny) against the sample policy so you can see the seam in action.

> Confidence is a hint, never a gate on its own. Blast radius is explicit. Anything the policy doesn't know about cannot run.
