# vectorizer.py
# FUCKUP² Techno-Divination Engine: Vectorizer Module (with Caching)

import json
import hashlib
from pathlib import Path
from sentence_transformers import SentenceTransformer

CACHE_PATH = Path(".embedding_cache.json")

# Initialize the model once and reuse
_model = None

# Load or initialize cache
if CACHE_PATH.exists():
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        _cache = json.load(f)
else:
    _cache = {}

def _text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _save_cache():
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(_cache, f)

def load_model(model_name="all-MiniLM-L6-v2"):
    global _model
    if _model is None:
        print(f"🌀 Loading embedding model: {model_name}...")
        _model = SentenceTransformer(model_name)
    return _model

def embed_text(text):
    """
    Embed text (single string or list of strings) into dense vector(s).
    Uses SHA256 hash-based cache to avoid redundant computation.
    """
    model = load_model()

    if isinstance(text, str):
        key = _text_hash(text)
        if key in _cache:
            return _cache[key]
        embedding = model.encode(text, normalize_embeddings=True).tolist()
        _cache[key] = embedding
        _save_cache()
        return embedding

    elif isinstance(text, list):
        results = []
        new_items = {}

        for t in text:
            key = _text_hash(t)
            if key in _cache:
                results.append(_cache[key])
            else:
                new_items[key] = t

        if new_items:
            new_embeddings = model.encode(list(new_items.values()), normalize_embeddings=True)
            for i, (key, t) in enumerate(new_items.items()):
                _cache[key] = new_embeddings[i].tolist()
                results.append(_cache[key])
            _save_cache()

        return results

    else:
        raise TypeError("embed_text only accepts a string or a list of strings")

# Example usage (for testing)
if __name__ == "__main__":
    test_texts = [
        "The dragon coils beneath thunderclouds.",
        "Solar winds whisper through the bones of data."
    ]
    vecs = embed_text(test_texts)
    print(f"Embedding count: {len(vecs)} | Size: {len(vecs[0])}")
    print(vecs[0][:5], "...")
