# ingestion/vectorizer.py

from sklearn.feature_extraction.text import TfidfVectorizer


# 🔥 Global instance (for reuse in hybrid search)
vectorizer_instance = None


def build_tfidf_vectors(chunks):
    """
    Optional TF-IDF (for hybrid search)
    """

    global vectorizer_instance

    if not chunks:
        return None, None

    # -------- Extract text safely --------
    texts = [chunk["text"] for chunk in chunks if "text" in chunk]

    if not texts:
        return None, None

    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(texts)

    # ✅ store globally for query-time reuse
    vectorizer_instance = vectorizer

    return vectorizer, vectors


# -----------------------------
# QUERY EMBEDDING (TF-IDF)
# -----------------------------
def embed_query_tfidf(query: str):
    """
    Convert query into TF-IDF vector
    """

    global vectorizer_instance

    if vectorizer_instance is None:
        raise ValueError("TF-IDF vectorizer not initialized. Run pipeline first.")

    return vectorizer_instance.transform([query])