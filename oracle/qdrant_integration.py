# qdrant_integration.py
# FUCKUP² Chaos Node: Qdrant Vector Storage Interface

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
from datetime import datetime

# Qdrant location (Chaos Node)
QDRANT_HOST = "10.0.0.66"
QDRANT_PORT = 6333
COLLECTION_NAME = "divinations"
VECTOR_SIZE = 384  # for MiniLM

def get_client():
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def ensure_collection():
    client = get_client()
    if COLLECTION_NAME not in [col.name for col in client.get_collections().collections]:
        print("✨ Creating Qdrant collection: divinations")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
    return client

def store_divination(embedding, metadata):
    """
    Store a vector + metadata into the Chaos Node.

    Args:
        embedding (list of float): The 384-dim vector.
        metadata (dict): Additional payload info.
    """
    client = ensure_collection()
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload=metadata
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])
    print("✅ Prophecy stored in Chaos Memory.")

# Optional test
if __name__ == "__main__":
    from vectorizer import embed_text

    test_text = "The sky cracked open and the coins fell upward."
    vec = embed_text(test_text)
    payload = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "hexagram": 49,
        "hexagram_name": "Revolution",
        "celestial_event": "Saturn squares Mercury",
        "oracle_excerpt": test_text
    }
    store_divination(vec, payload)
