# Policy-as-code: an un-encrypted bucket never gets past CI. Nothing to forget.
# Companion to: Operating DNA, Not Templates: What IaC Actually Encodes
#
# Modules make the right thing easy; policy makes the wrong thing impossible to
# merge — enforced on every plan, including the ones written by someone who has
# never read the wiki. Run against a terraform plan JSON with conftest/OPA:
#
#   terraform show -json plan.tfplan > plan.json
#   conftest test plan.json --policy policy/
package terraform.storage

deny[msg] {
  r := input.resource_changes[_]
  r.type == "aws_s3_bucket"
  not encrypted(r.address)
  msg := sprintf("bucket %v must be encrypted - org policy STO-014", [r.address])
}

# A bucket is considered encrypted if a matching SSE-configuration resource is
# being created/kept in the same plan for that bucket.
encrypted(bucket_addr) {
  enc := input.resource_changes[_]
  enc.type == "aws_s3_bucket_server_side_encryption_configuration"
  contains(enc.address, trim_prefix(bucket_addr, "aws_s3_bucket."))
}
