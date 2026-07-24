# vexpose-labs

Runnable code and reference material behind the posts on **[vExpose.blog](https://vexpose.blog)** — *the wiring behind the strategy: reference architectures, real code, real numbers.*

The premise of the blog is simple: state the call a technology leader has to make, then prove it in code, architecture, and benchmarks. This repo is the "prove it" half — every folder maps to a post and holds the code you can actually run.

## Index

| Folder | Post | What's inside |
|--------|------|---------------|
| [`agentic-itsm/`](./agentic-itsm) | [A Reference Architecture for Agentic ITSM](https://vexpose.blog/2026/07/16/agentic-itsm-reference-architecture/) | The deterministic policy gate, a scoped ServiceNow adapter, and least-privilege IaC |
| [`storage-benchmarking/`](./storage-benchmarking) | [The Benchmark Trap](https://vexpose.blog/the-benchmark-trap/) | An honest `fio` job for enterprise storage |
| [`rag/`](./rag) | [A Reference Architecture for Enterprise RAG](https://vexpose.blog/) | Grounded retrieval: hybrid search, reranking, a citation guard, and a faithfulness eval |
| [`servicenow-pagination/`](./servicenow-pagination) | [The ServiceNow REST pagination gotcha](https://vexpose.blog/) | Why offset pagination silently drops records — and the `sys_id` cursor fix |
| [`terraform/`](./terraform) | [The Terraform Gotcha That Destroys the Resource You Meant to Keep](https://vexpose.blog/) | The `count` trap, the `for_each` fix, and a no-downtime state migration |
| [`kubernetes/`](./kubernetes) | [The Readiness Probe That Turned a Deploy Into an Outage](https://vexpose.blog/) | Shallow readiness + startupProbe + `maxUnavailable: 0` vs the rollout death spiral |
| [`pgvector/`](./pgvector) | [Your pgvector Search Gets Slower as You Add Data](https://vexpose.blog/) | IVFFlat `lists`/`probes` tuning and a recall@k regression gate |
| [`inference/`](./inference) | [The Inference Bill Is a Memory-Bandwidth Problem](https://vexpose.blog/) | A bandwidth-bound token-cost calculator: decode speed from arithmetic |
| [`ansible/`](./ansible) | [Your Ansible Playbook Says 'changed' Every Run. It's Lying.](https://vexpose.blog/) | Idempotency fixes and a CI gate that fails on a non-converging second run |
| [`iac-guardrails/`](./iac-guardrails) | [Operating DNA, Not Templates](https://vexpose.blog/) | A paved-road module + OPA/Conftest policy that blocks non-compliant merges |
| [`latency-benchmarking/`](./latency-benchmarking) | [Coordinated Omission: Why Your p99 Latency Is Lying](https://vexpose.blog/) | A closed-loop stall demo: naive vs schedule-corrected percentiles |

## Principle

> AI fails in the operating model, not the model. The tool is not the transformation.

The code here is deliberately boring where it needs to be — the guardrail layers are plain, auditable code, not magic.

## License

[MIT](./LICENSE) — use it, adapt it, ship it.
