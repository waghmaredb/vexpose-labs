# Enterprise RAG — grounded retrieval reference

Companion code for **A Reference Architecture for Enterprise RAG (That Won't Hallucinate Your Docs)** on [vExpose.blog](https://vexpose.blog).

RAG demos are easy; RAG that refuses to confidently cite the wrong document is the hard part. The failure is almost never the model — it's retrieval handing over plausible-but-wrong context, which a bigger model then synthesizes more fluently. *The tool is not the transformation.* The fix lives in the retrieval and grounding layers.

## Files

| File | Role |
|------|------|
| [`retriever.py`](./retriever.py) | Hybrid (keyword + vector) recall → cross-encoder rerank → a relevance floor that lets the system **refuse** when nothing is truly relevant. Plus a grounding prompt that forbids answering outside the context. |
| [`eval_groundedness.py`](./eval_groundedness.py) | A minimal faithfulness harness: scores groundedness and catches hallucinated citations, so every prompt/model/index change is measured, not guessed. |

## Run the eval demo

```bash
python3 eval_groundedness.py
```

> Retrieval quality, not model size, is what makes RAG trustworthy. An empty retrieval result is a feature — it's what lets the generator say "I don't have that in the sources."
