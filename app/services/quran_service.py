import httpx
from app.config import settings
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class QuranService:
    def __init__(self):
        self.base_url = settings.QURAN_API_URL
        self.timeout = 10.0
    
    async def get_surah_info(self, surah_number: int) -> Optional[Dict]:
        """Get Surah basic information"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/chapters/{surah_number}")
                response.raise_for_status()
                data = response.json()
                return data.get("chapter")
        except Exception as e:
            logger.error(f"Error fetching Surah info: {str(e)}")
            return None
    
    async def get_verse(
        self,
        surah_number: int,
        ayah_number: int,
        translation_id: int = 131  # 131 = Sahih International (English)
    ) -> Optional[Dict]:
        """Get specific verse with translation"""
        try:
            verse_key = f"{surah_number}:{ayah_number}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Get Arabic text
                arabic_response = await client.get(
                    f"{self.base_url}/verses/by_key/{verse_key}",
                    params={"fields": "text_uthmani"}
                )
                arabic_response.raise_for_status()
                arabic_data = arabic_response.json()
                
                # Get translation
                translation_response = await client.get(
                    f"{self.base_url}/verses/by_key/{verse_key}",
                    params={
                        "translations": translation_id,
                        "fields": "text_uthmani"
                    }
                )
                translation_response.raise_for_status()
                translation_data = translation_response.json()
                
                verse = arabic_data.get("verse", {})
                translations = translation_data.get("verse", {}).get("translations", [])
                
                return {
                    "verse_key": verse_key,
                    "arabic_text": verse.get("text_uthmani", ""),
                    "translation": translations[0].get("text", "") if translations else "",
                    "surah_number": surah_number,
                    "ayah_number": ayah_number
                }
                
        except Exception as e:
            logger.error(f"Error fetching verse: {str(e)}")
            return None
    
    async def get_full_surah(
        self,
        surah_number: int,
        translation_id: int = 131
    ) -> Optional[Dict]:
        """Get full Surah with translation"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/verses/by_chapter/{surah_number}",
                    params={
                        "translations": translation_id,
                        "fields": "text_uthmani"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                verses = data.get("verses", [])
                
                return {
                    "surah_number": surah_number,
                    "verses": [
                        {
                            "ayah_number": v.get("verse_number"),
                            "arabic_text": v.get("text_uthmani", ""),
                            "translation": v.get("translations", [{}])[0].get("text", "")
                        }
                        for v in verses
                    ]
                }
                
        except Exception as e:
            logger.error(f"Error fetching full Surah: {str(e)}")
            return None
    
    def get_translation_id(self, language: str) -> int:
        """Get translation ID based on language"""
        translation_map = {
            "en": 131,  # Sahih International
            "ur": 97,   # Abul A'ala Maududi
            "hi": 122,  # Hindi
            "ar": 0,    # Arabic (original)
            "bn": 161   # Bengali
        }
        return translation_map.get(language, 131)
    
    async def search_quran(self, query: str, language: str = "en") -> Optional[List[Dict]]:
        """Search Quran by text"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params={"q": query, "size": 10}
                )
                response.raise_for_status()
                data = response.json()
                
                return data.get("search", {}).get("results", [])
                
        except Exception as e:
            logger.error(f"Error searching Quran: {str(e)}")
            return None