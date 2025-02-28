import os
import asyncio
from typing import Optional
from task_manager import TaskManager
from task_models import Task, TaskStatus
from content_generator import ContentGenerator
from web_scraper import WebScrapingTool
from utils import save_content_to_file

class AIAgent:
    def __init__(self, llm_provider: str = "gpt-4", api_key: Optional[str] = None):
        self.task_manager = TaskManager()
        self.content_generator = ContentGenerator(llm_provider, api_key)

    async def execute_task(self, task: Task):
        try:
            task.status = TaskStatus.IN_PROGRESS
            
            if "youtube_process" in task.description:
                # YouTube task result is already set in main.py
                # Just mark it as completed since processing is done
                task.status = TaskStatus.COMPLETED
                
            elif "scrape" in task.description:
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
                
                if not source_data:
                    raise ValueError("No source content available for generation")                
                blog_type = task.description.split(":")[1] if ":" in task.description else "standard"
                
                # Generate content using the content generator
                task.result = await self.content_generator.generate_content(
                    data=source_data,
                    blog_type=blog_type
                )
                
                if not task.result:
                    raise ValueError("Failed to generate content")

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