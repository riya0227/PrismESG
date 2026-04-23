# analysis/esg_scorer.py

def compute_esg_scores(pillar_data):
    """
    pillar_data: output from analyze_pillars()

    Returns:
    {
        "E": {
            "score": float,
            "breakdown": {...}
        },
        ...
    }
    """

    # -------- Configurable weights --------
    WEIGHTS = {
        "Policy": 1,
        "Action": 2,
        "Metric": 3
    }

    results = {}

    for pillar, data in pillar_data.get("scores", {}).items():

        counts = data.get("details", {})

        policy = counts.get("Policy", 0)
        action = counts.get("Action", 0)
        metric = counts.get("Metric", 0)

        total = policy + action + metric

        # -------- Handle empty --------
        if total == 0:
            results[pillar] = {
                "score": 0.0,
                "breakdown": {
                    "policy": 0,
                    "action": 0,
                    "metric": 0,
                    "reason": "No ESG evidence found"
                }
            }
            continue

        # -------- Weighted scoring --------
        weighted_sum = (
            policy * WEIGHTS["Policy"] +
            action * WEIGHTS["Action"] +
            metric * WEIGHTS["Metric"]
        )

        raw_score = weighted_sum / total  # range: 1–3

        # -------- Normalize to /10 --------
        final_score = round((raw_score / 3) * 10, 2)

        # -------- XAI breakdown --------
        results[pillar] = {
            "score": final_score,
            "breakdown": {
                "policy": policy,
                "action": action,
                "metric": metric,
                "weights": WEIGHTS,
                "raw_score": round(raw_score, 3),
                "explanation": build_score_explanation(
                    policy, action, metric, final_score
                )
            }
        }

    return results


# -----------------------------
# EXPLANATION ENGINE (XAI)
# -----------------------------
def build_score_explanation(policy, action, metric, score):
    """
    Generate human-readable explanation for ESG score.
    """

    if score == 0:
        return "No ESG-related disclosures found."

    explanation = []

    if metric > action and metric > policy:
        explanation.append("Strong presence of measurable ESG metrics.")
    elif action > policy:
        explanation.append("Focus on ESG actions and initiatives.")
    elif policy > 0:
        explanation.append("Primarily policy-level commitments.")

    if metric == 0:
        explanation.append("Lack of quantitative metrics reduces score.")

    if action == 0:
        explanation.append("Limited evidence of real-world implementation.")

    return " ".join(explanation)