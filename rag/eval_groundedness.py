"""
A minimal groundedness (faithfulness) eval harness for enterprise RAG.

Companion code for:
  https://vexpose.blog/  (A Reference Architecture for Enterprise RAG)

Wiring RAG is a weekend. Knowing whether it's getting better or worse is the
real engineering. This harness scores every answer on two axes that actually
predict trust:

  * groundedness  — is every claim supported by a retrieved chunk?
  * citation_valid — does each cited doc_id actually appear in the context?

Run it on a fixed set of (question, known-good-answer) pairs on every prompt,
model, or index change. A change that doesn't move these numbers is a guess.
"""

from dataclasses import dataclass


@dataclass
class EvalCase:
    question: str
    cited_doc_ids: list[str]     # doc_ids the answer cited
    context_doc_ids: list[str]   # doc_ids actually retrieved
    claims_supported: int        # claims backed by context (from a judge)
    claims_total: int


def score(case: EvalCase) -> dict:
    groundedness = (case.claims_supported / case.claims_total) if case.claims_total else 0.0
    hallucinated_citations = [d for d in case.cited_doc_ids if d not in case.context_doc_ids]
    citation_valid = len(hallucinated_citations) == 0
    return {
        "question": case.question,
        "groundedness": round(groundedness, 3),
        "citation_valid": citation_valid,
        "hallucinated_citations": hallucinated_citations,
    }


def summarize(cases: list[EvalCase], floor: float = 0.9) -> dict:
    rows = [score(c) for c in cases]
    grounded = sum(r["groundedness"] for r in rows) / len(rows)
    clean_citations = sum(1 for r in rows if r["citation_valid"]) / len(rows)
    return {
        "mean_groundedness": round(grounded, 3),
        "citation_pass_rate": round(clean_citations, 3),
        "regressions": [r for r in rows if r["groundedness"] < floor or not r["citation_valid"]],
    }


if __name__ == "__main__":
    demo = [
        EvalCase("What is the SLA?", ["kb-12"], ["kb-12", "kb-3"], 3, 3),
        EvalCase("Who owns billing?", ["kb-9"], ["kb-3"], 1, 2),   # cited a doc not retrieved
    ]
    from pprint import pprint
    pprint(summarize(demo))
