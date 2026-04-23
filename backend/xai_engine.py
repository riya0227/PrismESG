# xai_engine.py

from typing import List
import numpy as np
import re


# -----------------------------
# SENTENCE SPLITTING (IMPROVED)
# -----------------------------
def split_into_sentences(chunks):
    sentences = []

    for chunk in chunks:
        text = chunk.get("text", "")

        # better sentence split
        parts = re.split(r'(?<=[.!?]) +', text)

        for p in parts:
            p = p.strip()

            if len(p) > 30:  # filter noise
                sentences.append({
                    "text": p,
                    "page_number": chunk.get("page_number")
                })

    return sentences


# -----------------------------
# RANK SENTENCES
# -----------------------------
def rank_sentences(query_embedding, sentence_embeddings, sentences, top_k=5):
    """
    Rank sentences by cosine similarity
    """

    # normalize (important for cosine similarity)
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    sent_norm = sentence_embeddings / np.linalg.norm(sentence_embeddings, axis=1, keepdims=True)

    scores = np.dot(sent_norm, query_norm.T).flatten()

    ranked_idx = np.argsort(scores)[::-1][:top_k]

    return [
        {
            "text": sentences[i]["text"],
            "page_number": sentences[i]["page_number"],
            "score": float(scores[i])
        }
        for i in ranked_idx
    ]


# -----------------------------
# BUILD REASONING (XAI)
# -----------------------------
def build_reasoning(query: str, sentences):
    """
    Explain WHY each sentence was selected
    """

    reasoning = []

    # remove stopwords manually (simple version)
    stopwords = {"what", "is", "the", "are", "of", "in", "on", "for", "a", "an"}
    query_words = [
        w for w in query.lower().split()
        if w not in stopwords and len(w) > 2
    ]

    for s in sentences:
        text = s["text"].lower()

        matches = [w for w in query_words if w in text]

        if matches:
            reasoning.append(
                f"Matches key terms: {', '.join(matches)}"
            )
        else:
            reasoning.append(
                "Selected due to semantic similarity"
            )

    return reasoning


# -----------------------------
# CONFIDENCE SCORE
# -----------------------------
def compute_confidence(sentences):
    """
    Compute confidence score (0–1)
    """

    if not sentences:
        return 0.0

    scores = [s.get("score", 0) for s in sentences]

    avg_score = float(np.mean(scores))

    # normalize roughly to 0–1
    confidence = min(max(avg_score, 0), 1)

    return round(confidence, 2)