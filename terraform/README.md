# Terraform: the count trap (and the for_each fix)

Companion code for **[The Terraform Gotcha That Destroys the Resource You Meant to Keep](https://vexpose.blog/)** on vExpose.blog.

`count` addresses resources by list **position**, so removing/inserting anywhere but the end shifts every later index — and Terraform destroy-and-recreates the survivors to "fix" the mismatch. `for_each` keys each resource by a **stable string**, so identity survives list edits.

| File | What it shows |
|------|---------------|
| [`count-trap.tf`](./count-trap.tf) | The trap — identity bound to the index. Delete a middle element and `plan` replaces the survivors. |
| [`for_each-fix.tf`](./for_each-fix.tf) | The fix — identity bound to a key. Delete an entry and only that one is destroyed. |
| [`migrate.sh`](./migrate.sh) | `terraform state mv` from positional → keyed addresses (plus the 1.1+ `moved {}` block form) so migration replaces nothing. |

## Try it

```bash
terraform init
terraform apply            # creates node[0..2]
# delete "web-a" from the nodes list, then:
terraform plan             # see the count version churn the survivors
```

> Uses `null_resource` so it runs with no cloud credentials. The identity behavior is identical for real providers (`aws_instance`, etc.). **Rule: confirm the plan shows zero replacements before you apply.**
