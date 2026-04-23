# analysis/classifier.py

from typing import List, Tuple
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


def train_esg_classifier(vectors, labeled_chunks: List[dict]) -> Tuple[LogisticRegression, LabelEncoder]:
    """
    Train a Logistic Regression classifier using TF-IDF vectors
    and weak ESG labels.
    """

    # -------- Extract labels --------
    labels = np.array([item["esg_label"] for item in labeled_chunks])

    # -------- Remove UNCLASSIFIED --------
    mask = labels != "UNCLASSIFIED"

    if mask.sum() == 0:
        raise ValueError("No valid labeled data found (all UNCLASSIFIED).")

    vectors_filtered = vectors[mask]
    labels_filtered = labels[mask]

    # -------- Encode labels --------
    encoder = LabelEncoder()
    y = encoder.fit_transform(labels_filtered)

    # -------- Train model --------
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(vectors_filtered, y)

    return model, encoder


def predict_esg(model, encoder, vectors):
    """
    Predict ESG labels using trained classifier.
    """

    if model is None or encoder is None:
        raise ValueError("Model or encoder not initialized.")

    preds = model.predict(vectors)
    labels = encoder.inverse_transform(preds)

    return labels


def predict_esg_with_confidence(model, encoder, vectors):
    """
    Predict ESG labels + confidence scores (for XAI).
    """

    if model is None or encoder is None:
        raise ValueError("Model or encoder not initialized.")

    probs = model.predict_proba(vectors)
    preds = np.argmax(probs, axis=1)

    labels = encoder.inverse_transform(preds)
    confidences = np.max(probs, axis=1)

    return labels, confidences