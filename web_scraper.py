from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, JsonCssExtractionStrategy, PruningContentFilter, BM25ContentFilter, DefaultMarkdownGenerator
import json
from typing import Optional, Dict

class WebScrapingTool:
    def __init__(self):
        self.crawler = None

    async def __aenter__(self):
        self.crawler = AsyncWebCrawler()
        await self.crawler.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.crawler.__aexit__(exc_type, exc_val, exc_tb)

    async def scrape_url(self,description_parts : str, url: str, extraction_schema: Optional[dict] = None, user_query: str = "artificial intelligence") -> Dict:
            content_type = description_parts
            actual_url = url
            print(actual_url)
            print(f"Scraping URL: {actual_url} with content type: {content_type}")

            bm25_filter = BM25ContentFilter(
                user_query=user_query,
                bm25_threshold=1.0,
                language="english"
            )

            md_generator = DefaultMarkdownGenerator(
                content_filter=bm25_filter 
            )

            config = CrawlerRunConfig(
                cache_mode=CacheMode.ENABLED,
                markdown_generator=md_generator
            )
            default_schema = {
                "name": "Content Extractor",
                "baseSelector": "body",
                "fields": [
                    {
                        "name": "title",
                        "selector": "h1.entry-title, h1, .article-title",
                        "type": "text"
                    },
                    {
                        "name": "main_content",
                        "selector": "article, .entry-content, .post-content, main, .content",
                        "excludeSelectors": [
                            "nav",
                            "header",
                            "footer",
                            ".navigation",
                            ".menu",
                            ".sidebar",
                            ".related-posts"
                        ],
                        "type": "text"
                    }
                ]
            }
            config.extraction_strategy = JsonCssExtractionStrategy(extraction_schema or default_schema, verbose=True)
            result = await self.crawler.arun(
                url=actual_url, 
                config=config,
                word_count_threshold=50,
                excluded_tags=['form', 'nav', 'header', 'footer'], 
                exclude_external_links=True,
                exclude_social_media_links=True,
                exclude_external_images=True
            )

            if not result or not result.success:
                raise ValueError(f"Failed to crawl URL: {actual_url}")

            print("Raw Markdown:", len(result.markdown_v2.raw_markdown))
            print("Filtered Markdown:", len(result.markdown_v2.fit_markdown))

            content = result.markdown_v2.raw_markdown if content_type == "raw" else result.markdown_v2.fit_markdown
            return {
                'content': content,
                'extracted_data': json.loads(result.extracted_content) if result.extracted_content else None
            # 'links': result.links,
            # 'media': result.media
            } 