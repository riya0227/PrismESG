# analysis/esg_labeler.py

from typing import List, Dict
from collections import Counter
import re
from .schemas import TextChunk


# -----------------------------
# ESG KEYWORD CONFIGURATION
# -----------------------------
ESG_KEYWORDS: Dict[str, Dict[str, int]] = {
    "E": {
        "environment": 1,
        "environmental": 2,
        "climate": 2,
        "emissions": 3,
        "carbon": 3,
        "energy": 2,
        "renewable": 3,
        "water": 2,
        "waste": 2,
        "biodiversity": 3,
        "pollution": 3,
        "sustainability": 2,
    },
    "S": {
        "employee": 2,
        "employees": 2,
        "workforce": 2,
        "health": 2,
        "safety": 3,
        "training": 1,
        "diversity": 3,
        "inclusion": 3,
        "community": 2,
        "human rights": 3,
        "labour": 2,
        "well-being": 2,
    },
    "G": {
        "governance": 3,
        "board": 2,
        "directors": 2,
        "ethics": 3,
        "compliance": 3,
        "audit": 3,
        "risk": 2,
        "policy": 2,
        "regulation": 2,
        "transparency": 3,
    },
}


# -----------------------------
# CLEAN TOKEN MATCHING
# -----------------------------
def contains_keyword(text: str, keyword: str) -> bool:
    """
    Match full words only (avoids 'energy' in 'synergy')
    """
    pattern = r"\b" + re.escape(keyword) + r"\b"
    return re.search(pattern, text) is not None


# -----------------------------
# LABELING FUNCTION
# -----------------------------
def assign_esg_label(chunk: TextChunk) -> Dict:
    """
    Assign ESG label with score details (for XAI).
    """

    text = chunk.text.lower()
    scores = Counter()

    for label, keywords in ESG_KEYWORDS.items():
        for keyword, weight in keywords.items():
            if contains_keyword(text, keyword):
                scores[label] += weight

    # -------- No match --------
    if not scores:
        return {
            "label": "UNCLASSIFIED",
            "scores": {},
            "confidence": 0.0
        }

    # -------- Best label --------
    best_label, best_score = scores.most_common(1)[0]

    total_score = sum(scores.values())
    confidence = best_score / total_score if total_score > 0 else 0.0

    return {
        "label": best_label,
        "scores": dict(scores),
        "confidence": float(confidence)
    }


# -----------------------------
# LABEL ALL CHUNKS
# -----------------------------
def label_chunks(chunks: List[TextChunk]) -> List[Dict]:
    """
    Label chunks with ESG categories + scoring info.
    """

    labeled_data = []

    for chunk in chunks:
        result = assign_esg_label(chunk)

        labeled_data.append({
            "chunk_id": chunk.chunk_id,
            "text": chunk.text,
            "esg_label": result["label"],
            "scores": result["scores"],
            "confidence": result["confidence"]
        })

    return labeled_data