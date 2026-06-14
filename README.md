# Financial Document AI Assistant

A privacy-preserving RAG (Retrieval-Augmented Generation) application for querying financial documents using local LLM inference — no cloud APIs, no data leaves your machine.

![Stack](https://img.shields.io/badge/React-Frontend-blue) ![Stack](https://img.shields.io/badge/Node.js-Backend-green) ![Stack](https://img.shields.io/badge/Llama_3.2-LLM-orange) ![Stack](https://img.shields.io/badge/Ollama-Inference-red)

## What it does

Upload any financial PDF (10-K, earnings report, policy document) and ask questions about it in plain English. The system retrieves the most relevant sections and generates accurate, grounded answers using a locally-running Llama 3.2 model.

**Example queries:**
- *"What were Tesla's total revenues in 2025?"*
- *"What are the main risk factors mentioned?"*
- *"What does management say about the energy storage business?"*

## Architecture

```
PDF Upload → Text Extraction → Chunking (1500 chars, 200 overlap)
     ↓
Embedding (nomic-embed-text via Ollama)
     ↓
In-Memory Vector Store (custom cosine similarity search)
     ↓
Top-K Chunk Retrieval → Prompt Engineering → Llama 3.2 (local)
     ↓
Answer → React Chat UI
```

## Tech Stack

**Frontend**
- React + Vite
- Drag-and-drop PDF upload
- Real-time chat interface with typing indicators

**Backend**
- Node.js + Express REST API
- `pdf-parse` for text extraction
- `@langchain/textsplitters` for recursive chunking
- Custom cosine similarity vector search (no external vector DB dependency)
- `@langchain/ollama` for embeddings and LLM inference

**Models (via Ollama — fully local)**
- `nomic-embed-text` — document and query embeddings
- `llama3.2` — answer generation

## Why local inference?

Financial documents contain sensitive data. Running everything on-device means:
- Zero data transmitted to third-party APIs
- No per-token costs
- Works fully offline
- Suitable for regulated environments

## Getting Started

### Prerequisites
- Node.js 18+
- [Ollama](https://ollama.com) installed and running

### 1. Pull required models
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 2. Clone and install
```bash
git clone https://github.com/RishithaReddy-stack/fin-doc-assistant.git
cd fin-doc-assistant

# Install backend dependencies
cd backend && npm install

# Install frontend dependencies
cd ../frontend && npm install
```

### 3. Configure environment
```bash
cd backend
cp .env.example .env
# Edit .env if needed (default port is 3001)
```

### 4. Run the app
```bash
# Terminal 1 — Start Ollama
ollama serve

# Terminal 2 — Start backend
cd backend && node server.js

# Terminal 3 — Start frontend
cd frontend && npm run dev
```

Open `http://localhost:5173` in your browser.

## How it works

1. **Upload** — PDF is sent to the backend via multipart form upload
2. **Extract** — `pdf-parse` extracts raw text from the PDF
3. **Chunk** — Text is split into 1500-character overlapping chunks using `RecursiveCharacterTextSplitter`
4. **Embed** — Each chunk is embedded using `nomic-embed-text` running locally via Ollama
5. **Store** — Chunk embeddings are stored in memory with a unique document ID
6. **Query** — User question is embedded, cosine similarity is computed against all chunks, top 8 are retrieved
7. **Generate** — Retrieved chunks are injected into a prompt and sent to Llama 3.2 for answer generation

## Project Structure

```
fin-doc-assistant/
├── backend/
│   ├── server.js        # Express API — upload and chat endpoints
│   ├── .env.example     # Environment variable template
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main React component — upload flow and chat UI
│   │   └── index.css    # Styles
│   └── package.json
├── tesla/               # Sample Tesla 10-K PDF for testing
├── ragService.js        # Core RAG logic — chunking, embedding, retrieval, generation
└── README.md
```

## Limitations

- Vector store is in-memory — documents are cleared on server restart
- Optimized for text-based PDFs; scanned documents require OCR preprocessing
- Response speed depends on local hardware (Apple Silicon recommended)
