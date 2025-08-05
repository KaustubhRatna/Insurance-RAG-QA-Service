# Insurance RAG QA Service

An end-to-end Retrieval-Augmented Generation (RAG) system for querying large insurance-domain documents. It ingests PDFs (and other supported formats), semantically indexes them, and answers natural-language questions using context retrieved from both existing and newly uploaded policy documents.

---

## 🚀 Features

* **Document Ingestion**

  * Supports PDF (plain-text via `pdfplumber` or Markdown via `pymupdf4llm`), DOCX, TXT, and EML.
  * Automatically downloads from any HTTP(s) URL.

* **Smart Chunking**

  * Uses a character-based recursive splitter (`langchain`) with custom separators for Markdown semantics.
  * Configurable chunk size and overlap to match your embedding model’s context window.

* **Domain-Specific Embeddings**

  * Leverages a locally-hosted HuggingFace Sentence-Transformer fine-tuned on insurance data.
  * Fast GPU/CPU inference via `sentence-transformers`.

* **Vector Store with FAISS**

  * On-disk FAISS index + pickle metadata for persistent storage.
  * In-memory FAISS for newly uploaded docs, then merges into the main store.
  * Cosine (L2) retrieval of top-k relevant chunks.

* **RAG Prompt Assembly**

  * Combines “new” document context (if provided) with existing global context.
  * Deduplicates overlapping chunks.
  * Produces clear, instruction-driven prompts that constrain the LLM to only use provided context.

* **LLM Integration**

  * Async calls to Google Gemini QnA endpoint via `httpx`.
  * Exponential backoff + retry logic for transient errors (5xx, timeouts).
  * Strips numbering and whitespace from generated answers.

* **Secure API**

  * FastAPI server with a bearer-token auth dependency.
  * Health-check endpoint.
  * Pydantic request/response models for strict validation.

---

## 🏗️ Architecture Overview

```
Client Request
   └── POST /api/v1/hackrx/run
         ├─ Headers: Authorization: Bearer <AUTH_TOKEN>
         └─ Body: { documents: "<URL>", questions: ["Q1", "Q2", …] }

main.py (FastAPI)
 ├─ verify_token()    # checks AUTH_TOKEN
 ├─ generate_prompts() # in rag_system.py
 │    ├─ load persistent FAISS store
 │    ├─ if documents provided:
 │    │     ├─ download & parse (document_parser.py)
 │    │     ├─ chunk (text_chunker.py)
 │    │     ├─ dedupe against persistent .texts
 │    │     ├─ embed_texts() → local BERT model
 │    │     └─ build in-memory FAISS index
 │    ├─ for each question:
 │    │     ├─ embed_query() → local BERT model
 │    │     ├─ search new & existing FAISS stores
 │    │     ├─ dedupe & assemble context
 │    │     └─ build instruction-driven prompt
 │    └─ if new chunks exist & ALLOW_DB_UPDATE:
 │          └─ merge them into persistent FAISS store
 ├─ call_gemini_api()  # in embedder/llm.py
 │    ├─ POST to Gemini QnA endpoint
 │    ├─ retry on 5xx / timeouts with exponential backoff
 │    └─ extract candidates[0].content.parts[0].text
 └─ return JSON { answers: […] }

Persistent Storage:
 ├─ /vector_store/index.faiss
 └─ /vector_store/texts.pkl
```

---

## 🛠️ Tech Stack

* **Language & Framework**: Python 3.11 + [FastAPI](https://fastapi.tiangolo.com/)
* **Document Parsing**:

  * `pdfplumber` (plain text)
  * `pymupdf4llm` (Markdown conversion)
  * `python-docx` (DOCX)
* **Chunking**: `langchain.text_splitter.RecursiveCharacterTextSplitter`
* **Embeddings**: `sentence-transformers` (local BERT embed model)
* **Vector Search**: `faiss-cpu` for persistent on-disk and in-memory indexing
* **LLM Client**: `httpx.AsyncClient` → Google Gemini QnA API
* **Configuration & Secrets**: `pydantic-settings`, `.env` via `python-dotenv`
* **Containerization**: Docker + optional Docker Compose
* **Authentication**: Bearer token via FastAPI dependency

---

## ⚙️ Configuration

Copy the example `.env` file and fill in your secrets:

```dotenv
# .env
AUTH_TOKEN=your_custom_bearer_token
GEMINI_API_KEY=your_google_gemini_api_key
```

All other settings (chunk sizes, model paths, retry counts) live in [`config.py`](config.py).

---

## 📦 Installation & Local Run

1. **Clone & enter**

   ```bash
   git clone <repo-url>
   cd rag_insurance
   ```

2. **Create & activate** a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. **Install** dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare** your embedding model & vector store

   * Place your Sentence-Transformer model in `insurance_bert_embed/`
   * Create an empty `vector_store/` folder for FAISS artifacts

5. **Run** the server

   ```bash
   uvicorn main:app --reload --port 8000
   ```

6. **Test** your health and QA endpoints

   ```bash
   curl http://localhost:8000/health
   # POST /api/v1/hackrx/run with Bearer auth to get answers
   ```

---

## 🚢 Docker Deployment (in progress)

1. **Build** the image

   ```bash
   docker build -t rag-insurance .
   ```

2. **Run** (mount volumes for persistence/model)

   ```bash
   docker run -d \
     -p 8000:8000 \
     -e AUTH_TOKEN="$AUTH_TOKEN" \
     -e GEMINI_API_KEY="$GEMINI_API_KEY" \
     -v ./vector_store:/app/vector_store \
     -v ./insurance_bert_embed:/app/insurance_bert_embed \
     rag-insurance
   ```

---

## 🔄 Extensibility

* **Swap LLM**: point `generator/llm.py` at OpenAI or any other endpoint.
* **Alternative Vector Store**: swap FAISS for Chroma or Pinecone by implementing the same interface.
* **Enhanced Chunking**: adjust `separators` or integrate hierarchical splitting.
* **Multi‐Doc Queries**: accept arrays of URLs & merge their contexts in `generate_prompts()`.

---

Feel free to explore, customize, and extend!
