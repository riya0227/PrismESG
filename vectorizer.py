from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from .schemas import TextChunk

def build_tfidf_vectors(
    chunks: List[TextChunk],
    max_features: int = 5000
) -> Tuple[TfidfVectorizer, any]:
    """
    Fit a TF-IDF vectorizer on text chunks
    and return the vectorizer + vectors.
    """

    texts = [chunk.text for chunk in chunks]

    vectorizer = TfidfVectorizer(
        max_features=max_features,
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(texts)

    return vectorizer, vectors
