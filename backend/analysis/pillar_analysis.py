# analysis/pillar_analysis.py

def analyze_pillars(pam_data):
    """
    Analyze ESG pillars based on Policy–Action–Metric balance.

    Returns:
    {
        "weakest_pillar": str,
        "reason": str,
        "confidence": float,
        "scores": {...}
    }
    """

    scores = {}

    # -----------------------------
    # AGGREGATE COUNTS
    # -----------------------------
    for item in pam_data:
        pillar = item.get("esg_label")
        pam = item.get("pam_label")

        if not pillar or pillar == "UNCLASSIFIED":
            continue

        if pam not in ["Policy", "Action", "Metric"]:
            continue

        if pillar not in scores:
            scores[pillar] = {
                "score": 0.0,
                "details": {
                    "Policy": 0,
                    "Action": 0,
                    "Metric": 0
                }
            }

        scores[pillar]["details"][pam] += 1

    # -----------------------------
    # SAFETY CHECK
    # -----------------------------
    if not scores:
        return {
            "weakest_pillar": "UNKNOWN",
            "reason": "No valid ESG-labelled data available",
            "confidence": 0.0,
            "scores": {}
        }

    # -----------------------------
    # SCORING LOGIC (ALIGNED WITH ESG SCORER)
    # -----------------------------
    for pillar in scores:

        p = scores[pillar]["details"]["Policy"]
        a = scores[pillar]["details"]["Action"]
        m = scores[pillar]["details"]["Metric"]

        total = p + a + m

        if total == 0:
            scores[pillar]["score"] = 0
            continue

        # weighted scoring (same logic as ESG scorer)
        weighted = (p * 1 + a * 2 + m * 3) / total

        # normalize to /10
        final_score = (weighted / 3) * 10

        scores[pillar]["score"] = round(final_score, 2)

        # add ratios (XAI)
        scores[pillar]["details"].update({
            "policy_ratio": round(p / total, 3),
            "action_ratio": round(a / total, 3),
            "metric_ratio": round(m / total, 3)
        })

    # -----------------------------
    # FIND WEAKEST
    # -----------------------------
    weakest = min(scores, key=lambda x: scores[x]["score"])
    weakest_data = scores[weakest]

    # -----------------------------
    # XAI REASONING
    # -----------------------------
    reason = build_pillar_reason(weakest, weakest_data)

    confidence = compute_pillar_confidence(weakest_data)

    return {
        "weakest_pillar": weakest,
        "reason": reason,
        "confidence": confidence,
        "scores": scores
    }


# -----------------------------
# XAI HELPERS
# -----------------------------
def build_pillar_reason(pillar, data):
    d = data["details"]

    if d["metric_ratio"] < 0.2:
        return f"{pillar} is weakest due to lack of measurable ESG metrics."

    if d["action_ratio"] < 0.3:
        return f"{pillar} lacks sufficient ESG actions despite policies."

    if d["policy_ratio"] > 0.6:
        return f"{pillar} is dominated by policy statements with weak execution."

    return f"{pillar} has relatively weaker ESG balance compared to other pillars."


def compute_pillar_confidence(data):
    """
    Confidence based on imbalance severity
    """
    d = data["details"]

    imbalance = max(
        d["policy_ratio"],
        d["action_ratio"],
        d["metric_ratio"]
    )

    return round(imbalance, 2)