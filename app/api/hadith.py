from fastapi import APIRouter, HTTPException
from app.models.schemas import HadithExplainRequest, HadithResponse
from app.services.hadith_service import HadithService
from app.services.openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hadith", tags=["Hadith"])

# Initialize services
hadith_service = HadithService()
openai_service = OpenAIService()

@router.post("/explain", response_model=HadithResponse)
async def explain_hadith(request: HadithExplainRequest):
    """
    Get Hadith with AI explanation
    
    - **collection**: Hadith collection (bukhari, muslim, etc.)
    - **book_number**: Book number
    - **language**: Response language
    """
    try:
        # Fetch hadith
        hadith_data = await hadith_service.get_hadith(
            collection=request.collection,
            book_number=request.book_number
        )
        
        if not hadith_data:
            raise HTTPException(status_code=404, detail="Hadith not found")
        
        # Get AI explanation
        explanation = await openai_service.explain_hadith(
            hadith_text=hadith_data["text"],
            language=request.language
        )
        
        return HadithResponse(
            collection=hadith_data["collection"],
            book_number=hadith_data["book_number"],
            hadith_number=hadith_data.get("hadith_number"),
            arabic_text=hadith_data.get("arabic"),
            translation=hadith_data["text"],
            explanation=explanation,
            authenticity="Sahih",  # You can enhance this
            language=request.language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Hadith explain error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/random")
async def get_random_hadith(language: str = "en"):
    """Get a random Hadith with explanation"""
    try:
        hadith_data = await hadith_service.get_random_hadith()
        
        if not hadith_data:
            raise HTTPException(status_code=404, detail="Could not fetch hadith")
        
        explanation = await openai_service.explain_hadith(
            hadith_text=hadith_data["text"],
            language=language
        )
        
        return {
            "hadith": hadith_data,
            "explanation": explanation,
            "language": language
        }
        
    except Exception as e:
        logger.error(f"Random hadith error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/collections")
async def get_collections():
    """Get list of available Hadith collections"""
    try:
        collections = await hadith_service.get_available_collections()
        return {"collections": collections}
        
    except Exception as e:
        logger.error(f"Get collections error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))