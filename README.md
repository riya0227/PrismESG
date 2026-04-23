# 🌱 PrismESG — Explainable ESG Intelligence System

## 📌 Overview

PrismESG is an AI-powered platform designed to analyze ESG (Environmental, Social, Governance) reports and provide **explainable, data-driven insights**.
It goes beyond simple Q&A by offering **transparent reasoning, scoring, comparison, and risk detection**.

---

## 🚀 Key Features

### 🔍 1. ESG Question Answering (RAG-based)

* Ask natural language questions on ESG reports
* Retrieves relevant content using FAISS vector search
* Generates structured answers using LLMs
* Provides:

  * ✅ Answer
  * 📄 Evidence
  * 🧠 Reasoning
  * 📊 Confidence score

---

### 📊 2. ESG Scoring Engine

* Computes ESG score based on:

  * Emissions disclosure
  * Targets & commitments
  * Renewable energy usage
  * Transparency (metrics)
* Outputs:

  * Score (0–100)
  * Rating (Excellent / Good / Average / Poor)
  * Detailed breakdown

---

### 🧠 3. Explainable AI (XAI)

* Explains *why* an answer or score was generated
* Sentence-level ranking using embeddings
* Keyword + semantic reasoning
* Confidence estimation

---

### 🚨 4. Greenwashing Detection

* Identifies vague or misleading ESG claims
* Flags:

  * Missing metrics
  * Non-measurable commitments
* Helps assess credibility of reports

---

### 📌 5. ESG Insights Engine

* Extracts key ESG topics:

  * Emissions
  * Energy
  * Water
  * Waste
  * Governance
* Groups insights by category
* Highlights top disclosures

---

### ⚖️ 6. Document Comparison

* Compares ESG performance across companies
* Uses LLM to generate:

  * Structured comparison
  * Winner analysis
  * Key differences

---

### 💡 7. Strategy & Gap Analysis

* Detects missing ESG areas
* Suggests improvements
* Identifies risk exposure

---

## 🏗️ Architecture

```
PDF → Text Extraction → Chunking → Embeddings → FAISS Index
        ↓
   Retrieval (RAG)
        ↓
   XAI Engine (ranking + reasoning)
        ↓
   LLM (Gemini / Ollama)
        ↓
   Structured ESG Output
```

---

## 📁 Project Structure

```
backend/
│
├── analysis/          # ESG logic (scoring, gaps, strategy, etc.)
├── ingestion/         # PDF processing, chunking, embeddings
├── storage/           # Data storage + FAISS index
├── chatbot.py         # Main QA pipeline
├── views.py           # API layer
├── llm.py             # LLM wrapper (Gemini / Ollama)
├── xai_engine.py      # Explainability layer
│
requirements.txt
.gitignore
```

---

## ⚙️ Tech Stack

* Python
* FAISS (vector search)
* Sentence Transformers (embeddings)
* Gemini / Ollama (LLMs)
* Django (API layer)
* Streamlit (optional UI)

---

## ▶️ How to Run (Basic)

```bash
# Create environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend (if Django setup)
python manage.py runserver
```

---

## 🧪 Example Queries

* “What are the company’s emissions targets?”
* “Does the company use renewable energy?”
* “What ESG risks are mentioned?”
* “Compare sustainability strategies of two companies”

---

## 🎯 Use Cases

* ESG analysis for investors
* Sustainability benchmarking
* Risk assessment
* Corporate reporting evaluation

---

## 🧠 Key Highlight

> PrismESG doesn’t just answer — it **explains why the answer is correct**.

This makes it:

* Transparent
* Trustworthy
* Suitable for real-world ESG decision-making

---

## 📌 Future Improvements

* Fine-tuned ESG models
* Dashboard visualization
* Real-time ESG data integration
* Multi-document benchmarking

---

## 👩‍💻 Authors

* Dhruvie Shah
* Riya Singh
* Pragati Bist

---

## ⭐ If you found this useful

Give the repo a ⭐ and share feedback!
