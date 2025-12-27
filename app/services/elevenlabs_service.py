from elevenlabs import generate, set_api_key, Voice, VoiceSettings
from app.config import settings
import logging
import base64
from typing import Dict, List

logger = logging.getLogger(__name__)

# Set ElevenLabs API key
set_api_key(settings.ELEVENLABS_API_KEY)

class ElevenLabsService:
    def __init__(self):
        # Default voice IDs (you can customize these from ElevenLabs dashboard)
        self.voice_ids = {
            "calm": "21m00Tcm4TlvDq8ikWAM",   # Rachel - calm, clear
            "wise": "21m00Tcm4TlvDq8ikWAM",   # Can change to different voice
            "gentle": "21m00Tcm4TlvDq8ikWAM"  # Can change to different voice
        }
    
    async def text_to_speech(
        self,
        text: str,
        voice_style: str = "calm",
        language: str = "en",
        speed: float = 0.85  # Slower speed for clear pronunciation
    ) -> Dict:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: Text to convert
            voice_style: calm, wise, or gentle
            language: Language code (en, ur, ar, etc.)
            speed: Speech rate (0.5-1.5)
                   0.5 = Very slow (good for learning)
                   0.7 = Slow (Quranic recitation pace)
                   0.85 = Moderately slow (default)
                   1.0 = Normal speed
                   1.5 = Fast
        
        Returns:
            Dict with audio data and success status
        """
        try:
            # Get appropriate voice ID
            voice_id = self.voice_ids.get(voice_style, self.voice_ids["calm"])
            
            # Adjust stability based on speed
            # Slower speech needs higher stability
            stability = 0.75 if speed < 1.0 else 0.60
            
            # Adjust style based on language
            # Arabic/Urdu: More formal, less expressive
            # English: More natural variation
            style_exaggeration = 0.3 if language in ['ar', 'ur'] else 0.5
            
            logger.info(f"Generating voice: speed={speed}, stability={stability}, style={style_exaggeration}")
            
            # Generate audio with custom settings
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=voice_id,
                    settings=VoiceSettings(
                        stability=stability,           # Voice consistency (0-1)
                        similarity_boost=0.75,         # Voice similarity (0-1)
                        style=style_exaggeration,      # Expressiveness (0-1)
                        use_speaker_boost=True,        # Enhanced clarity
                        speed=speed                    # Speech rate (0.5-1.5)
                    )
                ),
                model="eleven_multilingual_v2"  # Supports multiple languages
            )
            
            # Convert to base64 for easy transmission
            audio_base64 = base64.b64encode(audio).decode('utf-8')
            
            logger.info(f"Voice generated successfully (speed: {speed})")
            
            return {
                "success": True,
                "audio_base64": audio_base64,
                "audio_format": "mp3",
                "text": text,
                "speed": speed,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "audio_base64": None
            }
    
    async def generate_meditation_audio(
        self,
        script: str,
        language: str = "en"
    ) -> Dict:
        """
        Generate meditation audio with very slow, calm pace
        """
        return await self.text_to_speech(
            text=script,
            voice_style="calm",
            language=language,
            speed=0.70  # Very slow for meditation
        )
    
    def get_available_voices(self) -> List[str]:
        """Return available voice styles"""
        return list(self.voice_ids.keys())
    
    def get_recommended_speed(self, content_type: str) -> float:
        """
        Get recommended speed for different content types
        
        Returns:
            float: Recommended speed multiplier
        """
        speed_recommendations = {
            "quran": 0.70,        # Quranic recitation pace
            "dua": 0.75,          # Prayer/supplication
            "hadith": 0.80,       # Hadith narration
            "advice": 0.85,       # Spiritual advice (default)
            "meditation": 0.70,   # Meditation guidance
            "normal": 1.0,        # Normal conversation
            "fast": 1.2           # Quick information
        }
        
        return speed_recommendations.get(content_type, 0.85)