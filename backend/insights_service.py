# analysis/insights_service.py

from storage.document_store import load_document
from analysis.insights_engine import (
    extract_esg_insights,
    group_insights,
    detect_red_flags
)


def generate_insights(document_id):
    """
    Full ESG insights pipeline:
    - Extract insights
    - Group by topic
    - Detect red flags
    - Generate highlights
    """

    # -------- LOAD DOCUMENT --------
    doc = load_document(document_id)

    if not doc or "chunks" not in doc:
        return {
            "grouped_insights": {},
            "top_insights": [],
            "red_flags": [],
            "summary": "No data available."
        }

    chunks = doc["chunks"]

    if not chunks:
        return {
            "grouped_insights": {},
            "top_insights": [],
            "red_flags": [],
            "summary": "Document contains no usable text."
        }

    # -------- CORE INSIGHTS --------
    insights = extract_esg_insights(chunks)

    # -------- GROUP BY TOPIC --------
    grouped = group_insights(insights)

    # -------- TOP INSIGHTS (by importance) --------
    top_insights = sorted(
        insights,
        key=lambda x: x.get("importance", 0),
        reverse=True
    )[:10]

    # -------- RED FLAGS --------
    flags = detect_red_flags(chunks)

    # -------- SUMMARY --------
    summary = build_insight_summary(grouped, flags)

    return {
        "grouped_insights": grouped,
        "top_insights": top_insights,
        "red_flags": flags,
        "summary": summary
    }


# -----------------------------
# SUMMARY BUILDER (XAI)
# -----------------------------
def build_insight_summary(grouped, flags):
    """
    Generate quick ESG insight summary
    """

    if not grouped:
        return "No significant ESG insights detected."

    summary_parts = []

    # topic coverage
    topics = list(grouped.keys())
    summary_parts.append(f"Detected ESG topics: {', '.join(topics)}.")

    # flag warning
    if flags:
        summary_parts.append(f"{len(flags)} potential ESG red flags identified.")

    # highlight strong areas
    strong_topics = [
        t for t, items in grouped.items()
        if len(items) > 5
    ]

    if strong_topics:
        summary_parts.append(
            f"Strong disclosure in: {', '.join(strong_topics)}."
        )

    return " ".join(summary_parts)