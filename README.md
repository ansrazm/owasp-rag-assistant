# owasp-rag-assistant

A small, end-to-end **Retrieval-Augmented Generation (RAG)** service with basic **MLOps** practices:
experiment tracking, a versioned index, containerized deployment, and CI.

The demo knowledge base is a short Indonesian summary of the OWASP Top 10 (2021) in `data/docs/`.
Replace those `.md` files with your own documents and re-run ingestion.

## How it works

```
docs (.md) -> chunking -> multilingual embeddings (fastembed, local) -> ChromaDB
question  -> embed -> top-k similar chunks -> prompt with context -> LLM (OpenRouter) -> answer + sources
```

| Part | Choice |
|---|---|
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2` via fastembed (runs locally, supports Indonesian) |
| Vector DB | ChromaDB (persistent, cosine similarity) |
| LLM | Any model on OpenRouter (free `:free` models work) |
| API | FastAPI: `/health`, `/search` (retrieval only), `/ask` (RAG answer) |
| Experiment tracking | MLflow (SQLite backend) |
| Deployment | Docker + docker-compose |
| CI | GitHub Actions (pytest with a hashing embedder, no model download) |

## Quick start (local)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env        # add your OPENROUTER_API_KEY, then load it (see below)
python scripts/ingest.py    # builds the index; first run downloads the embedding model
uvicorn rag.api:app --app-dir src --reload
```

Load `.env` into your shell (Linux/macOS: `set -a; source .env; set +a`), or just export the variables.

```bash
curl -s localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "Bagaimana cara mencegah SQL injection?"}'
```

`/search` returns only the retrieved chunks, so you can test retrieval without an API key.

## Docker

```bash
cp .env.example .env
docker compose build
docker compose run --rm api python scripts/ingest.py
docker compose up
```

The `storage/` volume keeps the vector index and the downloaded model between runs.

## MLOps parts

- **Experiment tracking:** `python scripts/evaluate.py` runs a grid over chunk size, overlap, and top-k on
  `eval/questions.json` (labelled questions with the expected source document) and logs params and metrics
  (`hit_rate`, `mrr`) to MLflow. View with `mlflow ui --backend-store-uri sqlite:///storage/mlflow.db`.
- **Versioning:** each ingestion writes `storage/index_meta.json` (embedding model, chunk settings, document hash,
  timestamp), exposed at `/health`. The same document hash is logged with every MLflow run.
- **Deployment:** the API is containerized; configuration comes from environment variables.
- **CI:** `pytest` runs on every push (chunking, retrieval, API behavior).

## Choosing settings

Run the evaluation, pick the best combination, then set `CHUNK_SIZE`, `CHUNK_OVERLAP`, and `TOP_K` in `.env`
and re-run ingestion. The evaluation measures retrieval quality only (does the right document come back?),
not the quality of the LLM's wording.

## Limitations / next steps

- The evaluation set is small (14 questions), so treat differences between settings as indicative.
- No automated answer-quality evaluation yet (e.g., LLM-as-judge or faithfulness checks).
- No production monitoring (latency, retrieval scores, drift) or model registry yet.
- Free OpenRouter models are rate-limited and the free list changes; check https://openrouter.ai/models.
