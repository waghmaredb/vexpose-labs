#!/usr/bin/env bash
# Migrate count -> for_each WITHOUT destroying live resources.
# Companion to: The Terraform Gotcha That Destroys the Resource You Meant to Keep
#
# Move each state entry from its positional address to its keyed address, THEN
# swap count for for_each in the config. The final plan must show zero changes.
set -euo pipefail

# 1) Move state entries from index -> key. (node[0] is web-a, [1] web-b, [2] web-c)
terraform state mv 'null_resource.node[0]' 'null_resource.node_keyed["web-a"]'
terraform state mv 'null_resource.node[1]' 'null_resource.node_keyed["web-b"]'
terraform state mv 'null_resource.node[2]' 'null_resource.node_keyed["web-c"]'

# 2) Now switch the config to the for_each version and confirm:
#    terraform plan   # MUST report: No changes. Zero replacements.
echo "State moved. Swap to the for_each config, then run: terraform plan"
echo "If the plan shows ANY replacement, stop and reconcile before apply."

# --- Alternative (Terraform 1.1+): declare the moves as code instead of CLI ---
# moved {
#   from = null_resource.node[0]
#   to   = null_resource.node_keyed["web-a"]
# }
# ...and let `terraform plan` do the reshuffle. Same rule: zero replacements.
