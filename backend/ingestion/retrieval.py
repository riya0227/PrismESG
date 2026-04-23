# ingestion/retrieval.py

import numpy as np
from ingestion.embeddings import embed_query
from storage.document_store import load_document


# -------- SEARCH --------
def retrieve_chunks(query: str, document_id: str, top_k: int = 5):
    """
    Retrieve top-k relevant chunks for a query from a specific document
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    # -------- LOAD DOCUMENT --------
    doc = load_document(document_id)

    chunks = doc["chunks"]
    index = doc["faiss_index"]

    if not chunks or index.ntotal == 0:
        return []

    # -------- EMBED QUERY --------
    query_vec = embed_query(query)
    query_vec = np.array([query_vec]).astype("float32")

    # -------- FAISS SEARCH --------
    distances, indices = index.search(query_vec, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        if idx < 0 or idx >= len(chunks):
            continue

        chunk = chunks[idx]

        results.append({
            "text": chunk["text"],
            "score": float(distances[0][i]),
            "page": chunk.get("page_number"),
            "chunk_id": chunk.get("chunk_id")
        })

    return results