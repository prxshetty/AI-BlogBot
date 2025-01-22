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
                    task.result = await scraper.scrape_url(task.description.split("scrape:")[-1].strip())
            elif "generate" in task.description:
                source_task_id = task.dependencies[0]
                source_data = self.task_manager.tasks[source_task_id].result
                task.result = await self.content_generator.generate_content(
                    data=source_data,
                    template="blog_post"
                )
            task.status = TaskStatus.COMPLETED
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            raise

    async def run(self):
        while True:
            ready_tasks = self.task_manager.get_next_tasks()
            if not ready_tasks:
                break
            await asyncio.gather(
                *[self.execute_task(task) for task in ready_tasks]
            ) 