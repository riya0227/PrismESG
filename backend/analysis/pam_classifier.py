# analysis/pam_classifier.py

import re


# -----------------------------
# KEYWORD CONFIG
# -----------------------------
METRIC_KEYWORDS = [
    "percent", "%", "tonnes", "tons", "mt", "kg",
    "increase", "decrease", "reduction", "target",
    "kpi", "intensity", "emissions data",
    "scope 1", "scope 2", "scope 3", "net zero", "baseline"
]

ACTION_KEYWORDS = [
    "implemented", "launched", "conducted",
    "reduced", "improved", "installed",
    "developed", "executed", "achieved",
    "transitioned", "invested", "initiated"
]

POLICY_KEYWORDS = [
    "committed", "aim", "focus", "policy",
    "vision", "believe", "strive", "intend",
    "pledge", "objective"
]


# -----------------------------
# MAIN CLASSIFIER
# -----------------------------
def classify_pam(text: str):
    """
    Classify text into:
    Policy / Action / Metric

    Returns:
    {
        "label": str,
        "confidence": float,
        "reason": str
    }
    """

    text_lower = text.lower()

    # -------- Metric detection --------
    number_match = re.search(r"\b\d+(\.\d+)?\b", text_lower)

    if number_match and any(k in text_lower for k in METRIC_KEYWORDS):
        return {
            "label": "Metric",
            "confidence": 0.9,
            "reason": "Contains numerical data with ESG metric keywords"
        }

    if any(k in text_lower for k in METRIC_KEYWORDS):
        return {
            "label": "Metric",
            "confidence": 0.75,
            "reason": "Contains ESG metric-related keywords"
        }

    # -------- Action detection --------
    if any(k in text_lower for k in ACTION_KEYWORDS):
        return {
            "label": "Action",
            "confidence": 0.8,
            "reason": "Describes implemented ESG activities"
        }

    # -------- Policy detection --------
    if any(k in text_lower for k in POLICY_KEYWORDS):
        return {
            "label": "Policy",
            "confidence": 0.7,
            "reason": "Describes ESG intent or commitment"
        }

    # -------- Default --------
    return {
        "label": "Policy",
        "confidence": 0.5,
        "reason": "No strong indicators found (default classification)"
    }


# -----------------------------
# APPLY TO CHUNKS
# -----------------------------
def apply_pam_classification(chunks, esg_predictions):
    """
    Combine PAM + ESG labels
    """

    enriched = []

    for chunk, esg in zip(chunks, esg_predictions):

        result = classify_pam(chunk.text)

        enriched.append({
            "text": chunk.text,
            "esg_label": esg,
            "pam_label": result["label"],
            "pam_confidence": result["confidence"],
            "pam_reason": result["reason"]
        })

    return enriched