# vexpose-labs

Runnable code and reference material behind the posts on **[vExpose.blog](https://vexpose.blog)** — *the wiring behind the strategy: reference architectures, real code, real numbers.*

The premise of the blog is simple: state the call a technology leader has to make, then prove it in code, architecture, and benchmarks. This repo is the "prove it" half — every folder maps to a post and holds the code you can actually run.

## Index

| Folder | Post | What's inside |
|--------|------|---------------|
| [`agentic-itsm/`](./agentic-itsm) | [A Reference Architecture for Agentic ITSM](https://vexpose.blog/2026/07/16/agentic-itsm-reference-architecture/) | The deterministic policy gate, a scoped ServiceNow adapter, and least-privilege IaC |
| [`storage-benchmarking/`](./storage-benchmarking) | [The Benchmark Trap](https://vexpose.blog/the-benchmark-trap/) | An honest `fio` job for enterprise storage |

## Principle

> AI fails in the operating model, not the model. The tool is not the transformation.

The code here is deliberately boring where it needs to be — the guardrail layers are plain, auditable code, not magic.

## License

[MIT](./LICENSE) — use it, adapt it, ship it.
