# IaC guardrails: operating DNA, not templates

Companion code for **[Operating DNA, Not Templates: What Infrastructure as Code Actually Encodes](https://vexpose.blog/)** on vExpose.blog.

Speed is what the tool sells. What IaC actually encodes — done well — is your organization's **operating DNA**: the accumulated judgment about how *you* run infrastructure, made explicit, versioned, and enforced. Two layers turn "scripts that build things" into "judgment that governs things."

| File | Layer |
|------|-------|
| [`secure-bucket.tf`](./secure-bucket.tf) | **Modules encode the paved road** — encryption, versioning, public-access-block and the cost-center tag are non-optional defaults. The compliant way is the easy way. |
| [`policy/bucket.rego`](./policy/bucket.rego) | **Policy-as-code makes guardrails non-negotiable** — an un-encrypted bucket never merges, enforced on every plan via OPA/Conftest. |

## The diagnostic

Two orgs can have identical Terraform and completely different operating DNA. Ask: can a new hire provision a compliant environment without asking anyone? What stops a non-compliant change from merging — a reviewer who happens to notice, or a policy in CI? Where does the reasoning live — commit history, or someone's memory?

```bash
terraform show -json plan.tfplan > plan.json
conftest test plan.json --policy policy/
```
