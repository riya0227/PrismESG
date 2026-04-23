# model_loader.py

"""
Central model loader (wrapper around embeddings.get_model)

Use this ONLY if you want a clean import layer.
"""

from ingestion.embeddings import get_model


def load_embedding_model():
    return get_model()