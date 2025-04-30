from qdrant_client import QdrantClient

client = QdrantClient("10.0.0.66", port=6333)
print(client.get_collections())
