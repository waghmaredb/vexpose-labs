"""
Measure RECALL, not just latency, whenever you touch lists / probes / index type.

Companion code for:
  https://vexpose.blog/  (Your pgvector Search Gets Slower as You Add Data)

A vector search that got 10x faster by missing a third of the right answers isn't
faster — it's broken with a good p99. This harness compares an APPROXIMATE query
(your tuned ANN index) against the EXACT brute-force ground truth for a fixed set
of probe queries, and reports recall@k. Wire it into CI as a regression gate.

Pseudo-DB here keeps it dependency-free; swap `exact_topk` / `ann_topk` for real
psycopg queries (ORDER BY embedding <=> $1 LIMIT k, with/without the index).
"""

from dataclasses import dataclass


@dataclass
class QueryResult:
    query_id: str
    exact_ids: list[str]   # ground truth: brute-force top-k (SET enable_indexscan=off)
    ann_ids: list[str]     # ANN result: top-k using the index at current `probes`


def recall_at_k(r: QueryResult, k: int) -> float:
    truth = set(r.exact_ids[:k])
    got = set(r.ann_ids[:k])
    return len(truth & got) / k if k else 0.0


def evaluate(results: list[QueryResult], k: int = 10, floor: float = 0.95) -> dict:
    per = [recall_at_k(r, k) for r in results]
    mean = sum(per) / len(per) if per else 0.0
    regressions = [r.query_id for r, rc in zip(results, per) if rc < floor]
    return {
        "mean_recall_at_k": round(mean, 3),
        "k": k,
        "floor": floor,
        "passed": not regressions,
        "regressions": regressions,
    }


if __name__ == "__main__":
    demo = [
        QueryResult("q1", ["d1", "d2", "d3"], ["d1", "d2", "d3"]),          # perfect
        QueryResult("q2", ["d4", "d5", "d6"], ["d4", "d9", "d6"]),          # missed d5
    ]
    from pprint import pprint
    pprint(evaluate(demo, k=3, floor=0.95))
    # -> passed: False, because q2 dropped a relevant result. Raise `probes` and re-run.
