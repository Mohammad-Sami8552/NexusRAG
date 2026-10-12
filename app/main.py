from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="NexusRAG API",
    description="Modular RAG pipeline with FastAPI and ChromaDB"
)
@app.get("/")
async def root():
    return {"status": "NexusRAG API is running", "docs": "Visit http://127.0.0.1:8000/docs to test endpoints"}
app.include_router(router, prefix="/api/v1")

# Run with: uvicorn app.main:app --reload