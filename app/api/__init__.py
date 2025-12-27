from fastapi import APIRouter
from app.api import murshid, quran, hadith, spiritual, voice

api_router = APIRouter()

api_router.include_router(murshid.router)
api_router.include_router(quran.router)
api_router.include_router(hadith.router)
api_router.include_router(spiritual.router)
api_router.include_router(voice.router)
