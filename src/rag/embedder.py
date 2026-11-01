import re
import zlib

import numpy as np

from . import config


class FastEmbedder:
    """Local multilingual embeddings (ONNX via fastembed). Works for Indonesian."""

    def __init__(self, model_name: str = config.EMBEDDING_MODEL):
        from fastembed import TextEmbedding

        cache = config.STORAGE_DIR / "fastembed_cache"
        cache.mkdir(parents=True, exist_ok=True)
        self.model_name = model_name
        self._model = TextEmbedding(model_name=model_name, cache_dir=str(cache))

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [v.tolist() for v in self._model.embed(texts)]


class FakeEmbedder:
    """Deterministic hashing bag-of-words embedder. For tests and CI only (no downloads)."""

    model_name = "fake-hashing-384"
    dim = 384

    def embed(self, texts: list[str]) -> list[list[float]]:
        out = []
        for t in texts:
            v = np.zeros(self.dim, dtype=np.float32)
            for tok in re.findall(r"\w+", t.lower()):
                v[zlib.crc32(tok.encode()) % self.dim] += 1.0
            n = np.linalg.norm(v)
            out.append((v / n if n else v).tolist())
        return out


_embedder = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = FakeEmbedder() if config.EMBEDDER == "fake" else FastEmbedder()
    return _embedder
