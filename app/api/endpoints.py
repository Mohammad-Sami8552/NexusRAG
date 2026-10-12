from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.rag_engine import rag_service
from app.core.config import settings
import os
import shutil

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    
@router.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    total_chunks = 0
    processed_files = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            continue # Skip non-PDFs
            
        file_path = os.path.join(settings.DATA_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        try:
            chunks_created = rag_service.process_document(file_path)
            total_chunks += chunks_created
            processed_files.append(file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")

    if not processed_files:
        raise HTTPException(status_code=400, detail="No valid PDF files were uploaded.")

    return {"message": f"Processed {len(processed_files)} documents into {total_chunks} chunks successfully."}

@router.post("/query")
async def query_rag(request: QueryRequest):
    try:
        return rag_service.query(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))