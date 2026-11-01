import pytest

from rag.chunking import chunk_text


def test_chunks_respect_size_and_keep_content():
    text = "\n\n".join(f"Paragraf nomor {i}. " + "kata " * 30 for i in range(10))
    chunks = chunk_text(text, size=300, overlap=40)
    assert len(chunks) > 1
    assert all(len(c) <= 300 + 40 + 1 for c in chunks)
    assert "nomor 0" in chunks[0] and "nomor 9" in chunks[-1]


def test_long_paragraph_is_split():
    chunks = chunk_text("a" * 1000, size=300, overlap=50)
    assert len(chunks) >= 4


def test_invalid_overlap_raises():
    with pytest.raises(ValueError):
        chunk_text("x", size=50, overlap=50)
