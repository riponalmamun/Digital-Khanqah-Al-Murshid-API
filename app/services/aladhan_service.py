import httpx
from app.config import settings
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AladhanService:
    def __init__(self):
        self.base_url = settings.ALADHAN_API_URL
        self.timeout = 10.0
    
    async def get_prayer_times(
        self,
        city: str = "Dhaka",
        country: str = "Bangladesh"
    ) -> Optional[Dict]:
        """Get prayer times by city"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/timingsByCity",
                    params={
                        "city": city,
                        "country": country,
                        "method": 2  # ISNA method (you can change)
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                timings = data.get("data", {}).get("timings", {})
                date_info = data.get("data", {}).get("date", {})
                
                return {
                    "date": date_info.get("readable"),
                    "hijri_date": date_info.get("hijri", {}).get("date"),
                    "timings": {
                        "fajr": timings.get("Fajr"),
                        "sunrise": timings.get("Sunrise"),
                        "dhuhr": timings.get("Dhuhr"),
                        "asr": timings.get("Asr"),
                        "maghrib": timings.get("Maghrib"),
                        "isha": timings.get("Isha")
                    },
                    "city": city,
                    "country": country
                }
                
        except Exception as e:
            logger.error(f"Error fetching prayer times: {str(e)}")
            return None
    
    async def get_prayer_times_by_coordinates(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[Dict]:
        """Get prayer times by GPS coordinates"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/timings",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "method": 2
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                timings = data.get("data", {}).get("timings", {})
                
                return {
                    "timings": {
                        "fajr": timings.get("Fajr"),
                        "sunrise": timings.get("Sunrise"),
                        "dhuhr": timings.get("Dhuhr"),
                        "asr": timings.get("Asr"),
                        "maghrib": timings.get("Maghrib"),
                        "isha": timings.get("Isha")
                    }
                }
                
        except Exception as e:
            logger.error(f"Error fetching prayer times by coordinates: {str(e)}")
            return None
    
    async def get_qibla_direction(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[float]:
        """Get Qibla direction in degrees"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/qibla/{latitude}/{longitude}"
                )
                response.raise_for_status()
                data = response.json()
                
                direction = data.get("data", {}).get("direction")
                return direction
                
        except Exception as e:
            logger.error(f"Error fetching Qibla direction: {str(e)}")
            return None
    
    async def get_99_names_of_allah(self) -> Optional[List[Dict]]:
        """Get 99 Names of Allah"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/asmaAlHusna")
                response.raise_for_status()
                data = response.json()
                
                names = data.get("data", [])
                return names
                
        except Exception as e:
            logger.error(f"Error fetching 99 names: {str(e)}")
            return None