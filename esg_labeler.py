from typing import List, Dict
from collections import Counter
from .schemas import TextChunk

# -----------------------------
# ESG KEYWORD CONFIGURATION
# -----------------------------
ESG_KEYWORDS: Dict[str, List[str]] = {
    "E": [
        "environment", "environmental", "climate", "emissions", "carbon",
        "energy", "renewable", "water", "waste", "biodiversity",
        "pollution", "sustainability"
    ],
    "S": [
        "employee", "employees", "workforce", "health", "safety",
        "training", "diversity", "inclusion", "community",
        "human rights", "labour", "well-being"
    ],
    "G": [
        "governance", "board", "directors", "ethics", "compliance",
        "audit", "risk", "policy", "regulation", "transparency"
    ]
}

# -----------------------------
# LABELING FUNCTION
# -----------------------------
def assign_esg_label(chunk: TextChunk) -> str:
    """
    Assign an ESG label (E / S / G) to a text chunk
    using keyword frequency heuristics.
    """

    text = chunk.text.lower()
    scores = Counter()

    for label, keywords in ESG_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[label] += 1

    # If no keywords matched, mark as 'UNCLASSIFIED'
    if not scores:
        return "UNCLASSIFIED"

    # Return label with highest score
    return scores.most_common(1)[0][0]


def label_chunks(chunks: List[TextChunk]) -> List[Dict]:
    """
    Label a list of TextChunks with ESG categories.
    Returns a list of dictionaries for downstream ML use.
    """

    labeled_data = []

    for chunk in chunks:
        label = assign_esg_label(chunk)
        labeled_data.append({
            "chunk_id": chunk.chunk_id,
            "text": chunk.text,
            "esg_label": label
        })

    return labeled_data
