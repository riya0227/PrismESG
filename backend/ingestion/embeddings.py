# ingestion/embeddings.py

import numpy as np
from sentence_transformers import SentenceTransformer

# ---- GLOBAL MODEL (loaded once) ----
_model = None


def get_model():
    """
    Load the sentence transformer model once
    (avoids reloading every time)
    """
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


# ---------- BUILD EMBEDDINGS FOR CHUNKS ----------
def build_embeddings(chunks):
    """
    Convert all text chunks into embeddings

    Returns:
    np.ndarray of shape (num_chunks, 384)
    """

    if not chunks:
        return np.array([], dtype="float32")

    model = get_model()

    # ✅ dict-based chunks
    texts = [chunk["text"] for chunk in chunks if "text" in chunk]

    if not texts:
        return np.array([], dtype="float32")

    embeddings = model.encode(
        texts,
        batch_size=32,               # ✅ prevents memory spikes
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True    # ✅ improves similarity search
    )

    return embeddings.astype("float32")  # ✅ FAISS-compatible


# ---------- EMBED USER QUERY ----------
def embed_query(query: str):
    """
    Convert user query into embedding
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    model = get_model()

    embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]

    return embedding.astype("float32")