# Latency benchmarking: coordinated omission

Companion code for **[Coordinated Omission: Why Your p99 Latency Is Lying](https://vexpose.blog/)** on vExpose.blog.

A closed-loop load test sends the next request only after the previous one returns. So when the server stalls, the load generator stalls with it — and never sends the requests that *should* have gone out during the freeze. Those omitted requests would have been slow too. Drop them and you report a beautiful p99 for a system that was, for a moment, serving no one.

The fix (Gil Tene's correction): measure each request's latency from the time it was **supposed** to start (its schedule), not the time it actually started.

| File | What it shows |
|------|---------------|
| [`coordinated_omission.py`](./coordinated_omission.py) | One 200 ms stall in an otherwise-fast service. Prints naive vs schedule-corrected percentiles. |

## Run it

```bash
python3 coordinated_omission.py
```

```
percentile   naive (ms)   corrected (ms)
        50          0.2              0.2
        90          0.2              0.2
        99          0.2            120.0
      99.9          0.2            192.0
```

Same system, same stall. The naive p99 says 0.2 ms; the honest p99 is 120 ms — a 600× understatement. The average survives; the tail is where the lie lives.

> Illustrative simulation with fixed parameters — the point is the *mechanism* and the gap, not the exact milliseconds. Real fixes: use an open-loop / constant-throughput generator (wrk2, or `fio` with a rate cap), or a tool that corrects for coordinated omission (HdrHistogram-based).
