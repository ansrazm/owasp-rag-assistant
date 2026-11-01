import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
# Read ROOT/.env when running locally (Docker passes env vars itself, which take priority).
load_dotenv(ROOT / ".env", override=False)
DATA_DIR = Path(os.getenv("DATA_DIR", ROOT / "data" / "docs"))
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", ROOT / "storage"))
CHROMA_DIR = STORAGE_DIR / "chroma"
INDEX_META_PATH = STORAGE_DIR / "index_meta.json"
COLLECTION = "docs"

# "fastembed" = real multilingual model (downloaded on first run). "fake" = hashing embedder for tests/CI.
EMBEDDER = os.getenv("EMBEDDER", "fastembed")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "80"))
TOP_K = int(os.getenv("TOP_K", "4"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
