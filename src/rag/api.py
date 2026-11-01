import json

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import config
from .llm import LLMNotConfigured
from .pipeline import answer, retrieve
from .store import get_client, get_collection

app = FastAPI(title="RAG demo", version="0.1.0")


class Question(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    top_k: int = Field(default=config.TOP_K, ge=1, le=10)


def _require_index():
    if get_collection(get_client()).count() == 0:
        raise HTTPException(503, "Index is empty. Run: python scripts/ingest.py")


@app.get("/health")
def health():
    meta = json.loads(config.INDEX_META_PATH.read_text()) if config.INDEX_META_PATH.exists() else None
    return {"status": "ok", "index": meta, "llm_model": config.OPENROUTER_MODEL}


@app.post("/search")
def search(body: Question):
    """Retrieval only (no LLM call)."""
    _require_index()
    return {"results": retrieve(body.question, body.top_k)}


@app.post("/ask")
def ask(body: Question):
    _require_index()
    try:
        return answer(body.question, body.top_k)
    except LLMNotConfigured as e:
        raise HTTPException(503, str(e))
    except httpx.HTTPError as e:
        raise HTTPException(502, f"LLM provider error: {e}")
