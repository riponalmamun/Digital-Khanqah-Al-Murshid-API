import httpx
from app.config import settings
import logging
from typing import Dict, Optional, List
import random

logger = logging.getLogger(__name__)

class HadithService:
    def __init__(self):
        self.base_url = settings.HADITH_API_URL
        self.timeout = 10.0
        
        # Updated collections with proper format
        self.collections = {
            "bukhari": {
                "name": "Sahih Bukhari",
                "prefix": "eng-bukhari",
                "books": 97
            },
            "muslim": {
                "name": "Sahih Muslim",
                "prefix": "eng-muslim",
                "books": 56
            },
            "abudawud": {
                "name": "Sunan Abu Dawud",
                "prefix": "eng-abudawud",
                "books": 43
            },
            "tirmidhi": {
                "name": "Jami At-Tirmidhi",
                "prefix": "eng-tirmidhi",
                "books": 51
            },
            "nasai": {
                "name": "Sunan an-Nasa'i",
                "prefix": "eng-nasai",
                "books": 51
            },
            "ibnmajah": {
                "name": "Sunan Ibn Majah",
                "prefix": "eng-ibnmajah",
                "books": 37
            }
        }
    
    async def get_hadith(
        self,
        collection: str = "bukhari",
        book_number: int = 1
    ) -> Optional[Dict]:
        """Get hadith from specific collection and book"""
        try:
            # Normalize collection name
            collection = collection.lower()
            
            if collection not in self.collections:
                logger.error(f"Invalid collection: {collection}")
                return None
            
            collection_info = self.collections[collection]
            
            # Validate book number
            if book_number < 1 or book_number > collection_info["books"]:
                logger.error(f"Invalid book number for {collection}: {book_number} (max: {collection_info['books']})")
                # Return first book instead of error
                book_number = 1
            
            # Try different URL formats
            url_formats = [
                f"{self.base_url}/editions/{collection_info['prefix']}/{book_number}.json",
                f"{self.base_url}/editions/{collection}/{book_number}.json",
                f"{self.base_url}/editions/eng-{collection}/{book_number}.json"
            ]
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                for url in url_formats:
                    try:
                        logger.info(f"Trying URL: {url}")
                        response = await client.get(url)
                        response.raise_for_status()
                        data = response.json()
                        
                        hadiths = data.get("hadiths", [])
                        
                        if not hadiths:
                            continue
                        
                        # Return first hadith from the book
                        hadith = hadiths[0]
                        
                        return {
                            "collection": collection_info["name"],
                            "book_number": book_number,
                            "hadith_number": hadith.get("hadithnumber", 1),
                            "text": hadith.get("text", ""),
                            "arabic": hadith.get("arabic", ""),
                            "reference": hadith.get("reference", {})
                        }
                    except Exception as e:
                        logger.warning(f"Failed with URL {url}: {str(e)}")
                        continue
                
                # If all formats failed, return error
                logger.error(f"All URL formats failed for {collection}, book {book_number}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching hadith: {str(e)}")
            return None
    
    async def get_random_hadith(self) -> Optional[Dict]:
        """Get a random hadith"""
        try:
            # Pick random collection
            collection = random.choice(list(self.collections.keys()))
            collection_info = self.collections[collection]
            
            # Pick random book number (from available books)
            book_number = random.randint(1, min(10, collection_info["books"]))
            
            return await self.get_hadith(collection, book_number)
            
        except Exception as e:
            logger.error(f"Error getting random hadith: {str(e)}")
            return None
    
    async def get_available_collections(self) -> List[Dict]:
        """Get list of available hadith collections"""
        return [
            {
                "id": key,
                "name": value["name"],
                "total_books": value["books"]
            }
            for key, value in self.collections.items()
        ]
    
    async def get_hadith_by_number(
        self,
        collection: str,
        hadith_number: int
    ) -> Optional[Dict]:
        """
        Get specific hadith by its number
        Note: This requires knowing which book it's in
        """
        # For now, search through books (not efficient, but works)
        collection_info = self.collections.get(collection.lower())
        if not collection_info:
            return None
        
        # Try first few books
        for book_num in range(1, min(5, collection_info["books"] + 1)):
            result = await self.get_hadith(collection, book_num)
            if result and result.get("hadith_number") == hadith_number:
                return result
        
        return None