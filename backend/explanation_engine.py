# analysis/explanation_engine.py

def explain_score_with_llm(score_data, top_chunks, llm):
    """
    Generate explainable ESG score interpretation using LLM.
    """

    if not score_data:
        return {
            "explanation": "No score data available.",
            "confidence": 0.0
        }

    # -------- SAFE CONTEXT BUILD --------
    context_text = " ".join([
        c.get("text", "")
        for c in top_chunks[:15]   # ✅ smaller, more focused
        if c.get("text")
    ])

    # -------- EXTRACT STRUCTURED DATA --------
    score = score_data.get("score", {})
    breakdown = score_data.get("breakdown", {})
    rating = score_data.get("rating", "N/A")

    # -------- PROMPT --------
    prompt = f"""
You are an ESG analyst.

A company has received the following ESG evaluation:

Overall Score:
{score}

Rating:
{rating}

Breakdown (E, S, G):
{breakdown}

Using the context below, explain clearly:

1. Why this score was given
2. What the company is doing well
3. What is weak or missing
4. Specific improvements needed

Be factual and base your reasoning ONLY on the context.

Context:
{context_text}
"""

    # -------- LLM CALL --------
    explanation = llm.generate(prompt)

    return {
        "explanation": explanation,
        "confidence": 0.8  # optional fixed or computed later
    }