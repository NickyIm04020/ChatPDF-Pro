# 📄 ChatPDF Pro – Enterprise RAG QA System

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-v0.3-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-teal?logo=fastapi)
![Pinecone](https://img.shields.io/badge/VectorDB-Pinecone-orange)

---

## 🧩 Overview
**ChatPDF Pro** is a **production-grade Retrieval-Augmented Generation (RAG)** system designed to query large collections of PDF documents with **high accuracy and traceability**.

It solves the common **context loss and hallucination problem** in LLMs by combining **semantic vector search** with **multi-turn conversational memory** and **source-level citations** (page numbers).

---

## ⚡ Key Features
- **Multi-PDF Ingestion:** Parallel PDF processing using `PyPDFLoader` with optimized latency  
- **Semantic Retrieval:** OpenAI embeddings with Pinecone serverless vector storage  
- **Context-Aware Q&A:** Maintains conversational state across follow-up questions  
- **Intelligent Chunking:** Tuned chunking strategy for maximum context retention  
- **Citation Tracking:** Every answer includes source filename + page number  
- **API-First Design:** FastAPI backend ready for web or mobile frontends  

---

## 🧠 How It Works
1. PDFs are parsed, chunked, and converted into vector embeddings  
2. Embeddings are stored in Pinecone for fast semantic retrieval  
3. User queries retrieve the most relevant chunks  
4. GPT generates grounded answers using retrieved context  
5. Responses include **verifiable citations** to prevent hallucinations  

---

## 🛠️ Tech Stack
- **Language:** Python 3.11  
- **Framework:** FastAPI + Uvicorn  
- **LLM Orchestration:** LangChain (v0.3)  
- **Embeddings & LLM:** OpenAI (GPT-4, text-embedding-3-small)  
- **Vector Database:** Pinecone (Serverless)  

---

## 📂 Project Structure
```

ChatPDF-Pro/
├── app/
│ ├── main.py # FastAPI application entry point
│ ├── ingest.py # PDF parsing, chunking, and vector upsert
│ └── rag.py # RAG pipeline with retrieval + memory
├── documents/ # Temporary PDF storage
├── requirements.txt # Dependencies
└── .env # API keys & environment config
````

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ChatPDF-Pro.git
cd ChatPDF-Pro
pip install -r requirements.txt
````
2️⃣ Configure Environment
```bash
Copy code
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=your_index_name
````
3️⃣ Run the Server
```bash
Copy code
uvicorn app.main:app --reload
````
📡 API Usage Example
```bash
POST /query
{
  "question": "What are the key conclusions in this document?"
}

````
Response
```json
{
  "answer": "The document concludes that...",
  "sources": [
    {
      "file": "report.pdf",
      "page": 12
    }
  ]
}
````
---

## 💡 Why This Project Matters
- **Real-World RAG Design:** Demonstrates end-to-end retrieval-augmented generation system architecture  
- **LLM Reliability:** Shows effective grounding and hallucination control using citations  
- **Enterprise Applicability:** Suitable for enterprise search, legal documents, research papers, and internal knowledge bases  
- **Production Readiness:** Strong example of scalable, production-grade AI backend engineering  

---
