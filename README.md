# 🧠 DocuMind AI — RAG Document Intelligence System

A production-grade **Retrieval-Augmented Generation (RAG)** application that lets you upload any PDF documents and ask questions with **full source citations**. Built with LangChain-style architecture using FAISS, Sentence Transformers, and free LLMs (Groq/Gemini).

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red) ![FAISS](https://img.shields.io/badge/FAISS-Vector%20DB-orange) ![LLM](https://img.shields.io/badge/LLM-Groq%20%7C%20Gemini-purple)

---

## 🏗 Architecture

```
PDF Upload
    │
    ▼
┌─────────────────────────────────────────────┐
│              RAG PIPELINE                   │
│                                             │
│  1. PDF Parser (PyPDF2)                     │
│     └─► Extract text per page              │
│                                             │
│  2. Text Chunker                            │
│     └─► Split into overlapping chunks      │
│         (configurable size + overlap)       │
│                                             │
│  3. Embedding Model (SentenceTransformers)  │
│     └─► all-MiniLM-L6-v2 (runs locally)   │
│         Convert chunks → dense vectors      │
│                                             │
│  4. FAISS Vector Index                      │
│     └─► IndexFlatIP (cosine similarity)    │
│         Fast nearest-neighbor search        │
│                                             │
│  5. Retriever                               │
│     └─► Query → embed → top-k search      │
│                                             │
│  6. LLM Generator (Groq / Gemini)           │
│     └─► Context + Query → Cited Answer     │
└─────────────────────────────────────────────┘
    │
    ▼
Answer + Source Citations
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/documind-ai.git
cd documind-ai
pip install -r requirements.txt
```

### 2. Get a Free API Key

**Option A — Groq (Recommended, Fastest)**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up → Create API Key
3. Free tier: 14,400 requests/day

**Option B — Google Gemini**
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Get API Key → Free tier available

### 3. Run the App

```bash
streamlit run app.py
```

### 4. Use It
1. Paste your API key in the sidebar
2. Upload one or more PDFs
3. Click "Process Documents"
4. Ask any question!

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Semantic Search | Vector similarity search, not keyword matching |
| 📌 Source Citations | Every answer cites exact page & document |
| 📄 Multi-PDF | Query across multiple documents simultaneously |
| ⚡ Free LLMs | Groq (LLaMA 3) and Gemini 1.5 Flash — both free |
| 🔧 Configurable | Adjust chunk size, overlap, and top-k retrieval |
| 💬 Chat History | Full conversation memory within session |
| ⬇ Export | Download your Q&A session as text |
| 🏠 Local Embeddings | Embeddings run locally (no API cost for indexing) |

---

## 🧰 Tech Stack

| Component | Technology | Why |
|---|---|---|
| UI | Streamlit | Fast, Python-native dashboards |
| PDF Parsing | PyPDF2 | Reliable PDF text extraction |
| Embeddings | SentenceTransformers (MiniLM) | Free, fast, high-quality local embeddings |
| Vector DB | FAISS (Facebook AI) | Industry-standard, runs locally, extremely fast |
| LLM | Groq (LLaMA 3) / Gemini | Free tier, production quality |

---

## 📁 Project Structure

```
documind-ai/
├── app.py              # Streamlit UI + session management
├── rag_engine.py       # Core RAG pipeline (parsing, chunking, embedding, retrieval, generation)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🔬 How RAG Works (For Interviews)

**The Problem with plain LLMs:**
LLMs have a knowledge cutoff and can't access your private documents.

**RAG Solution:**
1. **Index time**: Convert your documents into vector embeddings stored in FAISS
2. **Query time**: Embed the question → find similar document chunks → inject as context → LLM answers from context

**Why this beats keyword search:**
Semantic embeddings capture *meaning*, not just exact words. "revenue decline" will match chunks about "sales dropped" even without shared keywords.

---

## 🎯 Resume Talking Points

- *"Built end-to-end RAG pipeline from scratch without LangChain abstractions — implemented custom chunking, FAISS indexing, and prompt engineering"*
- *"Used cosine similarity with FAISS IndexFlatIP for sub-millisecond retrieval across 1000+ document chunks"*
- *"Integrated dual LLM support (Groq/Gemini) with provider-agnostic architecture"*
- *"Reduced hallucination by constraining LLM to retrieved context only, with source attribution"*

---

## 🛠 Possible Extensions

- [ ] Add chat memory (multi-turn conversations)
- [ ] Support .docx, .txt, .csv file types
- [ ] Add HyDE (Hypothetical Document Embeddings) for better retrieval
- [ ] Deploy to Streamlit Cloud / Hugging Face Spaces
- [ ] Add reranking with cross-encoders
- [ ] Metadata filtering (filter by document or page range)

---

## 📄 License

MIT License — free to use and extend.
