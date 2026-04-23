# analysis/comparison_engine.py

from analysis.esg_scorer import compute_esg_scores
from analysis.pillar_analysis import analyze_pillars
from analysis.greenwashing import detect_greenwashing


def compare_documents(doc1, doc2, pam_data1, pam_data2, llm=None):
    """
    Advanced ESG comparison engine:
    - ESG scores
    - Pillar strength
    - Greenwashing risk
    - Final verdict + explanation
    """

    # -------- ANALYSIS --------
    pillar1 = analyze_pillars(pam_data1)
    pillar2 = analyze_pillars(pam_data2)

    scores1 = compute_esg_scores(pillar1)
    scores2 = compute_esg_scores(pillar2)

    gw1 = detect_greenwashing(pam_data1)
    gw2 = detect_greenwashing(pam_data2)

    # -------- PILLAR COMPARISON --------
    pillar_comparison = []
    total1, total2 = 0, 0

    for pillar in ["E", "S", "G"]:
        s1 = scores1.get(pillar, 0)
        s2 = scores2.get(pillar, 0)

        total1 += s1
        total2 += s2

        if s1 > s2:
            pillar_comparison.append({
                "pillar": pillar,
                "winner": "doc1",
                "doc1_score": s1,
                "doc2_score": s2
            })
        elif s2 > s1:
            pillar_comparison.append({
                "pillar": pillar,
                "winner": "doc2",
                "doc1_score": s1,
                "doc2_score": s2
            })
        else:
            pillar_comparison.append({
                "pillar": pillar,
                "winner": "equal",
                "doc1_score": s1,
                "doc2_score": s2
            })

    # -------- GREENWASHING COMPARISON --------
    gw_comparison = []

    for pillar in ["E", "S", "G"]:
        r1 = gw1.get(pillar, {}).get("risk", "UNKNOWN")
        r2 = gw2.get(pillar, {}).get("risk", "UNKNOWN")

        gw_comparison.append({
            "pillar": pillar,
            "doc1_risk": r1,
            "doc2_risk": r2
        })

    # -------- FINAL VERDICT --------
    if total1 > total2:
        winner = "Document 1"
    elif total2 > total1:
        winner = "Document 2"
    else:
        winner = "Tie"

    # -------- XAI EXPLANATION --------
    explanation = build_comparison_explanation(
        pillar_comparison,
        gw_comparison,
        winner
    )

    # -------- OPTIONAL LLM SUMMARY (🔥) --------
    llm_summary = None
    if llm:
        llm_summary = generate_llm_comparison(
            pillar_comparison,
            gw_comparison,
            winner,
            llm
        )

    return {
        "scores_doc1": scores1,
        "scores_doc2": scores2,
        "pillar_comparison": pillar_comparison,
        "greenwashing_comparison": gw_comparison,
        "total_score_doc1": round(total1, 2),
        "total_score_doc2": round(total2, 2),
        "winner": winner,
        "explanation": explanation,
        "llm_summary": llm_summary
    }


# -----------------------------
# XAI EXPLANATION
# -----------------------------
def build_comparison_explanation(pillar_comp, gw_comp, winner):
    insights = []

    for p in pillar_comp:
        if p["winner"] == "doc1":
            insights.append(f"{p['pillar']}: Document 1 outperforms Document 2.")
        elif p["winner"] == "doc2":
            insights.append(f"{p['pillar']}: Document 2 outperforms Document 1.")

    for g in gw_comp:
        if g["doc1_risk"] != g["doc2_risk"]:
            insights.append(
                f"{g['pillar']}: Greenwashing risk differs "
                f"(Doc1={g['doc1_risk']}, Doc2={g['doc2_risk']})"
            )

    return f"{winner} performs better overall. " + " ".join(insights)


# -----------------------------
# LLM COMPARISON (🔥 FEATURE)
# -----------------------------
def generate_llm_comparison(pillar_comp, gw_comp, winner, llm):
    prompt = f"""
You are an ESG analyst.

Compare two ESG reports using the following data:

Pillar Comparison:
{pillar_comp}

Greenwashing:
{gw_comp}

Final Winner: {winner}

Explain clearly:
- Which company is better
- Why (based on ESG strength)
- Any risks (greenwashing, weak metrics)

Keep it concise and professional.
"""

    return llm.generate(prompt)