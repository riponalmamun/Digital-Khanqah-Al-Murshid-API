from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    ELEVENLABS_API_KEY: str
    
    # Islamic APIs
    QURAN_API_URL: str = "https://api.quran.com/api/v4"
    HADITH_API_URL: str = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"
    ALADHAN_API_URL: str = "https://api.aladhan.com/v1"
    
    # App Settings
    APP_NAME: str = "Digital Khanqah Al Murshid API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Rate Limits
    FREE_TIER_DAILY_LIMIT: int = 10
    PREMIUM_TIER_DAILY_LIMIT: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()