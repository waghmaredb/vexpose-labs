-- pgvector index tuning — the two knobs that decide everything.
-- Companion to: Your pgvector Search Gets Slower as You Add Data
--   https://vexpose.blog/
--
-- Rule of thumb for IVFFlat `lists`:
--   lists ≈ rows / 1000   up to ~1M rows
--   lists ≈ sqrt(rows)    beyond ~1M rows
-- For 2,000,000 rows -> sqrt(2e6) ≈ 1414 lists.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS docs (
  id        bigserial PRIMARY KEY,
  embedding vector(768)
);

-- Build the index AFTER the data is loaded: IVFFlat clusters existing vectors to
-- define its lists. On an empty/tiny table the clusters are meaningless.
CREATE INDEX IF NOT EXISTS docs_embedding_ivf
  ON docs USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 1414);

-- probes trades recall for speed AT QUERY TIME. Default of 1 is far too low.
-- Sane start ≈ sqrt(lists); sqrt(1414) ≈ 38. Then tune to a recall target.
SET ivfflat.probes = 38;

-- Alternative: HNSW. Slower to build, larger on disk, better recall/latency, and
-- no clusters to go stale as data changes — usually the better pick for churny data.
-- CREATE INDEX docs_embedding_hnsw ON docs USING hnsw (embedding vector_cosine_ops)
--   WITH (m = 16, ef_construction = 64);
-- SET hnsw.ef_search = 40;
