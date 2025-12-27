from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import (
    ChatRequest, ChatResponse,
    DailyNaseehahResponse, ErrorResponse
)
from app.services.openai_service import OpenAIService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/murshid", tags=["AI Murshid"])

# Initialize service
openai_service = OpenAIService()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_murshid(request: ChatRequest):
    """
    Chat with AI Murshid - Your spiritual guide
    
    - **message**: Your question or message
    - **language**: Response language (en, ur, hi, ar, bn)
    - **conversation_history**: Optional previous messages for context
    """
    try:
        result = await openai_service.chat_with_murshid(
            message=request.message,
            language=request.language,
            conversation_history=request.conversation_history
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail="AI service error")
        
        return ChatResponse(
            response=result["response"],
            language=request.language,
            timestamp=datetime.now().isoformat(),
            tokens_used=result.get("tokens_used")
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/daily-naseehah", response_model=DailyNaseehahResponse)
async def get_daily_naseehah(language: str = "en"):
    """
    Get daily spiritual advice (Naseehah)
    
    - **language**: Response language
    """
    try:
        result = await openai_service.generate_daily_naseehah(language=language)
        
        return DailyNaseehahResponse(
            naseehah=result["naseehah"],
            reference=result.get("reference"),
            language=language,
            date=datetime.now().date().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Daily naseehah error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Murshid",
        "timestamp": datetime.now().isoformat()
    }