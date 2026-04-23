# analysis/scoring_service.py

from storage.document_store import load_document
from analysis.scoring_engine import compute_esg_score
from analysis.explanation_engine import explain_score_with_llm


def get_document_score(doc_id, llm):
    """
    Full ESG scoring pipeline:
    - Load document
    - Compute score
    - Generate explanation
    """

    # -------- LOAD DOCUMENT --------
    doc = load_document(doc_id)

    if not doc or "chunks" not in doc:
        return {
            "score": 0,
            "rating": "Poor",
            "breakdown": {},
            "explanation": "Document not found or invalid."
        }

    chunks = doc["chunks"]

    if not chunks:
        return {
            "score": 0,
            "rating": "Poor",
            "breakdown": {},
            "explanation": "No usable content in document."
        }

    # -------- COMPUTE SCORE --------
    score_data = compute_esg_score(chunks)

    # -------- SELECT TOP CHUNKS (for explanation) --------
    top_chunks = chunks[:20]  # simple heuristic (can improve later)

    # -------- GENERATE EXPLANATION --------
    explanation = explain_score_with_llm(
        score_data,
        top_chunks,
        llm
    )

    return {
        "score": score_data["score"],
        "rating": score_data["rating"],
        "breakdown": score_data["breakdown"],
        "explanation": explanation.get("explanation", explanation)
    }