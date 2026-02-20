import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


# load SAME model used in embeddings.py
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_query(query: str):
    """
    Convert user query into embedding vector
    """
    return model.encode([query])


def semantic_search(query, embeddings, chunks, top_k=5):
    """
    Returns most relevant chunks for a query
    """
    query_vec = embed_query(query)

    # similarity between query and all chunk embeddings
    scores = cosine_similarity(query_vec, embeddings)[0]

    # sort highest similarity first
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "score": float(scores[idx]),
            "text": chunks[idx].text,
            "chunk_id": chunks[idx].chunk_id
        })

    return results