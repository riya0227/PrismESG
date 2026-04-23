# ---------- Imports ----------
from .pdf_loader import extract_pages
from .chunking import chunk_page
from .vectorizer import build_tfidf_vectors
from .esg_labeler import label_chunks
from .classifier import train_esg_classifier, predict_esg
from .embeddings import build_embeddings

from sklearn.metrics import classification_report, accuracy_score


# ---------- Core Pipeline ----------
def ingest_pdf(pdf_path: str, document_id: str):
    """
    Full ingestion pipeline:
    PDF → pages → cleaned chunks
    """
    all_chunks = []

    for page_number, text in extract_pages(pdf_path):
        page_chunks = chunk_page(
            document_id=document_id,
            page_number=page_number,
            raw_text=text
        )
        all_chunks.extend(page_chunks)

    return all_chunks


# ---------- SINGLE MAIN TEST BLOCK ----------
if __name__ == "__main__":

    pdf_path = "/Users/dhruvieshah/Desktop/capstone/HUL_2023-2024_BRSR.pdf"
    doc_id = "TEST_DOC"

    # Module 0 — Ingestion
    chunks = ingest_pdf(pdf_path, doc_id)
    print(f"Total chunks created: {len(chunks)}\n")

    # Module 1 — TF‑IDF
    vectorizer, vectors = build_tfidf_vectors(chunks)
    print("TF-IDF matrix shape:", vectors.shape)

    # Module 2A — Weak ESG Labels
    labeled_chunks = label_chunks(chunks)

    # Module 2B — Train Classifier
    model, encoder = train_esg_classifier(vectors, labeled_chunks)
    print("\nClassifier trained successfully!")
    print("Classes learned:", encoder.classes_)

    # Module 2C — Predictions
    predictions = predict_esg(model, encoder, vectors)

    print("\nSample Predictions:\n")
    for i in range(10):
        print(predictions[i], "=>", chunks[i].text[:80])

    # Evaluation Step
    true_labels = [item["esg_label"] for item in labeled_chunks]

    filtered_true = []
    filtered_pred = []

    for t, p in zip(true_labels, predictions):
        if t != "UNCLASSIFIED":
            filtered_true.append(t)
            filtered_pred.append(p)

    print("\nEvaluation Results:")
    print("Accuracy:", accuracy_score(filtered_true, filtered_pred))
    print("\nClassification Report:\n")
    print(classification_report(filtered_true, filtered_pred))

    # Module 3 — Embeddings (Deep Learning Layer)
    embeddings = build_embeddings(chunks)
    print("\nEmbedding matrix shape:", embeddings.shape)

from .retrieval import semantic_search

print("\n--- Semantic Search Test ---")

query = "climate change and emissions reduction strategy"

results = semantic_search(query, embeddings, chunks)

for r in results:
    print(r["score"], "=>", r["text"][:80])

from .rag_engine import generate_esg_answer
from .retrieval import semantic_search

print("\n--- RAG Answer Test ---")

query = "What are the company's greenhouse gas emissions?"

results = semantic_search(query, embeddings, chunks)

# take top retrieved chunk texts
top_texts = [r["text"] for r in results]

answer = generate_esg_answer(query, top_texts)

print(answer)
