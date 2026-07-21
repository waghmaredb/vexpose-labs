"""
Grounded retrieval for enterprise RAG — hybrid search + rerank + citation guard.

Companion code for:
  https://vexpose.blog/  (A Reference Architecture for Enterprise RAG)

The point of this file: retrieval quality, not model size, decides whether RAG
is trustworthy. We (1) retrieve with BOTH keyword and vector search, (2) rerank
the union, and (3) refuse to answer if nothing clears a relevance floor — so the
model can only ground on real context, never improvise.
"""

from dataclasses import dataclass


@dataclass
class Chunk:
    doc_id: str
    text: str
    score: float = 0.0


class GroundedRetriever:
    def __init__(self, bm25, vector_index, reranker, min_score: float = 0.35):
        self.bm25 = bm25                 # keyword search backend
        self.vector_index = vector_index # embedding search backend
        self.reranker = reranker         # cross-encoder: (query, chunk) -> score
        self.min_score = min_score       # relevance floor; below this we refuse

    def retrieve(self, query: str, k: int = 5) -> list[Chunk]:
        # 1) Hybrid recall: keyword catches exact terms, vectors catch meaning.
        candidates = self._dedupe(
            self.bm25.search(query, k=20) + self.vector_index.search(query, k=20)
        )

        # 2) Rerank the union with a cross-encoder — the single biggest quality win.
        for c in candidates:
            c.score = self.reranker.score(query, c.text)
        candidates.sort(key=lambda c: c.score, reverse=True)

        # 3) Relevance floor: if nothing is actually relevant, return nothing.
        #    An empty result is a feature — it lets the generator refuse.
        top = [c for c in candidates[:k] if c.score >= self.min_score]
        return top

    @staticmethod
    def _dedupe(chunks: list[Chunk]) -> list[Chunk]:
        seen, out = set(), []
        for c in chunks:
            key = (c.doc_id, c.text[:80])
            if key not in seen:
                seen.add(key)
                out.append(c)
        return out


GROUNDING_INSTRUCTION = (
    "Answer ONLY from the provided context. Cite the doc_id for every claim. "
    "If the context does not contain the answer, say 'I don't have that in the "
    "sources' — do not use prior knowledge."
)


def build_prompt(query: str, chunks: list[Chunk]) -> str:
    if not chunks:
        # No grounded context -> we don't even ask the model to guess.
        return f"{GROUNDING_INSTRUCTION}\n\nContext: (none)\n\nQuestion: {query}"
    context = "\n\n".join(f"[{c.doc_id}] {c.text}" for c in chunks)
    return f"{GROUNDING_INSTRUCTION}\n\nContext:\n{context}\n\nQuestion: {query}"
