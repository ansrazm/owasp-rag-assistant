import pytest
from fastapi.testclient import TestClient

from rag import config, pipeline
from rag.store import get_client, reset_collection


@pytest.fixture()
def api(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "STORAGE_DIR", tmp_path)
    monkeypatch.setattr(config, "CHROMA_DIR", tmp_path / "chroma")
    monkeypatch.setattr(config, "INDEX_META_PATH", tmp_path / "index_meta.json")
    from rag.api import app
    return TestClient(app)


def test_retrieval_finds_expected_doc(tmp_path):
    col = reset_collection(get_client(tmp_path / "c"), "test_col")
    meta = pipeline.build_index(col, 500, 80)
    assert meta["n_docs"] == 10 and meta["n_chunks"] >= 10
    hits = pipeline.retrieve("Bagaimana cara mencegah SQL injection?", 3, col)
    assert "a03_injection.md" in [h["source"] for h in hits]


def test_api_search_and_ask_without_key(api, monkeypatch):
    assert api.post("/search", json={"question": "apa itu SSRF"}).status_code == 503  # empty index
    pipeline.ingest()
    r = api.post("/search", json={"question": "SSRF server-side request forgery"})
    assert r.status_code == 200 and r.json()["results"][0]["source"] == "a10_ssrf.md"
    monkeypatch.setattr(config, "OPENROUTER_API_KEY", "")
    assert api.post("/ask", json={"question": "apa itu SSRF"}).status_code == 503
    assert api.get("/health").json()["index"]["n_docs"] == 10
