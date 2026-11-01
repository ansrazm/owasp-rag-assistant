import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rag.pipeline import ingest  # noqa: E402

if __name__ == "__main__":
    print(json.dumps(ingest(), indent=2))
