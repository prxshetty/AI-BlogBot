import httpx
from typing import List
from .base import BaseCollector
from data_models import SourceContent
from web_scraper import WebScrapingTool

class SerperCollector(BaseCollector):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://google.serper.dev/search"

    async def search(self, query: str, num: int = 5) -> List[dict]:
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type' : 'application/json'
        }
        payload = {'q': query, 'num': num}

        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json().get('organic', [])

    async def collect(self, query: str, **kwargs) -> List[SourceContent]:
        print(f"🔍 Searching web for: {query}")
        results = await self.search(query)
        sources = []

        async with WebScrapingTool() as scraper:
            for result in results:
                try:
                    print(f" Scraping: {result['link']}")
                    scraped = await scraper.scrape_url("filter", result['link'])
                    sources.append(SourceContent(
                        source_type='web',
                        source_url=result['link'],
                        title=result.get('title', ''),
                        content=scraped['content'],
                        metadata={'snippet': result.get('snippet', '')}
                    ))
                except Exception as e:
                    print(f" Failed to scrape {result['link']: {e}}")
            
            return sources
            

    