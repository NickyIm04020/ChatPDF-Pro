import shutil
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.ingest import ingest_docs
from app.rag import ChatPDFSystem

app = FastAPI(title="ChatPDF Pro API")

# GLOBAL VARIABLE (Start as None)
rag_system = None

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "active", "message": "ChatPDF Pro is running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global rag_system
    
    # 1. Save the file
    os.makedirs("documents", exist_ok=True)
    file_path = f"documents/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Trigger Ingestion (This Creates the Index if missing)
    try:
        ingest_docs("documents")
        
        # 3. Initialize the RAG system now that the index exists
        if rag_system is None:
            rag_system = ChatPDFSystem()
            
        return {"message": f"Successfully ingested {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/chat")
async def chat(request: QueryRequest):
    global rag_system
    
    if rag_system is None:
        # Try to initialize if not ready
        try:
            rag_system = ChatPDFSystem()
        except Exception as e:
            raise HTTPException(status_code=400, detail="System not ready. Please upload a PDF first to create the index.")
            
    response = rag_system.ask(request.query)
    return response