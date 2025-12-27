from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    SpiritualAdviceRequest, SpiritualAdviceResponse,
    MeditationRequest, MeditationResponse
)
from app.services.openai_service import OpenAIService
from app.services.elevenlabs_service import ElevenLabsService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/spiritual", tags=["Spiritual Guidance"])

# Initialize services
openai_service = OpenAIService()
elevenlabs_service = ElevenLabsService()

@router.post("/advice", response_model=SpiritualAdviceResponse)
async def get_spiritual_advice(request: SpiritualAdviceRequest):
    """
    Get personalized spiritual advice
    
    - **topic**: What you need guidance on
    - **user_level**: Your spiritual level (beginner/intermediate/advanced)
    - **language**: Response language
    """
    try:
        result = await openai_service.generate_spiritual_advice(
            topic=request.topic,
            user_level=request.user_level,
            language=request.language
        )
        
        return SpiritualAdviceResponse(
            advice=result["advice"],
            recommended_zikr=result["recommended_zikr"],
            next_steps=result["next_steps"],
            language=request.language
        )
        
    except Exception as e:
        logger.error(f"Spiritual advice error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/meditation", response_model=MeditationResponse)
async def generate_meditation(request: MeditationRequest):
    """
    Generate guided meditation script
    
    - **goal**: Meditation goal (stress relief, focus, repentance, etc.)
    - **duration_minutes**: How long (3-30 minutes)
    - **language**: Response language
    """
    try:
        # Generate meditation script
        script = await openai_service.generate_meditation_script(
            goal=request.goal,
            duration=request.duration_minutes,
            language=request.language
        )
        
        # Split script into steps (simple splitting by newlines)
        steps = [step.strip() for step in script.split('\n\n') if step.strip()]
        
        # Optionally generate audio (for premium users)
        audio_url = None
        # Uncomment below to enable audio generation
        # audio_result = await elevenlabs_service.generate_meditation_audio(script, request.language)
        # if audio_result.get("success"):
        #     audio_url = audio_result.get("audio_base64")  # In production, save to file/S3
        
        return MeditationResponse(
            script=script,
            audio_url=audio_url,
            duration_minutes=request.duration_minutes,
            steps=steps,
            language=request.language
        )
        
    except Exception as e:
        logger.error(f"Meditation generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/zikr-suggestions")
async def get_zikr_suggestions(mood: str = "general", language: str = "en"):
    """
    Get Zikr suggestions based on mood/state
    
    - **mood**: Current state (peaceful, anxious, grateful, repentant, etc.)
    - **language**: Response language
    """
    try:
        # Predefined Zikr recommendations
        zikr_map = {
            "peaceful": [
                "SubhanAllah (100 times)",
                "Alhamdulillah (100 times)",
                "La ilaha illallah (100 times)"
            ],
            "anxious": [
                "La hawla wa la quwwata illa billah",
                "Hasbunallahu wa ni'mal wakeel (70 times)",
                "Ayatul Kursi (3 times)"
            ],
            "grateful": [
                "Alhamdulillah (100 times)",
                "Shukran lillah (continuous)",
                "Surah Al-Fatihah (7 times)"
            ],
            "repentant": [
                "Astaghfirullah (100 times)",
                "Rabbi la tazarni fardan (11 times)",
                "Durood Sharif (100 times)"
            ],
            "general": [
                "SubhanAllah (33 times)",
                "Alhamdulillah (33 times)",
                "Allahu Akbar (34 times)"
            ]
        }
        
        zikr_list = zikr_map.get(mood.lower(), zikr_map["general"])
        
        return {
            "mood": mood,
            "zikr_suggestions": zikr_list,
            "language": language,
            "note": "Recite with full presence and sincerity"
        }
        
    except Exception as e:
        logger.error(f"Zikr suggestions error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))