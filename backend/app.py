# app.py

import streamlit as st
from chatbot import answer_query
from llm import HybridLLM
from storage.document_store import load_document, list_documents
from ingestion.embeddings import get_model

# -------- INIT --------
st.set_page_config(page_title="ESG Assistant", layout="wide")

st.title("📊 Explainable ESG Assistant")

llm = HybridLLM(mode="gemini")
embedding_model = get_model()

# -------- DOCUMENT SELECTION --------
documents = list_documents()

if not documents:
    st.warning("No documents found. Please process a PDF first.")
    st.stop()

selected_doc = st.selectbox("Select Document", documents)

doc = load_document(selected_doc)

faiss_index = doc["faiss_index"]
chunks = doc["chunks"]

# -------- QUERY INPUT --------
query = st.text_input("Ask a question")

# -------- RUN QUERY --------
if query:
    result = answer_query(
        query,
        faiss_index,
        chunks,
        embedding_model,
        llm
    )

    # -------- DISPLAY --------
    st.write("## 🧾 Answer")
    st.write(result["answer"])

    st.write("## 🔍 Evidence")
    for s in result["evidence"]:
        st.write(f"- {s['text']} (Page {s['page_number']})")

    st.write("## 🧠 Reasoning")
    for r in result["reasoning"]:
        st.write(f"- {r}")

    st.write("## 📊 Confidence")
    st.write(result["confidence"])