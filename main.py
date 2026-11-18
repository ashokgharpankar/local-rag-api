from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import chromadb
import asyncio

app = FastAPI(title="Local RAG Microservice (Async)", version="1.0")

# 1. Initialize Ollama Client (pointing to local instance)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# 2. Initialize Local ChromaDB Vector Store
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="enterprise_docs")

# --- Pydantic Models for Type Validation ---
class DocumentInput(BaseModel):
    doc_id: str
    text: str

class QueryInput(BaseModel):
    question: str

# --- Helper Function (Run synchronously or wrap in thread pool if heavy) ---
def get_embedding(text: str):
    response = client.embeddings.create(
        model="nomic-embed-text",
        input=text
    )
    return response.data[0].embedding

# --- Endpoint 1: Async Ingest ---
@app.post("/ingest")
async def ingest_document(doc: DocumentInput):
    try:
        # Offload CPU/blocking embedding generation to a background thread if needed,
        # or run directly for local lightweight setups
        vector = await asyncio.to_thread(get_embedding, doc.text)

        # Store in ChromaDB
        collection.add(
            ids=[doc.doc_id],
            embeddings=[vector],
            documents=[doc.text]
        )
        return {"status": "success", "message": f"Document '{doc.doc_id}' successfully embedded and stored."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint 2: Async RAG Query Pipeline ---
@app.post("/ask")
async def ask_question(query: QueryInput):
    try:
        # 1. Embed user query asynchronously
        query_vector = await asyncio.to_thread(get_embedding, query.question)

        # 2. Retrieve top matching document chunk from ChromaDB
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=1
        )

        retrieved_docs = results["documents"][0] if results["documents"] else []
        context = retrieved_docs[0] if retrieved_docs else "No relevant internal documentation found."

        # 3. Construct prompt with retrieved context
        system_prompt = (
            "You are an enterprise AI assistant. Answer the user's question accurately "
            "using *only* the provided context below. If the answer cannot be found in the context, "
            "state that you do not know.\n\n"
            f"Context:\n{context}"
        )

        # 4. Generate answer using local Llama 3.2 model asynchronously
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query.question}
            ]
        )

        return {
            "answer": response.choices[0].message.content,
            "retrieved_context_used": context
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
