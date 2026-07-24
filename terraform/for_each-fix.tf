# The fix — identity is a stable KEY, not a position.
# Companion to: The Terraform Gotcha That Destroys the Resource You Meant to Keep
#
# for_each keys each instance by a string you control. Delete one entry and only
# that one is destroyed; the rest keep their identity because it was never their
# position. Addresses become null_resource.node["web-b"], etc.
#
# This file is an ALTERNATIVE to count-trap.tf — use one or the other in a real
# root module (both declare a resource named "node"). Kept separate here so each
# reads cleanly against the post.

variable "nodes_fixed" {
  type    = set(string)
  default = ["web-a", "web-b", "web-c"]
}

resource "null_resource" "node_keyed" {
  for_each = var.nodes_fixed

  triggers = {
    name = each.key
  }
}

output "for_each_addresses" {
  value = [for n in var.nodes_fixed : "null_resource.node_keyed[\"${n}\"]"]
}
