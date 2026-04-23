# analysis/greenwashing.py

def detect_greenwashing(pam_data):
    """
    Detects greenwashing likelihood based on:
    Policy vs Action vs Metric imbalance

    Returns:
    {
        "E": {
            "risk": "HIGH",
            "confidence": 0.9,
            "details": {...},
            "explanation": "..."
        }
    }
    """

    pillar_stats = {}

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

        if pillar not in pillar_stats:
            pillar_stats[pillar] = {
                "Policy": 0,
                "Action": 0,
                "Metric": 0
            }

        pillar_stats[pillar][pam] += 1

    results = {}

    # -----------------------------
    # RISK ANALYSIS
    # -----------------------------
    for pillar, counts in pillar_stats.items():

        p = counts.get("Policy", 0)
        a = counts.get("Action", 0)
        m = counts.get("Metric", 0)

        total = p + a + m

        if total == 0:
            continue

        policy_ratio = p / total
        action_ratio = a / total
        metric_ratio = m / total

        # 🚨 Risk Logic
        if policy_ratio > 0.6 and (a + m) < p * 0.5:
            risk = "HIGH"
            confidence = 0.9

        elif policy_ratio > 0.5 and metric_ratio < 0.2:
            risk = "MEDIUM"
            confidence = 0.65

        else:
            risk = "LOW"
            confidence = 0.4

        # -----------------------------
        # BUILD RESULT (XAI)
        # -----------------------------
        results[pillar] = {
            "risk": risk,
            "confidence": confidence,
            "details": {
                "policy_count": p,
                "action_count": a,
                "metric_count": m,
                "policy_ratio": round(policy_ratio, 3),
                "action_ratio": round(action_ratio, 3),
                "metric_ratio": round(metric_ratio, 3)
            },
            "explanation": build_greenwashing_explanation(
                risk, p, a, m, policy_ratio, metric_ratio
            )
        }

    return results


# -----------------------------
# EXPLANATION ENGINE (XAI)
# -----------------------------
def build_greenwashing_explanation(risk, p, a, m, pr, mr):
    """
    Generate human-readable explanation for greenwashing detection.
    """

    base = f"Detected {p} policy, {a} action, and {m} metric statements."

    if risk == "HIGH":
        return (
            base +
            " Strong dominance of policy-level claims with minimal supporting "
            "actions or measurable outcomes indicates potential greenwashing."
        )

    elif risk == "MEDIUM":
        return (
            base +
            " Moderate policy emphasis with limited quantitative metrics suggests "
            "partial disclosure and possible overstatement."
        )

    else:
        return (
            base +
            " Balanced presence of policies, actions, and metrics suggests "
            "credible ESG disclosure."
        )