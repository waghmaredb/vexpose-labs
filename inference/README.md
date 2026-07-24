# Inference: the bill is a memory-bandwidth problem

Companion code for **[The Inference Bill Is a Memory-Bandwidth Problem](https://vexpose.blog/)** on vExpose.blog.

LLM **decode** generates one token at a time, and each token requires reading the entire model's weights out of HBM again. So single-stream decode speed is set by **memory bandwidth**, not TFLOPs — and you can estimate the ceiling with arithmetic, no benchmark required.

## Run it

```bash
python3 token_cost.py
```

```
model      GB/token   TB/s   ms/token    tok/s
7B  FP16       14.0    2.0        7.0      143
13B FP16       26.0    2.0       13.0       77
70B FP16      140.0    2.0       70.0       14
70B FP8        70.0    2.0       35.0       29
```

These are ceilings from bandwidth alone (real systems land lower). The tell: going FP16 → FP8 **halves bytes read per token and roughly doubles throughput** — you cut the bottleneck, you didn't add compute. Change `HBM` in the script to your accelerator's real bandwidth.

> Batching amortizes the weight read across many in-flight sequences (continuous batching) until the **KV cache** exhausts HBM capacity — at which point you're capacity-bound instead of bandwidth-bound. Spec accelerators by bandwidth and capacity, not headline TFLOPs.
