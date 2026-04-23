# ingestion/pipeline.py

from .pdf_loader import extract_pages
from .chunking import chunk_page
from .vectorizer import build_tfidf_vectors
from .embeddings import build_embeddings

from document_store import save_document

import faiss
import numpy as np


def process_pdf(pdf_path: str, document_id: str):

    all_chunks = []

    # -------- Extract + Chunk --------
    for page_number, text in extract_pages(pdf_path):
        page_chunks = chunk_page(
            document_id=document_id,
            page_number=page_number,
            raw_text=text
        )
        all_chunks.extend(page_chunks)

    print(f"✅ Total chunks: {len(all_chunks)}")

    # -------- TF-IDF --------
    vectorizer, vectors = build_tfidf_vectors(all_chunks)
    print("✅ TF-IDF built")

    # -------- Embeddings --------
    embeddings = build_embeddings(all_chunks)
    print("✅ Embeddings built")

    # -------- FAISS --------
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    print("✅ FAISS index built")

    # -------- SAVE PER DOCUMENT --------
    save_document(
        document_id=document_id,
        data={
            "chunks": all_chunks,
            "vectorizer": vectorizer,
            "vectors": vectors,
            "embeddings": embeddings
        },
        index=index
    )

    print(f"💾 Saved document: {document_id}")

    return {
        "faiss_index": index,
        "chunks": all_chunks
    }


# -------- RUN SCRIPT --------
if __name__ == "__main__":
    process_pdf(
        pdf_path="data/sample.pdf",
        document_id="doc1"
    )