# LandRight 🛬
### AI Copilot for International Students

> Built by an international student, for international students.
> Because figuring out the US shouldn't feel like solving a puzzle blindfolded.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-LLaMA3-orange?style=flat-square&logo=amazonaws)
![AWS S3](https://img.shields.io/badge/AWS_S3-Knowledge_Base-yellow?style=flat-square&logo=amazons3)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-purple?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-Anthropic-black?style=flat-square)

---

## What is this?

When you land in the US as an international student, nobody hands you a manual.
You're expected to figure out — in the right order — things like:

- Which eSIM to buy before you board
- How to open a bank account without an SSN
- What to bring to the DMV and in what order
- When you can apply for an SSN (hint: not right away)
- How OPT and CPT work before it's too late to plan

LandRight is an AI copilot that knows all of this and tells you exactly what
to do, in what order, based on your specific stage — in plain English, not government-speak.

---

## Demo

> Ask it anything:
> *"How do I open a bank account without an SSN?"*
> *"What do I need for my state ID?"*
> *"Explain OPT vs CPT like I'm 5"*
> *"What taxes do I need to file as an F1 student?"*

---

## How it works

```
User question
     ↓
Streamlit UI
     ↓
FastAPI backend
     ↓
LangGraph agent
     ↓
MCP server (exposes tools)
     ↓
Qdrant vector search (finds relevant knowledge)
     ↓
AWS S3 (knowledge base storage)
     ↓
AWS Bedrock / LLaMA3 (generates answer from retrieved context)
     ↓
Response
```

This is a full **RAG (Retrieval Augmented Generation)** pipeline:
1. **Retrieval** — Qdrant finds the most semantically relevant documents from the knowledge base using vector similarity search
2. **Augmentation** — retrieved documents are passed as context to the LLM
3. **Generation** — LLaMA3 via AWS Bedrock generates a grounded, conversational answer

---

## Tech stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | Streamlit | Fast to ship, perfect for AI apps |
| Backend | FastAPI | Industry standard, async-ready |
| Agent | LangGraph | State-managed agent orchestration |
| Tools | MCP (Anthropic) | Exposes knowledge base as callable tools |
| Vector DB | Qdrant | Fast, modern, free to self-host |
| Embeddings | sentence-transformers | Local, no API cost |
| LLM | AWS Bedrock (LLaMA3) | Enterprise-grade managed inference |
| Knowledge base | AWS S3 | Cloud storage, decoupled from application code |
| Language | Python 3.11 | — |

---

## MCP tools

The MCP server exposes three tools the agent can call:

| Tool | What it does |
|---|---|
| `search_docs(query)` | Semantic search over the knowledge base |
| `get_roadmap(stage)` | Returns ordered action steps for a given stage |
| `get_checklist(stage)` | Returns a checklist for a given stage |

---

## Knowledge base

Covers the full international student journey:

| Stage | Topics |
|---|---|
| Pre-arrival | eSIM setup, housing, lease checklist, scam red flags |
| Day 0 | SEVIS check-in, DSO meeting, I-20 validation |
| Week 1 | Bank account (no SSN needed), state ID, health insurance |
| Month 1 | Credit building, secured cards, financial foundations |
| Ongoing | SSN eligibility, taxes, OPT/CPT timelines, work authorisation |

---

## Project structure

```
landright/
├── backend/
│   ├── agents/          # LangGraph agent + conversation logic
│   ├── api/             # FastAPI routes and schemas
│   ├── core/            # Config, LLM setup, embeddings
│   ├── db/              # Qdrant vector DB client (loads from S3)
│   ├── knowledge/       # Knowledge base content
│   └── mcp/             # MCP server + tool definitions
├── frontend/
│   └── app.py           # Streamlit UI
├── scripts/
│   └── upload_knowledge_to_s3.py  # One-time S3 upload script
├── tests/               # pytest test suite
├── .github/workflows/   # CI/CD
└── docker-compose.yml
```

---

## Quickstart

### Prerequisites
- Python 3.11
- Docker
- AWS account with Bedrock and S3 access

```bash
# 1. Clone and set up
git clone https://github.com/RishithaReddy-stack/landright.git
cd landright
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Add your AWS credentials to .env

# 3. Upload knowledge base to S3 (one-time)
PYTHONPATH=. python scripts/upload_knowledge_to_s3.py

# 4. Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# 5. Index the knowledge base
PYTHONPATH=. python backend/db/qdrant.py

# 6. Run the app
PYTHONPATH=. streamlit run frontend/app.py
```

---

## Why I built this

I'm an international student. When I landed, I had no idea what to do first —
whether to get a SIM card, find housing, open a bank account, or go to the
international office. Nobody tells you the order. Nobody tells you the gotchas.

I built LandRight to be the guide I wish I had.

---

## Roadmap

- [ ] Personalisation — visa type, state, university aware responses
- [ ] Deadline tracker — OPT application reminders, tax deadlines
- [ ] Community Q&A — real questions from real students
- [ ] Voice interface — ask questions out loud
- [ ] University-specific info — different rules for different schools

---

## Author

**Rishitha Reddy** — international student, AI engineer in training.

[GitHub](https://github.com/RishithaReddy-stack)
