from fastapi import APIRouter, HTTPException
from app.models.schemas import QuranExplainRequest, QuranResponse
from app.services.quran_service import QuranService
from app.services.openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quran", tags=["Quran"])

# Initialize services
quran_service = QuranService()
openai_service = OpenAIService()

@router.post("/explain", response_model=QuranResponse)
async def explain_verse(request: QuranExplainRequest):
    """
    Get Quranic verse with AI explanation
    
    - **surah_number**: Surah number (1-114)
    - **ayah_number**: Ayah number (optional, if not provided, explains full Surah)
    - **language**: Response language
    """
    try:
        # Get translation ID for language
        translation_id = quran_service.get_translation_id(request.language)
        
        # Fetch verse from Quran API
        if request.ayah_number:
            verse_data = await quran_service.get_verse(
                surah_number=request.surah_number,
                ayah_number=request.ayah_number,
                translation_id=translation_id
            )
        else:
            # Get first verse of Surah
            verse_data = await quran_service.get_verse(
                surah_number=request.surah_number,
                ayah_number=1,
                translation_id=translation_id
            )
        
        if not verse_data:
            raise HTTPException(status_code=404, detail="Verse not found")
        
        # Get AI explanation
        explanation = await openai_service.explain_quran_verse(
            verse=verse_data["arabic_text"],
            translation=verse_data["translation"],
            language=request.language
        )
        
        # Get Surah info
        surah_info = await quran_service.get_surah_info(request.surah_number)
        surah_name = surah_info.get("name_simple", f"Surah {request.surah_number}") if surah_info else f"Surah {request.surah_number}"
        
        return QuranResponse(
            surah_number=request.surah_number,
            surah_name=surah_name,
            ayah_number=verse_data.get("ayah_number"),
            arabic_text=verse_data["arabic_text"],
            translation=verse_data["translation"],
            explanation=explanation,
            language=request.language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Quran explain error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/surah/{surah_number}")
async def get_surah_info(surah_number: int):
    """Get basic information about a Surah"""
    try:
        if not 1 <= surah_number <= 114:
            raise HTTPException(status_code=400, detail="Invalid Surah number (1-114)")
        
        surah_info = await quran_service.get_surah_info(surah_number)
        
        if not surah_info:
            raise HTTPException(status_code=404, detail="Surah not found")
        
        return surah_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get Surah info error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_quran(query: str, language: str = "en"):
    """Search Quran by keyword"""
    try:
        results = await quran_service.search_quran(query, language)
        
        if results is None:
            raise HTTPException(status_code=500, detail="Search failed")
        
        return {"query": query, "results": results}
        
    except Exception as e:
        logger.error(f"Quran search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))