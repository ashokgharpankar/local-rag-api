# 🚀 Local RAG Microservice (FastAPI + Ollama + ChromaDB)

A high-performance, privacy-first **Retrieval-Augmented Generation (RAG)** microservice built with **FastAPI**, **Pydantic v2**, **ChromaDB**, and **Ollama**.

This project is designed as an enterprise-grade AI pattern for secure, air-gapped environments where proprietary data cannot leave local infrastructure or private VPCs.

---

## 🛠️ Tech Stack & Architecture

- **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Async request handling & automatic Swagger documentation)
- **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/) (Strict schema validation and type safety)
- **Vector Database:** [ChromaDB](https://www.trychroma.com/) (Lightweight local vector embedding storage and semantic search)
- **Local LLM & Embeddings:** [Ollama](https://ollama.com/) running **`llama3.2`** (text generation) and **`nomic-embed-text`** (vector embeddings)
- **Package Management:** [uv](https://github.com/astral-sh/uv) (Blazing-fast dependency management)

---

## 📂 Project Structure

```text
local-rag-api/
│
├── .venv/               # Isolated virtual environment (managed by uv)
├── main.py              # FastAPI application & RAG pipeline logic
├── pyproject.toml       # Project metadata and dependencies
└── README.md            # Project documentation
