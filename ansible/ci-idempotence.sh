#!/usr/bin/env bash
# Idempotency regression gate — the second run must report zero changed tasks.
# Companion to: Your Ansible Playbook Says 'changed' Every Run. It's Lying.
#
# A playbook that isn't green on the second run doesn't converge, and one that
# doesn't converge can't be trusted to tell you the truth about your fleet.
# Wire this into CI.
set -euo pipefail

PLAYBOOK="${1:-site.yml}"

# 1) Converge.
ansible-playbook "$PLAYBOOK"

# 2) Run again and fail the build if ANY task reports changed.
#    We parse the recap: "changed=N". Any N>0 on the second pass is a failure.
OUT="$(ansible-playbook "$PLAYBOOK" 2>&1)"
echo "$OUT"

if echo "$OUT" | grep -qE 'changed=[1-9]'; then
  echo "IDEMPOTENCY FAILURE: second run reported changed tasks." >&2
  exit 1
fi
echo "Idempotent: second run was all ok."
