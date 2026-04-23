# analysis/gap_detection.py

from collections import defaultdict


def detect_esg_gaps(structured_data):
    """
    Detect ESG disclosure gaps using Policy-Action-Metric structure.

    Args:
        structured_data (list): List of dicts with keys:
            - pillar
            - principle
            - type (Policy / Action / Metric)
            - text

    Returns:
        list: Gap analysis results (XAI-ready)
    """

    # ---- Group by Principle ----
    principle_data = defaultdict(lambda: {"Policy": 0, "Action": 0, "Metric": 0})

    for item in structured_data:
        principle = item.get("principle")
        category = item.get("type")

        if principle and category in ["Policy", "Action", "Metric"]:
            principle_data[principle][category] += 1

    gaps = []

    # ---- Gap Logic ----
    for principle, counts in principle_data.items():

        policy_count = counts.get("Policy", 0)
        action_count = counts.get("Action", 0)
        metric_count = counts.get("Metric", 0)

        total = policy_count + action_count + metric_count

        # 🚨 Case 1: Only policy
        if policy_count > 0 and action_count == 0 and metric_count == 0:
            gaps.append(build_gap(
                principle,
                issue="Only policy statements",
                reason="No actions or measurable metrics provided",
                severity="HIGH",
                counts=counts
            ))

        # 🚨 Case 2: Policy + Action but no metrics
        elif policy_count > 0 and action_count > 0 and metric_count == 0:
            gaps.append(build_gap(
                principle,
                issue="Missing quantitative metrics",
                reason="Actions mentioned but no measurable evidence",
                severity="MEDIUM",
                counts=counts
            ))

        # 🚨 Case 3: Very low content
        elif total <= 1:
            gaps.append(build_gap(
                principle,
                issue="Insufficient disclosure",
                reason="Very limited ESG information provided",
                severity="HIGH",
                counts=counts
            ))

        # 🚨 Case 4: Action but no policy (rare but important)
        elif action_count > 0 and policy_count == 0:
            gaps.append(build_gap(
                principle,
                issue="Action without policy backing",
                reason="Activities mentioned but no formal ESG policy",
                severity="LOW",
                counts=counts
            ))

    return gaps


# -----------------------------
# HELPER: BUILD GAP OBJECT
# -----------------------------
def build_gap(principle, issue, reason, severity, counts):
    return {
        "principle": principle,
        "issue": issue,
        "reason": reason,
        "severity": severity,
        "confidence": map_severity_to_confidence(severity),
        "details": {
            "policy_count": counts.get("Policy", 0),
            "action_count": counts.get("Action", 0),
            "metric_count": counts.get("Metric", 0)
        },
        "explanation": generate_gap_explanation(issue, counts)
    }


# -----------------------------
# HELPER: CONFIDENCE
# -----------------------------
def map_severity_to_confidence(severity):
    mapping = {
        "HIGH": 0.9,
        "MEDIUM": 0.65,
        "LOW": 0.4
    }
    return mapping.get(severity, 0.5)


# -----------------------------
# HELPER: EXPLANATION (XAI)
# -----------------------------
def generate_gap_explanation(issue, counts):
    p = counts.get("Policy", 0)
    a = counts.get("Action", 0)
    m = counts.get("Metric", 0)

    return (
        f"{issue}: Found {p} policy, {a} action, and {m} metric entries. "
        "This imbalance indicates incomplete ESG disclosure."
    )