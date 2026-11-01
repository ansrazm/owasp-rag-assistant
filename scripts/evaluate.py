"""Compare chunking/top-k settings on a small labelled question set and log every run to MLflow.

Metrics: hit_rate (expected source appears in top-k) and mrr (mean reciprocal rank).
Run:  python scripts/evaluate.py      then      mlflow ui --backend-store-uri sqlite:///storage/mlflow.db
"""
import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import mlflow  # noqa: E402

from rag import config  # noqa: E402
from rag.embedder import get_embedder  # noqa: E402
from rag.pipeline import build_index, retrieve  # noqa: E402
from rag.store import get_client, reset_collection  # noqa: E402

QUESTIONS = Path(__file__).resolve().parents[1] / "eval" / "questions.json"


def ints(s):
    return [int(x) for x in s.split(",")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk-sizes", type=ints, default=[250, 500, 900])
    ap.add_argument("--overlaps", type=ints, default=[0, 80])
    ap.add_argument("--top-ks", type=ints, default=[1, 3, 5])
    args = ap.parse_args()

    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    config.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(f"sqlite:///{config.STORAGE_DIR / 'mlflow.db'}")
    mlflow.set_experiment("rag-retrieval")
    client = get_client(config.STORAGE_DIR / "eval_chroma")
    emb = get_embedder()
    rows = []

    for size, overlap in itertools.product(args.chunk_sizes, args.overlaps):
        if size <= overlap:
            continue
        col = reset_collection(client, f"eval_{size}_{overlap}")
        meta = build_index(col, size, overlap)
        for k in args.top_ks:
            ranks, details = [], []
            for q in questions:
                hits = retrieve(q["question"], k, col)
                sources = [h["source"] for h in hits]
                rank = sources.index(q["expected_source"]) + 1 if q["expected_source"] in sources else None
                ranks.append(rank)
                details.append({"question": q["question"], "expected": q["expected_source"], "rank": rank})
            hit = sum(r is not None for r in ranks) / len(ranks)
            mrr = sum(1 / r for r in ranks if r) / len(ranks)
            with mlflow.start_run(run_name=f"size{size}_ov{overlap}_k{k}"):
                mlflow.log_params({"chunk_size": size, "chunk_overlap": overlap, "top_k": k,
                                   "embedding_model": emb.model_name, "docs_sha256": meta["docs_sha256"]})
                mlflow.log_metrics({"hit_rate": hit, "mrr": mrr, "n_chunks": meta["n_chunks"]})
                mlflow.log_dict({"results": details}, "per_question.json")
            rows.append((size, overlap, k, hit, mrr, meta["n_chunks"]))

    rows.sort(key=lambda r: (-r[3], -r[4], r[5]))
    print(f"{'size':>5} {'ovl':>4} {'k':>2} {'hit':>6} {'mrr':>6} {'chunks':>6}")
    for r in rows:
        print(f"{r[0]:>5} {r[1]:>4} {r[2]:>2} {r[3]:>6.2f} {r[4]:>6.2f} {r[5]:>6}")


if __name__ == "__main__":
    main()
