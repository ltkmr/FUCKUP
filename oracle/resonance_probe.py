# resonance_probe.py
# FUCKUP² Chaos Echo Finder

from oracle.vectorizer import embed_text
from oracle.qdrant_integration import get_client, COLLECTION_NAME

DEFAULT_TOP_K = 3

def recall_similar_divinations(query_text, top_k=DEFAULT_TOP_K):
    client = get_client()
    vector = embed_text(query_text)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        vector=vector,
        limit=top_k
    )

    print("\n🔍 Resonant Echoes Found:")
    for i, hit in enumerate(results, start=1):
        payload = hit.payload
        print(f"\n#{i}: {payload.get('date', 'Unknown Date')} — Hexagram {payload.get('hexagram')} {payload.get('hexagram_name')}")
        print(f"✦ Score: {hit.score:.4f}")
        print(f"✦ Excerpt: {payload.get('oracle_excerpt', '')[:300]}...")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m oracle.resonance_probe \"your question or phrase here\"")
        exit(1)

    input_text = " ".join(sys.argv[1:])
    recall_similar_divinations(input_text)
