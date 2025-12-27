from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import Response
from app.models.schemas import VoiceGenerateRequest, LanguageEnum, VoiceStyleEnum
from typing import Optional
from fastapi import Query
from app.services.elevenlabs_service import ElevenLabsService
from app.services.openai_service import OpenAIService
import logging
import base64
from openai import OpenAI
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["Voice"])

# Initialize services
elevenlabs_service = ElevenLabsService()
openai_service = OpenAIService()
whisper_client = OpenAI(api_key=settings.OPENAI_API_KEY)

@router.post("/generate")
async def generate_voice(
    request: VoiceGenerateRequest,
    speed: Optional[float] = 0.85  # Slower speed (0.5-1.5, default: 0.85)
):
    """
    Convert text to speech and download MP3
    
    - **text**: Text to convert to voice
    - **language**: Language (en, ur, ar, hi, bn)
    - **voice_style**: Voice style (calm, wise, gentle)
    - **speed**: Reading speed (0.5=very slow, 0.85=slow, 1.0=normal, 1.5=fast)
    
    Returns: Downloadable MP3 file
    
    **For Arabic/Quranic text, use speed=0.7 for recitation-like pace**
    """
    try:
        logger.info(f"Generating voice for text: {request.text[:50]}... (speed: {speed})")
        
        result = await elevenlabs_service.text_to_speech(
            text=request.text,
            voice_style=request.voice_style,
            language=request.language,
            speed=speed
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail="Voice generation failed")
        
        # Decode base64 to bytes
        audio_bytes = base64.b64decode(result['audio_base64'])
        
        logger.info("Voice generated successfully")
        
        # Return as downloadable MP3 file
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=voice_{request.language}_speed{speed}.mp3"
            }
        )
        
    except Exception as e:
        logger.error(f"Voice generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def voice_chat(
    audio: UploadFile = File(..., description="Audio file (MP3, WAV, M4A)"),
    language: LanguageEnum = Query(default=LanguageEnum.ENGLISH, description="Response language - Select from dropdown"),
    response_speed: Optional[float] = Query(default=0.85, ge=0.5, le=1.5, description="Voice speed (0.5-1.5)")
):
    """
    Voice chat with AI Murshid
    
    **Upload your voice → Get AI response with voice**
    
    Flow:
    1. Upload your audio file (MP3/WAV/M4A)
    2. Audio transcribed to text (Whisper)
    3. AI Murshid responds to your message
    4. Response converted to voice (ElevenLabs) - SLOW, CLEAR pace
    5. Returns text + audio in JSON
    
    Parameters:
    - **audio**: Your voice/audio file
    - **language**: Response language (en, ur, ar, hi, bn)
    - **response_speed**: Voice speed (0.5-1.5, default: 0.85 = slow & clear)
    
    **For Arabic responses, use 0.7 for Quranic recitation pace**
    
    Returns:
    - user_message: What you said (transcribed)
    - ai_response: AI Murshid's text response
    - audio_base64: AI response in audio format (base64)
    - download_url: Data URL to play/download audio
    """
    try:
        # Step 1: Read uploaded audio
        audio_bytes = await audio.read()
        logger.info(f"Received audio file: {audio.filename} ({len(audio_bytes)} bytes)")
        
        # Step 2: Transcribe audio to text (Whisper)
        logger.info("Transcribing audio with Whisper...")
        
        temp_filename = f"temp_audio.{audio.filename.split('.')[-1]}"
        
        transcription = whisper_client.audio.transcriptions.create(
            model="whisper-1",
            file=(temp_filename, audio_bytes, audio.content_type)
        )
        
        user_message = transcription.text
        logger.info(f"Transcribed: {user_message}")
        
        # Step 3: Get AI Murshid response
        logger.info("Getting AI Murshid response...")
        
        chat_result = await openai_service.chat_with_murshid(
            message=user_message,
            language=language.value  # Convert enum to string
        )
        
        if not chat_result.get("success"):
            raise HTTPException(status_code=500, detail="AI response failed")
        
        response_text = chat_result["response"]
        logger.info(f"AI response generated ({len(response_text)} chars)")
        
        # Step 4: Convert AI response to voice (SLOW pace)
        logger.info(f"Converting response to voice (speed: {response_speed})...")
        
        voice_result = await elevenlabs_service.text_to_speech(
            text=response_text,
            voice_style="calm",
            language=language.value,  # Convert enum to string
            speed=response_speed
        )
        
        if not voice_result.get("success"):
            raise HTTPException(status_code=500, detail="Voice generation failed")
        
        audio_base64 = voice_result['audio_base64']
        logger.info("Voice chat completed successfully")
        
        # Return complete response
        return {
            "user_message": user_message,
            "ai_response": response_text,
            "audio_base64": audio_base64,
            "download_url": f"data:audio/mpeg;base64,{audio_base64}",
            "language": language.value,  # Return string value
            "speed": response_speed,
            "tokens_used": chat_result.get("tokens_used"),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Voice chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))