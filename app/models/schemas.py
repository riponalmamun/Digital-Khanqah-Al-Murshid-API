from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

# Enums
class LanguageEnum(str, Enum):
    """Supported languages - User can select from dropdown"""
    ENGLISH = "en"
    URDU = "ur"
    HINDI = "hi"
    ARABIC = "ar"
    BENGALI = "bn"

class UserTierEnum(str, Enum):
    FREE = "free"
    PREMIUM = "premium"

class VoiceStyleEnum(str, Enum):
    """Voice styles for audio generation"""
    CALM = "calm"
    WISE = "wise"
    GENTLE = "gentle"

# Request Models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="User's message")
    language: LanguageEnum = Field(default=LanguageEnum.ENGLISH, description="Response language")
    user_id: Optional[str] = Field(None, description="User ID for context")
    conversation_history: Optional[List[dict]] = Field(default=[], description="Previous messages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "How do I get closer to Allah?",
                "language": "en",
                "user_id": "user123"
            }
        }

class VoiceChatRequest(BaseModel):
    message: str = Field(..., description="Message to convert to voice")
    language: LanguageEnum = Field(default=LanguageEnum.ENGLISH)
    voice_id: Optional[str] = Field(None, description="ElevenLabs voice ID")

class QuranExplainRequest(BaseModel):
    surah_number: int = Field(..., ge=1, le=114, description="Surah number (1-114)")
    ayah_number: Optional[int] = Field(None, ge=1, description="Ayah number")
    language: LanguageEnum = Field(default=LanguageEnum.ENGLISH)
    
    class Config:
        json_schema_extra = {
            "example": {
                "surah_number": 1,
                "ayah_number": 1,
                "language": "en"
            }
        }

class HadithExplainRequest(BaseModel):
    collection: str = Field(..., description="Hadith collection (e.g., 'bukhari')")
    book_number: int = Field(..., ge=1, description="Book number")
    hadith_number: Optional[int] = Field(None, description="Specific hadith number")
    language: LanguageEnum = Field(default=LanguageEnum.ENGLISH)

class SpiritualAdviceRequest(BaseModel):
    topic: str = Field(..., description="Spiritual topic or issue")
    user_level: Optional[str] = Field("beginner", description="Spiritual level: beginner, intermediate, advanced")
    language: LanguageEnum = Field(default=LanguageEnum.ENGLISH)

class MeditationRequest(BaseModel):
    goal: str = Field(..., description="Meditation goal (e.g., 'stress relief', 'focus', 'repentance')")
    duration_minutes: int = Field(5, ge=3, le=30, description="Meditation duration")
    language: LanguageEnum = Field(default=LanguageEnum.ENGLISH)

class VoiceGenerateRequest(BaseModel):
    text: str = Field(..., max_length=5000, description="Text to convert to voice")
    language: LanguageEnum = Field(default=LanguageEnum.ENGLISH, description="Language of the text")
    voice_style: VoiceStyleEnum = Field(default=VoiceStyleEnum.CALM, description="Voice style")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Bismillah ir-Rahman ir-Rahim",
                "language": "ar",
                "voice_style": "calm"
            }
        }

# Response Models
class ChatResponse(BaseModel):
    response: str = Field(..., description="AI Murshid's response")
    language: str
    timestamp: str
    tokens_used: Optional[int] = None
    
class VoiceResponse(BaseModel):
    text: str
    audio_url: str
    duration_seconds: Optional[float] = None
    language: str

class QuranResponse(BaseModel):
    surah_number: int
    surah_name: str
    ayah_number: Optional[int]
    arabic_text: str
    translation: str
    explanation: str
    language: str

class HadithResponse(BaseModel):
    collection: str
    book_number: int
    hadith_number: Optional[int]
    arabic_text: Optional[str]
    translation: str
    explanation: str
    authenticity: Optional[str]
    language: str

class SpiritualAdviceResponse(BaseModel):
    advice: str
    recommended_zikr: List[str]
    next_steps: List[str]
    language: str

class MeditationResponse(BaseModel):
    script: str
    audio_url: Optional[str]
    duration_minutes: int
    steps: List[str]
    language: str

class DailyNaseehahResponse(BaseModel):
    naseehah: str
    reference: Optional[str] = None
    language: str
    date: str

# Error Response
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str