# Storage benchmarking — an honest fio job

Companion code for **[The Benchmark Trap: Why Your Storage Numbers Lie — and How to Get Honest Ones](https://vexpose.blog/the-benchmark-trap/)**.

Peak IOPS on a datasheet is a real measurement — of a workload that looks nothing like yours. [`db-like.fio`](./db-like.fio) is a starting point that measures the storage, not the cache, and reports the tail latency you'll actually feel.

## Run it

```bash
# WARNING: reads/writes a 200g test file — point --directory at scratch space.
fio db-like.fio --directory=/mnt/scratch
```

## Every knob is a decision about honesty

- `direct=1` — bypass the page cache, so you measure storage, not memory.
- `ramp_time=60` — throw away the artificially fast warm-up; measure at steady state.
- `size=200g` — larger than the array's cache, so you force cache misses.
- `bs=16k`, `rwmixread=70` — your real block size and read/write mix, not 4k reads.
- `percentile_list=99:99.9` — report the tail, not just the average. This is the one most people skip.

> Don't ask "how fast is it." Ask "how fast is it, running my workload, at my latency budget, at steady state, averaged over five runs."
