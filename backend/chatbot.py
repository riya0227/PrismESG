# chatbot.py

from xai_engine import (
    split_into_sentences,
    rank_sentences,
    build_reasoning,
    compute_confidence,
)

from storage.document_store import load_document
import numpy as np


def answer_query(query, document_id, embedding_model, llm, top_k=5):

    # -------- VALIDATE INPUT --------
    if not query or not query.strip():
        return {
            "answer": "Query cannot be empty.",
            "evidence": [],
            "reasoning": [],
            "confidence": 0.0
        }

    # -------- LOAD DOCUMENT --------
    doc = load_document(document_id)
    faiss_index = doc["faiss_index"]
    chunks = doc["chunks"]

    if not chunks or faiss_index.ntotal == 0:
        return {
            "answer": "No data available for this document.",
            "evidence": [],
            "reasoning": [],
            "confidence": 0.0
        }

    # -------- EMBED QUERY --------
    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    )
    query_embedding = np.array(query_embedding).astype("float32")

    # -------- RETRIEVE --------
    distances, indices = faiss_index.search(query_embedding, top_k)

    retrieved_chunks = []
    for idx in indices[0]:
        if idx < 0 or idx >= len(chunks):
            continue
        retrieved_chunks.append(chunks[idx])

    if not retrieved_chunks:
        return {
            "answer": "No relevant information found.",
            "evidence": [],
            "reasoning": [],
            "confidence": 0.0
        }

    # -------- SENTENCE SPLIT --------
    sentences = split_into_sentences(retrieved_chunks)

    if not sentences:
        return {
            "answer": "No relevant information found.",
            "evidence": [],
            "reasoning": [],
            "confidence": 0.0
        }

    # -------- EMBED SENTENCES --------
    sentence_texts = [s["text"] for s in sentences]

    sentence_embeddings = embedding_model.encode(
        sentence_texts,
        normalize_embeddings=True
    )
    sentence_embeddings = np.array(sentence_embeddings).astype("float32")

    # -------- RANK --------
    ranked = rank_sentences(
        query_embedding,
        sentence_embeddings,
        sentences
    )

    top_sentences = ranked[:5]

    # -------- XAI --------
    reasoning = build_reasoning(query, top_sentences)
    confidence = compute_confidence(top_sentences)

    # -------- BUILD PROMPT --------
    evidence_text = "\n".join([
        f"- {s['text']} (Page {s['page_number']})"
        for s in top_sentences
    ])

    prompt = f"""
You are an ESG analyst.

Answer using ONLY the evidence.

Question:
{query}

Evidence:
{evidence_text}

Return EXACTLY:

Answer:
<answer>

Evidence:
- <sentence>

Explanation:
<why this evidence supports answer>
"""

    # -------- LLM --------
    answer = llm.generate(prompt)

    return {
        "answer": answer,
        "evidence": top_sentences,
        "reasoning": reasoning,
        "confidence": float(confidence)
    }