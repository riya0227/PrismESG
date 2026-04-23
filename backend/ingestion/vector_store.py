# ingestion/vector_store.py

import faiss
import numpy as np


# -----------------------------
# BUILD INDEX
# -----------------------------
def build_faiss_index(embeddings):
    """
    Build FAISS index from embeddings
    """

    if embeddings is None or len(embeddings) == 0:
        raise ValueError("Embeddings are empty. Cannot build FAISS index.")

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index


# -----------------------------
# SAVE / LOAD
# -----------------------------
def save_faiss_index(index, path="faiss.index"):
    faiss.write_index(index, path)


def load_faiss_index(path="faiss.index"):
    return faiss.read_index(path)


# -----------------------------
# SEARCH
# -----------------------------
def search_faiss(query_embedding, index, chunks, top_k=5):
    """
    Search FAISS index and return top chunks
    """

    if index is None or index.ntotal == 0:
        return []

    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        # -------- Safety check --------
        if idx < 0 or idx >= len(chunks):
            continue

        chunk = chunks[idx]

        results.append({
            "score": float(distances[0][i]),
            "text": chunk["text"],
            "page": chunk.get("page_number"),
            "chunk_id": chunk.get("chunk_id")
        })

    return results