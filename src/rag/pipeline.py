import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from . import config
from .chunking import chunk_text
from .embedder import get_embedder
from .llm import generate
from .store import get_client, get_collection, reset_collection

SYSTEM_PROMPT = (
    "Kamu adalah asisten yang menjawab HANYA berdasarkan konteks yang diberikan. "
    "Jika jawabannya tidak ada di konteks, katakan bahwa kamu tidak tahu. "
    "Jawab ringkas dalam bahasa yang sama dengan pertanyaan, dan sebutkan sumber dalam tanda kurung siku, misalnya [a03_injection.md]."
)


def load_docs(data_dir: Path = config.DATA_DIR) -> list[tuple[str, str]]:
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted(data_dir.glob("*.md"))]


def build_index(collection, chunk_size: int, overlap: int, data_dir: Path = config.DATA_DIR) -> dict:
    """Chunk every doc, embed, and store in `collection`. Returns index metadata."""
    docs = load_docs(data_dir)
    ids, texts, metas = [], [], []
    for name, text in docs:
        for i, chunk in enumerate(chunk_text(text, chunk_size, overlap)):
            ids.append(f"{name}:{i}")
            texts.append(chunk)
            metas.append({"source": name, "chunk": i})
    emb = get_embedder()
    if texts:
        collection.add(ids=ids, documents=texts, embeddings=emb.embed(texts), metadatas=metas)
    digest = hashlib.sha256("".join(t for _, t in docs).encode()).hexdigest()[:12]
    return {
        "embedding_model": emb.model_name,
        "chunk_size": chunk_size,
        "chunk_overlap": overlap,
        "n_docs": len(docs),
        "n_chunks": len(texts),
        "docs_sha256": digest,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def ingest() -> dict:
    client = get_client()
    col = reset_collection(client)
    meta = build_index(col, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    config.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    config.INDEX_META_PATH.write_text(json.dumps(meta, indent=2))
    return meta


def retrieve(question: str, k: int = config.TOP_K, collection=None) -> list[dict]:
    col = collection or get_collection(get_client())
    q = get_embedder().embed([question])[0]
    res = col.query(query_embeddings=[q], n_results=k)
    hits = []
    for text, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        hits.append({"text": text, "source": meta["source"], "chunk": meta["chunk"], "score": round(1 - dist, 4)})
    return hits


def answer(question: str, k: int = config.TOP_K) -> dict:
    hits = retrieve(question, k)
    context = "\n\n".join(f"[{h['source']}]\n{h['text']}" for h in hits)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Konteks:\n{context}\n\nPertanyaan: {question}"},
    ]
    return {"answer": generate(messages), "sources": hits}
