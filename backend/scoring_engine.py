# analysis/scoring_engine.py

def compute_esg_score(chunks):
    """
    Compute ESG score using:
    - keyword signals
    - metric presence
    - action vs policy balance
    """

    if not chunks:
        return {
            "score": 0,
            "rating": "Poor",
            "breakdown": {}
        }

    # -------- COMBINE TEXT --------
    text = " ".join([
        c.get("text", "").lower()
        for c in chunks if c.get("text")
    ])

    # -------- BREAKDOWN --------
    breakdown = {
        "emissions": 0,
        "targets": 0,
        "renewable": 0,
        "transparency": 0,
        "penalty": 0
    }

    # -------- EMISSIONS (STRONG SIGNAL) --------
    emissions_score = 0
    for scope in ["scope 1", "scope 2", "scope 3"]:
        if scope in text:
            emissions_score += 10

    breakdown["emissions"] = emissions_score

    # -------- TARGETS --------
    if "target" in text or "goal" in text:
        breakdown["targets"] += 20

    # -------- RENEWABLE --------
    if any(x in text for x in ["renewable", "clean energy", "solar", "wind"]):
        breakdown["renewable"] += 10

    # -------- TRANSPARENCY (METRICS) --------
    metric_keywords = ["%", "tons", "kg", "co2", "intensity", "reduction"]
    metric_hits = sum(1 for m in metric_keywords if m in text)

    breakdown["transparency"] += min(metric_hits * 5, 25)

    # -------- PENALTY (VAGUE LANGUAGE) --------
    vague_words = ["committed", "aim", "strive", "working towards"]

    vague_hits = sum(1 for w in vague_words if w in text)

    # apply controlled penalty
    breakdown["penalty"] -= min(vague_hits * 2, 10)

    # -------- FINAL SCORE --------
    raw_score = sum(breakdown.values())

    # normalize to 0–100
    score = max(0, min(raw_score, 100))

    return {
        "score": score,
        "rating": get_rating(score),
        "breakdown": breakdown
    }


# -------- RATING --------
def get_rating(score):
    if score >= 75:
        return "Excellent"
    elif score >= 50:
        return "Good"
    elif score >= 30:
        return "Average"
    else:
        return "Poor"