from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from .schemas import TextChunk

# Load lightweight CPU‑friendly model
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def build_embeddings(chunks: List[TextChunk]) -> np.ndarray:
    """
    Convert text chunks into semantic embeddings.
    """

    model = get_model()
    texts = [c.text for c in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings
