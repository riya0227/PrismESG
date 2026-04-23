# analysis/gap_analysis.py

from typing import List, Union


def detect_gaps(text_chunks: List[Union[str, object]]):
    """
    Detect ESG disclosure gaps.

    Accepts:
    - list of strings OR
    - list of TextChunk objects
    """

    # -------- Normalize input --------
    processed_texts = []

    for chunk in text_chunks:
        if hasattr(chunk, "text"):
            processed_texts.append(chunk.text.lower())
        else:
            processed_texts.append(str(chunk).lower())

    combined_text = " ".join(processed_texts)

    gaps = []

    # -----------------------------
    # ENVIRONMENTAL (P6)
    # -----------------------------
    if contains_any(combined_text, ["emission", "emissions", "climate", "carbon"]):

        has_metrics = contains_any(combined_text, [
            "ton", "co2", "kg", "intensity", "%", "scope 1", "scope 2", "scope 3"
        ])

        has_actions = contains_any(combined_text, [
            "reduce", "target", "plan", "initiative", "transition"
        ])

        if not has_metrics:
            gaps.append(build_gap(
                principle="P6",
                issue="Lack of measurable emissions data",
                reason="Emissions discussed but no quantitative metrics found",
                severity="HIGH"
            ))

        elif not has_actions:
            gaps.append(build_gap(
                principle="P6",
                issue="Metrics without action plan",
                reason="Data present but no clear reduction strategy",
                severity="MEDIUM"
            ))

    # -----------------------------
    # SOCIAL (P3)
    # -----------------------------
    if contains_any(combined_text, ["employee", "workforce", "labour"]):

        has_metrics = contains_any(combined_text, [
            "number", "%", "ratio", "diversity", "gender", "turnover"
        ])

        if not has_metrics:
            gaps.append(build_gap(
                principle="P3",
                issue="Missing workforce metrics",
                reason="Employee-related discussion lacks measurable indicators",
                severity="MEDIUM"
            ))

    # -----------------------------
    # GOVERNANCE (P1)
    # -----------------------------
    if contains_any(combined_text, ["board", "governance", "directors"]):

        has_structure = contains_any(combined_text, [
            "independent", "committee", "meetings", "audit", "chair"
        ])

        if not has_structure:
            gaps.append(build_gap(
                principle="P1",
                issue="Weak governance structure disclosure",
                reason="Board mentioned but governance mechanisms unclear",
                severity="MEDIUM"
            ))

    return gaps


# -----------------------------
# HELPERS
# -----------------------------
def contains_any(text: str, keywords: List[str]) -> bool:
    return any(k in text for k in keywords)


def build_gap(principle, issue, reason, severity):
    """
    Standardized gap output (XAI-friendly)
    """
    return {
        "principle": principle,
        "issue": issue,
        "reason": reason,
        "severity": severity,
        "confidence": map_severity_to_confidence(severity)
    }


def map_severity_to_confidence(severity: str) -> float:
    """
    Convert severity → confidence score
    """
    mapping = {
        "HIGH": 0.9,
        "MEDIUM": 0.6,
        "LOW": 0.3
    }
    return mapping.get(severity, 0.5)