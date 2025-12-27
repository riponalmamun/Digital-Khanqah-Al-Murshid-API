from openai import OpenAI
from app.config import settings
from app.utils.prompts import SufiPrompts
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"  # or "gpt-4" or "gpt-3.5-turbo"
        self.prompts = SufiPrompts()
    
    async def chat_with_murshid(
        self,
        message: str,
        language: str = "en",
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """Main AI Murshid chat function"""
        try:
            # Build messages
            messages = [
                {
                    "role": "system",
                    "content": f"{self.prompts.MURSHID_SYSTEM_PROMPT}\n\n{self.prompts.get_language_instruction(language)}"
                }
            ]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Last 5 messages for context
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            return {
                "response": assistant_message,
                "tokens_used": tokens_used,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"OpenAI chat error: {str(e)}")
            return {
                "response": "I apologize, dear seeker. I'm having difficulty responding at the moment. Please try again.",
                "tokens_used": 0,
                "success": False,
                "error": str(e)
            }
    
    async def explain_quran_verse(
        self,
        verse: str,
        translation: str,
        language: str = "en"
    ) -> str:
        """Explain Quran verse in simple language"""
        try:
            prompt = self.prompts.get_quran_explanation_prompt(verse, translation)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a Sufi Quranic scholar. {self.prompts.get_language_instruction(language)}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Quran explanation error: {str(e)}")
            return "Unable to provide explanation at this moment. Please try again."
    
    async def explain_hadith(
        self,
        hadith_text: str,
        language: str = "en"
    ) -> str:
        """Explain Hadith in simple language"""
        try:
            prompt = self.prompts.get_hadith_explanation_prompt(hadith_text)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a Hadith scholar with Sufi understanding. {self.prompts.get_language_instruction(language)}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Hadith explanation error: {str(e)}")
            return "Unable to provide explanation at this moment. Please try again."
    
    async def generate_spiritual_advice(
        self,
        topic: str,
        user_level: str = "beginner",
        language: str = "en"
    ) -> Dict:
        """Generate spiritual advice"""
        try:
            prompt = self.prompts.get_spiritual_advice_prompt(topic, user_level)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"{self.prompts.MURSHID_SYSTEM_PROMPT}\n\n{self.prompts.get_language_instruction(language)}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=700
            )
            
            advice = response.choices[0].message.content
            
            # Extract recommended practices (simple parsing)
            recommended_zikr = [
                "SubhanAllah (33 times)",
                "Alhamdulillah (33 times)",
                "Allahu Akbar (34 times)"
            ]
            
            next_steps = [
                "Maintain regular prayers",
                "Practice daily dhikr",
                "Read Quran with reflection"
            ]
            
            return {
                "advice": advice,
                "recommended_zikr": recommended_zikr,
                "next_steps": next_steps
            }
            
        except Exception as e:
            logger.error(f"Spiritual advice error: {str(e)}")
            return {
                "advice": "May Allah guide you on your spiritual journey.",
                "recommended_zikr": [],
                "next_steps": []
            }
    
    async def generate_meditation_script(
        self,
        goal: str,
        duration: int,
        language: str = "en"
    ) -> str:
        """Generate meditation script"""
        try:
            prompt = self.prompts.get_meditation_script_prompt(goal, duration)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a Sufi meditation guide. {self.prompts.get_language_instruction(language)}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Meditation script error: {str(e)}")
            return "Begin by taking deep breaths and remembering Allah..."
    
    async def generate_daily_naseehah(self, language: str = "en") -> Dict:
        """Generate daily spiritual advice"""
        try:
            prompt = self.prompts.get_daily_naseehah_prompt()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are Al Murshid, a Sufi spiritual guide. {self.prompts.get_language_instruction(language)}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=300
            )
            
            naseehah = response.choices[0].message.content
            
            return {
                "naseehah": naseehah,
                "reference": "Quran/Hadith"  # Could be enhanced to extract actual reference
            }
            
        except Exception as e:
            logger.error(f"Daily naseehah error: {str(e)}")
            return {
                "naseehah": "Remember Allah in all that you do.",
                "reference": None
            }