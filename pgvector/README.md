# pgvector: why search slows at scale (and the setting everyone misses)

Companion code for **[Your pgvector Search Gets Slower as You Add Data](https://vexpose.blog/)** on vExpose.blog.

Without an ANN index, pgvector brute-forces every row — fine at 10k, fatal at 2M. The fix is an index, but two knobs decide everything and both have quietly wrong defaults for a large table: **`lists`** (build time) and **`probes`** (query time).

| File | What it shows |
|------|---------------|
| [`schema.sql`](./schema.sql) | IVFFlat with `lists = 1414` (sqrt of 2M rows) and `probes = 38` (≈ sqrt(lists)); HNSW alternative. Build the index **after** loading data. |
| [`recall_test.py`](./recall_test.py) | Recall@k gate — compares the ANN result against exact brute-force ground truth. Fails when speed came at the cost of missing relevant rows. |

## The rule

Measure **recall, not just latency**. Every time you touch `lists`, `probes`, or the index type, confirm recall held before you celebrate the speed — a fast search that misses a third of the right answers is broken with a good p99.

```bash
python3 recall_test.py   # demo: fails because a relevant row was dropped
```
