import chromadb

from . import config


def get_client(path=None):
    p = path or config.CHROMA_DIR
    p.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(p))


def get_collection(client, name: str = config.COLLECTION):
    return client.get_or_create_collection(name, metadata={"hnsw:space": "cosine"})


def reset_collection(client, name: str = config.COLLECTION):
    try:
        client.delete_collection(name)
    except Exception:
        pass
    return get_collection(client, name)
