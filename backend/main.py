"""
FastAPI Backend for Telecommunications SMB Bot
Handles RAG queries, model selection, and API responses
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Telecommunications SMB Bot API",
    description="Backend API for RAG-powered cybersecurity assistant",
    version="1.0.0"
)

# Pydantic models
class ChatRequest(BaseModel):
    question: str
    namespace: Optional[str] = "custom_sources"
    mode: Optional[str] = "hybrid"
    top_k: Optional[int] = 8
    model_override: Optional[str] = None

class Citation(BaseModel):
    title: str
    source_id: str
    section: str
    pages: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    model: str
    citations: List[Citation] = []

# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    Processes question and returns RAG-augmented response
    """
    try:
        # TODO: Implement RAG logic here
        # This is a placeholder that returns a template response
        
        answer = f"Processing question: '{request.question}' in {request.mode} mode with namespace '{request.namespace}'"
        
        return ChatResponse(
            answer=answer,
            model=request.model_override or os.getenv("MODEL", "unknown"),
            citations=[]
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models"""
    return {
        "models": [
            "base",
            "finetuned",
            "rag",
            "hybrid"
        ]
    }

@app.get("/config")
async def get_config():
    """Get current configuration"""
    return {
        "api_url": os.getenv("API_URL", "http://localhost:8000"),
        "model": os.getenv("MODEL"),
        "namespace": os.getenv("PINECONE_NAMESPACE"),
        "system_name": os.getenv("SYSTEM_NAME", "Telecommunications SMB Bot")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
