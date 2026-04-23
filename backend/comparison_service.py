# analysis/comparison_service.py

from analysis.comparison_engine import compare_documents
from storage.document_store import load_document


def compare_with_llm(doc_id_1, doc_id_2, pam_data_1, pam_data_2, llm):
    """
    Full ESG comparison pipeline with LLM explanation
    """

    # -------- LOAD DOCUMENTS --------
    doc1 = load_document(doc_id_1)
    doc2 = load_document(doc_id_2)

    # -------- CORE COMPARISON --------
    comparison = compare_documents(
        doc1,
        doc2,
        pam_data_1,
        pam_data_2,
        llm=llm
    )

    # -------- OPTIONAL EXTRA LLM SUMMARY --------
    prompt = f"""
You are an ESG analyst.

Compare two companies based on structured ESG analysis.

Scores:
Doc1: {comparison['scores_doc1']}
Doc2: {comparison['scores_doc2']}

Pillar Comparison:
{comparison['pillar_comparison']}

Greenwashing Risk:
{comparison['greenwashing_comparison']}

Final Winner:
{comparison['winner']}

Explain:
- Which company performs better
- Why (based on ESG pillars)
- Any risks or weaknesses

Keep it clear and professional.
"""

    llm_summary = llm.generate(prompt)

    return {
        "structured_comparison": comparison,
        "llm_summary": llm_summary
    }