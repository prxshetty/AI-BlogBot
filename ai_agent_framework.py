from crawl4ai import *
import asyncio
import json
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

class TaskStatus(Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"

@dataclass
class Task:
    id: str
    dependencies : List[str]
    description: str
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None

class TaskManager: 
    def __init__(self):
        self.tasks : Dict[str, Task] = {}
    def add_task(self, task_id : str, description : str, dependencies : List[str] = None):
        self.tasks[task_id] = Task(
            id = task_id, 
            description = description,
            dependencies = dependencies or []
        )
    def get_next_tasks(self) -> List[Task]:
        ready_tasks = []
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                if all(self.tasks[dep].status == TaskStatus.COMPLETED for dep in task.dependencies):
                    ready_tasks.append(task)
        return ready_tasks
    
class WebScrapingTool:
    def __init__(self):
        self.crawler = None
    async def __aenter__(self):
        self.crawler = AsyncWebCrawler()
        await self.crawler.__aenter__()
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.crawler.__aexit__(exc_type, exc_val, exc_tb)
    async def scrape_url(self, url : str, extraction_schema : Optional[dict] = None) -> dict:
        config = CrawlerRunConfig(
            cache_mode = CacheMode.ENABLED  
        )
        default_schema = {
            "name" : "Content Extractor",
            "baseSelector" : "body",
            "fields" : [
                {
                    "name" : "title",
                    "selector" : "h1",
                    "type" : "text"
                },
                {
                    "name" : "main_content",
                    "selector" : "article",
                    "type" : "text"
                }
            ]
        }
        config.extraction_strategy = JsonCssExtractionStrategy(extraction_schema or default_schema, verbose = True)
        result = await self.crawler.arun(url = url, config = config)
        return {
            'content' : result.markdown_v2.raw_markdown,
            'extracted_data' : json.loads(result.extracted_content) if result.extracted_content else None,
            'links' : result.links,
            'media' : result.media
        }
    
class ContentGenerator:
    def __init__(self, llm_provider : str, api_key : Optional[str] = None):
        self.client = OpenAI(api_key = api_key)
        self.llm_provider = llm_provider
        self.api_key = api_key

    async def generate_content(self, data: dict, template : str) -> str:
        try:
            content = data.get('content', '')
            extracted_data = data.get('extracted_data', {})
            prompt = f"""Based on the following content, create a well-structured blog post:
            
            Content: {content[:2000]}  # Limiting content length for API constraints
            
            Please create a blog post that:
            1. Has a compelling title
            2. Includes an introduction
            3. Contains 3-4 main sections
            4. Ends with a conclusion
            5. Uses a professional tone
            """
            def make_openai_call():
                return self.client.chat.completions.create(
                    model = self.llm_provider,
                    messages = [{"role" : "system", "content" : "You are a professional blog writer"},
                    {"role" : "user" , "content" : prompt}
                    ]
                )
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, make_openai_call)

            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {str(e)}"

    
class AIAgent:
    def __init__(self, llm_provider : str = "gpt-4", api_key = os.getenv("OPENAI_API_KEY")):
        self.task_manager = TaskManager()
        self.content_generator = ContentGenerator(llm_provider, api_key)

    async def execute_task(self, task: Task):
        try: 
            task.status = TaskStatus.IN_PROGRESS
            if "scrape" in task.description:
                async with WebScrapingTool() as scraper:
                    task.result = await scraper.scrape_url(task.description.split("scrape:")[-1].strip())
            elif "generate" in task.description:
                source_task_id = task.dependencies[0]
                source_data = self.task_manager.tasks[source_task_id].result
                task.result = await self.content_generator.generate_content(
                    data = source_data,
                    template = "blog_post"
                )
            task.status = TaskStatus.COMPLETED
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = str(e)
            raise
    
    async def run(self):
        while True:
            ready_tasks = self.task_manager.get_next_tasks()
            if not ready_tasks:
                break
            await asyncio.gather(
                *[self.execute_task(task) for task in ready_tasks]
            )

async def main():
    agent = AIAgent(llm_provider = "gpt-4", api_key = os.getenv("OPENAI_API_KEY"))
    agent.task_manager.add_task(
        task_id = "scrape_blog",
        description = "scrape:https://www.techcrunch.com",
        dependencies = []
    )
    agent.task_manager.add_task(
        task_id = "generate_blog_post",
        description= "generate : blog_post",
        dependencies=["scrape_blog"]
    )
    await agent.run()

    for task_id, task in agent.task_manager.tasks.items():
        print(f"Task {task_id}: {task.status}")
        if task.result:
            print(f"Result: {task.result}")

asyncio.run(main())