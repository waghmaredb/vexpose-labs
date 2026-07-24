# A module that encodes operating DNA: the compliant config is the DEFAULT.
# Companion to: Operating DNA, Not Templates: What IaC Actually Encodes
#   https://vexpose.blog/
#
# A good module isn't a thin wrapper over a resource — it's an opinion. Encryption,
# logging, versioning, public-access-block and the cost-center tag are baked in and
# NON-OPTIONAL, so the easy way to provision is also the compliant way. There is no
# "encryption = false" knob to get wrong.

variable "name" {
  type        = string
  description = "Bucket name."
}

variable "cost_center" {
  type        = string
  description = "Required for cost allocation — no bucket without an owner."
}

resource "aws_s3_bucket" "this" {
  bucket = var.name
  tags   = { cost-center = var.cost_center, managed-by = "secure-bucket" }
}

# Enforced inside the module — callers can't turn these off.
resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" }
  }
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket                  = aws_s3_bucket.this.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
