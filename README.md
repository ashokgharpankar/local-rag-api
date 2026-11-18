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
```
---

## ⚙️ Getting & Setting Up
1. Prerequisites
Ensure you have Ollama installed and running locally with the required models pulled:
```bash
ollama serve
ollama pull llama3.2
ollama pull nomic-embed-text
```
2. Clone the Repository & Set Up with uv
Clone the repository and initialize the project environment using uv:
```bash
git clone [https://github.com/ashokgharpankar/local-rag-api.git](https://github.com/ashokgharpankar/local-rag-api.git)
cd local-rag-api

# Pin python version and sync dependencies
uv python pin 3.12
uv venv --python 3.12
uv sync
```
---

## 🚀 Running the Application
Start the development server with live auto-reload enabled:
```bash
uv run uvicorn main:app --reload
```
The API will be live at http://127.0.0.1:8000.
---
## 📄 API Endpoints & Usage
You can test the endpoints interactively via FastAPI's built-in Swagger UI at http://127.0.0.1:8000/docs.

1. Ingest Documents (POST /ingest)
Saves a text document chunk, generates its local vector embedding using nomic-embed-text, and stores it securely in ChromaDB.

- Endpoint: POST /ingest
- Payload Example:
```bash
{
  "doc_id": "policy-01",
  "text": "Company Policy: Employees are entitled to 20 days of paid time off (PTO) per calendar year."
}
```
2. Query RAG Pipeline (POST /ask)
Embeds the user query, performs semantic similarity search against ChromaDB, extracts relevant context, and passes it to llama3.2 to generate a grounded, cited answer.

- Endpoint: POST /ask
- Payload Example:
```bash
{
  "question": "How many days of PTO do I get?"
}
```
- Response Example:
```bash
{
  "answer": "You are entitled to 20 days of paid time off (PTO) per calendar year.",
  "retrieved_context_used": "Company Policy: Employees are entitled to 20 days of paid time off (PTO) per calendar year."
}
```
---

## 💡 Enterprise Use Cases
- Air-Gapped & Compliance-First AI: Runs 100% locally with zero data sent to external cloud APIs, satisfying strict GDPR, HIPAA, and financial security requirements.
- Vendor-Agnostic Gateway: Uses an OpenAI-compatible client interface, allowing seamless switching between local weights and cloud providers (like GPT-4o) with zero application logic changes.


---


### How to Save & Push the Updated README to GitHub

Once you've updated the `README.md` file in your editor, run these quick Git commands in your terminal to push the changes:

```bash
git add README.md
git commit -m "Docs: Update comprehensive README with installation and API usage"
git push origin main
```
