# analysis/strategy_engine.py

def generate_strategy_suggestions(pam_data, pillar_result, gaps=None):
    """
    Generates ESG improvement strategies.

    Returns:
    [
        {
            "pillar": "E",
            "issue": "...",
            "suggestion": "...",
            "priority": "HIGH",
            "confidence": 0.8,
            "based_on": {...}
        }
    ]
    """

    suggestions = []

    # -----------------------------
    # IDENTIFY WEAKEST PILLAR
    # -----------------------------
    weakest = pillar_result.get("weakest_pillar")

    # -----------------------------
    # AGGREGATE PAM
    # -----------------------------
    pillar_stats = {}

    for item in pam_data:
        pillar = item.get("esg_label")
        pam = item.get("pam_label")

        if not pillar or pillar == "UNCLASSIFIED":
            continue

        if pam not in ["Policy", "Action", "Metric"]:
            continue

        if pillar not in pillar_stats:
            pillar_stats[pillar] = {
                "Policy": 0,
                "Action": 0,
                "Metric": 0
            }

        pillar_stats[pillar][pam] += 1

    # -----------------------------
    # RULE-BASED SUGGESTIONS
    # -----------------------------
    for pillar, counts in pillar_stats.items():

        p = counts["Policy"]
        a = counts["Action"]
        m = counts["Metric"]

        total = p + a + m if (p + a + m) > 0 else 1

        # ---- Policy dominance ----
        if p > (a + m):
            suggestions.append(build_suggestion(
                pillar,
                issue="Policy-heavy disclosure",
                suggestion="Shift focus from commitments to real ESG implementation initiatives.",
                priority="HIGH",
                confidence=0.85,
                counts=counts
            ))

        # ---- Missing metrics ----
        if m == 0:
            suggestions.append(build_suggestion(
                pillar,
                issue="No measurable ESG metrics",
                suggestion="Introduce KPIs, targets, and quantitative disclosures.",
                priority="HIGH",
                confidence=0.9,
                counts=counts
            ))

        elif m < a:
            suggestions.append(build_suggestion(
                pillar,
                issue="Weak metric coverage",
                suggestion="Strengthen ESG reporting with measurable indicators.",
                priority="MEDIUM",
                confidence=0.7,
                counts=counts
            ))

        # ---- No actions ----
        if a == 0:
            suggestions.append(build_suggestion(
                pillar,
                issue="No ESG actions",
                suggestion="Implement operational ESG initiatives to support policies.",
                priority="HIGH",
                confidence=0.85,
                counts=counts
            ))

    # -----------------------------
    # WEAKEST PILLAR PRIORITY
    # -----------------------------
    if weakest:
        suggestions.append({
            "pillar": weakest,
            "issue": "Weakest ESG pillar",
            "suggestion": f"Prioritize improvement in {weakest} pillar based on overall ESG imbalance.",
            "priority": "CRITICAL",
            "confidence": pillar_result.get("confidence", 0.7),
            "based_on": pillar_result.get("scores", {}).get(weakest, {})
        })

    # -----------------------------
    # GAP-BASED SUGGESTIONS
    # -----------------------------
    if gaps:
        for gap in gaps:
            suggestions.append({
                "pillar": gap.get("principle"),
                "issue": gap.get("issue"),
                "suggestion": gap.get("reason"),
                "priority": gap.get("severity", "MEDIUM"),
                "confidence": gap.get("confidence", 0.6),
                "based_on": gap
            })

    return suggestions


# -----------------------------
# HELPER
# -----------------------------
def build_suggestion(pillar, issue, suggestion, priority, confidence, counts):
    return {
        "pillar": pillar,
        "issue": issue,
        "suggestion": suggestion,
        "priority": priority,
        "confidence": confidence,
        "based_on": {
            "policy_count": counts.get("Policy", 0),
            "action_count": counts.get("Action", 0),
            "metric_count": counts.get("Metric", 0)
        }
    }