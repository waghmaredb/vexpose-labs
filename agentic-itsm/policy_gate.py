"""
Deterministic policy gate for an agentic ITSM system — "the seam".

Companion code for:
  https://vexpose.blog/2026/07/16/agentic-itsm-reference-architecture/

Every action an agent proposes passes through evaluate() BEFORE it can touch
ServiceNow. This layer is plain, auditable code — not a model — because
"what is this agent allowed to do" is a decision you must be able to read,
test, and diff in git.
"""

from dataclasses import dataclass
from enum import Enum


class Decision(Enum):
    ALLOW = "allow"
    REQUIRE_APPROVAL = "require_approval"
    DENY = "deny"


@dataclass
class ProposedAction:
    name: str            # e.g. "restart_service", "reassign", "add_work_note"
    target_ci: str       # configuration item the action touches
    params: dict
    confidence: float    # model-reported, treated as a hint, never as truth


# Policy is data you can read, diff in git, and audit — not model output.
POLICY = {
    "add_work_note":   {"max_blast_radius": "none",    "min_confidence": 0.0},
    "reassign":        {"max_blast_radius": "ticket",  "min_confidence": 0.75},
    "restart_service": {"max_blast_radius": "service", "min_confidence": 0.90,
                        "require_approval_for": ["prod"]},
    # default-deny: anything not listed cannot run
}


def evaluate(action: ProposedAction, ci_env: str) -> Decision:
    rule = POLICY.get(action.name)
    if rule is None:
        return Decision.DENY                       # default deny — the safe default
    if action.confidence < rule["min_confidence"]:
        return Decision.REQUIRE_APPROVAL
    if ci_env in rule.get("require_approval_for", []):
        return Decision.REQUIRE_APPROVAL
    return Decision.ALLOW


if __name__ == "__main__":
    examples = [
        (ProposedAction("add_work_note", "CI-1001", {"note": "triaged"}, 0.55), "prod"),
        (ProposedAction("reassign", "CI-1001", {"group": "network"}, 0.62), "dev"),
        (ProposedAction("reassign", "CI-1001", {"group": "network"}, 0.88), "dev"),
        (ProposedAction("restart_service", "CI-2002", {}, 0.97), "prod"),
        (ProposedAction("delete_everything", "CI-9999", {}, 0.99), "dev"),
    ]
    for action, env in examples:
        print(f"{action.name:<18} conf={action.confidence:<4} env={env:<5} -> "
              f"{evaluate(action, env).value}")
