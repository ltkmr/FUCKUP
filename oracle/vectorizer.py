from sentence_transformers import SentenceTransformer

# Initialize the model once and reuse
_model = None

def load_model(model_name="all-MiniLM-L6-v2"):
    global _model
    if _model is None:
        print(f"🌀 Loading embedding model: {model_name}...")
        _model = SentenceTransformer(model_name)
    return _model

def embed_text(text):
    """
    Embed a piece of text into a dense vector.

    Args:
        text (str): The input text to embed.

    Returns:
        list: Dense vector (list of floats).
    """
    model = load_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

# Example usage (for testing)
if __name__ == "__main__":
    test_text = "The dragon coils beneath thunderclouds."
    vec = embed_text(test_text)
    print(f"Embedding size: {len(vec)}")
    print(vec[:5], "...")  # Print first 5 elements for sanity check