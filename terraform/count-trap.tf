# The count trap — identity is the list POSITION.
# Companion to: The Terraform Gotcha That Destroys the Resource You Meant to Keep
#   https://vexpose.blog/
#
# Remove or insert an element anywhere but the end of the list and every index
# after it shifts. Terraform reads that as "the thing at index N is a different
# thing now" and destroy-and-recreates it. Try it:
#
#   terraform init
#   terraform apply                    # creates node[0], node[1], node[2]
#   # now delete "web-a" from the list below and run:
#   terraform plan                     # watch it destroy/recreate the survivors

variable "nodes" {
  type    = list(string)
  default = ["web-a", "web-b", "web-c"]
}

resource "null_resource" "node" {
  count = length(var.nodes)

  # The index IS the identity. var.nodes[count.index] just feeds a trigger so a
  # change in mapping forces replacement — the same way a real resource's
  # positionally-bound attributes would.
  triggers = {
    name = var.nodes[count.index]
  }
}

output "count_addresses" {
  value = [for i, n in var.nodes : "null_resource.node[${i}] => ${n}"]
}
