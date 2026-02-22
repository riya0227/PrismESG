from typing import List, Tuple
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


def train_esg_classifier(vectors, labeled_chunks: List[dict]) -> Tuple[LogisticRegression, LabelEncoder]:
    """
    Train a Logistic Regression classifier using TF-IDF vectors
    and weak ESG labels.
    """

    # Extract labels
    labels = [item["esg_label"] for item in labeled_chunks]

    # Convert to numpy
    labels = np.array(labels)

    # ---- IMPORTANT ----
    # Remove UNCLASSIFIED samples (no signal)
    mask = labels != "UNCLASSIFIED"
    vectors = vectors[mask]
    labels = labels[mask]

    # Encode labels (E/S/G → numbers)
    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)

    # Train classifier
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(vectors, y)

    return model, encoder

def predict_esg(model, encoder, vectors):
    """
    Predict ESG labels using trained classifier.
    """
    preds = model.predict(vectors)
    labels = encoder.inverse_transform(preds)
    return labels
