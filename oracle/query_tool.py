# query_tool.py
# FUCKUP² Chaos Stockpile Query Utility

from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from oracle.vectorizer import embed_text
from oracle.qdrant_integration import get_client, COLLECTION_NAME


def query_similar(
    text: str,
    section: Optional[str] = None,
    top_k: int = 5,
    filters: Optional[dict] = None,
) -> List[dict]:
    """
    Perform a vector similarity query against Qdrant.

    Args:
        text (str): The input query text.
        section (str, optional): Section filter (e.g. 'oracle').
        top_k (int): Number of results to return.
        filters (dict, optional): Additional payload filters.

    Returns:
        List of result dicts with score and payload.
    """
    client: QdrantClient = get_client()
    vector = embed_text(text)

    filter_conditions = []

    if section:
        filter_conditions.append(FieldCondition(key="section", match=MatchValue(value=section)))

    if filters:
        for key, val in filters.items():
            filter_conditions.append(FieldCondition(key=key, match=MatchValue(value=val)))

    qfilter = Filter(must=filter_conditions) if filter_conditions else None

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        query_filter=qfilter,
        limit=top_k,
        with_payload=True,
    )

    return [{"score": r.score, "payload": r.payload} for r in results]


# CLI interface for quick testing
if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "solar eclipse prophecy"
    hits = query_similar(query, section="oracle", top_k=3)
    for i, hit in enumerate(hits):
        print(f"#{i+1} Score: {hit['score']:.3f} | Date: {hit['payload'].get('date')} | Hexagram: {hit['payload'].get('hexagram_name')}")
        print(hit['payload']['content'][:300])
        print("\u2500" * 60)
