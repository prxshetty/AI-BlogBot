import os
import asyncio
from typing import Optional
from task_manager import TaskManager
from task_models import Task, TaskStatus
from content_generator import ContentGenerator
from web_scraper import WebScrapingTool

class AIAgent:
    def __init__(self, llm_provider: str = "gpt-4", api_key: Optional[str] = None):
        self.task_manager = TaskManager()
        self.content_generator = ContentGenerator(llm_provider, api_key)

    async def execute_task(self, task: Task):
        try:
            task.status = TaskStatus.IN_PROGRESS
            if "scrape" in task.description:
                async with WebScrapingTool() as scraper:
                    parts = task.description.split("_", 2) 
                    if len(parts) != 3:
                        raise ValueError(f"Invalid task description format: {task.description}")
                    content_type = parts[1].strip()
                    url = parts[2].strip()
                    
                    print(f"Processing task: content_type={content_type}, url={url}")
                    task.result = await scraper.scrape_url(content_type, url)
            
            elif "generate" in task.description:
                source_task_id = task.dependencies[0]
                source_data = self.task_manager.tasks[source_task_id].result
                
                task.result = await self.content_generator.generate_content(
                    data=source_data,
                    template="blog_post" # figure out how to use this in the prompt 
                )
            task.status = TaskStatus.COMPLETED
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            print(f"Task failed: {str(e)}")
            raise

    async def run(self):
        while True:
            ready_tasks = self.task_manager.get_next_tasks()
            if not ready_tasks:
                break
            await asyncio.gather(
                *[self.execute_task(task) for task in ready_tasks]
            ) 