# analysis/insights_engine.py

import numpy as np

# -------- ESG TOPICS --------
ESG_TOPICS = {
    "emissions": ["emissions", "carbon", "ghg", "scope 1", "scope 2", "scope 3"],
    "energy": ["renewable", "energy", "electricity"],
    "water": ["water", "wastewater"],
    "waste": ["waste", "recycling"],
    "governance": ["board", "ethics", "compliance"],
}

# -------- MULTI-TOPIC DETECTION --------
def detect_topics(text):
    text_lower = text.lower()
    matched = []

    for topic, keywords in ESG_TOPICS.items():
        if any(kw in text_lower for kw in keywords):
            matched.append(topic)

    return matched if matched else ["other"]


# -------- INSIGHT EXTRACTION --------
def extract_esg_insights(chunks):
    """
    Extract structured ESG insights with topic + importance
    """

    insights = []

    for chunk in chunks:
        text = chunk.get("text", "")
        page = chunk.get("page_number")

        if not text:
            continue

        topics = detect_topics(text)

        importance = compute_importance(text)

        insights.append({
            "text": text,
            "topics": topics,
            "page": page,
            "importance": importance
        })

    return insights


# -------- IMPORTANCE SCORING --------
def compute_importance(text):
    """
    Simple heuristic importance score
    """

    score = 0
    text_lower = text.lower()

    # metrics = high importance
    if any(x in text_lower for x in ["%", "target", "reduction", "increase"]):
        score += 2

    # action words
    if any(x in text_lower for x in ["implemented", "reduced", "achieved"]):
        score += 1

    # long informative text
    score += min(len(text) / 200, 1)

    return round(score, 2)


# -------- GROUP INSIGHTS --------
def group_insights(insights):
    grouped = {}

    for item in insights:
        for topic in item["topics"]:

            if topic not in grouped:
                grouped[topic] = []

            grouped[topic].append(item)

    return grouped


# -------- RED FLAG DETECTION (UPGRADED) --------
def detect_red_flags(chunks):
    """
    Detect vague or suspicious ESG claims
    """

    flags = []

    vague_words = ["committed", "aim to", "strive", "working towards"]
    metric_words = ["%", "target", "ton", "kg", "co2", "intensity"]

    for chunk in chunks:
        text = chunk.get("text", "").lower()
        page = chunk.get("page_number")

        if not text:
            continue

        # ---- Vague claim detection ----
        if any(v in text for v in vague_words):
            if not any(m in text for m in metric_words):
                flags.append({
                    "text": chunk.get("text"),
                    "page": page,
                    "type": "VAGUE_CLAIM",
                    "severity": "MEDIUM",
                    "reason": "Claim lacks measurable targets"
                })

        # ---- Missing metrics for emissions ----
        if "emission" in text or "carbon" in text:
            if not any(m in text for m in metric_words):
                flags.append({
                    "text": chunk.get("text"),
                    "page": page,
                    "type": "MISSING_METRIC",
                    "severity": "HIGH",
                    "reason": "Environmental claim without quantitative data"
                })

    return flags