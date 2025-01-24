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

    async def scrape_url(self, url: str, extraction_schema: Optional[dict] = None, user_query: str = "artificial intelligence") -> Dict:
        # prune_filter = PruningContentFilter(
        #     threshold=0.35,
        #     threshold_type="dynamic",
        #     min_word_threshold=50
        # )
        bm25_filter = BM25ContentFilter(
            user_query=user_query,
            bm25_threshold=1.2,
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
                    "selector": "h1",
                    "type": "text"
                },
                {
                    "name": "main_content",
                    "selector": "article",
                    "type": "text"
                }
            ]
        }
        config.extraction_strategy = JsonCssExtractionStrategy(extraction_schema or default_schema, verbose=True)
        result = await self.crawler.arun(url=url, 
            config=config,
            word_count_threshold = 10,
            excluded_tags = ['form'], 
            exclude_external_links = False,
            exclude_social_media_links = True,
            exclude_external_images = True,)
        
        if result.markdown_v2.fit_markdown:
            bm25_filtered_content = bm25_filter.filter_content(result.markdown_v2.fit_markdown)
            final_content = "\n---\n".join(bm25_filtered_content) if bm25_filtered_content else result.markdown_v2.fit_markdown
        else:
            final_content = result.markdown_v2.fit_markdown

        print("Raw Markdown:", len(result.markdown_v2.raw_markdown))
        print("Pruned Markdown:", len(result.markdown_v2.fit_markdown))
        print("Final BM25 Filtered Content Length:", len(final_content))

        return {
            'content': final_content,
            'extracted_data': json.loads(result.extracted_content) if result.extracted_content else None,
            'links': result.links,
            'media': result.media
        } 