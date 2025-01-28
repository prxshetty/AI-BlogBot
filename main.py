import asyncio
import os
from dotenv import load_dotenv
from ai_agent import AIAgent

load_dotenv()

async def main(content_type : str, url: str):
    agent = AIAgent(llm_provider="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
    agent.task_manager.add_task(
        task_id="scrape_blog",
        description=f"scrape_{content_type}_{url}",
        dependencies=[]
    )
    agent.task_manager.add_task(
        task_id="generate_blog_post",
        description="generate:blog_post",
        dependencies=["scrape_blog"]
    )
    await agent.run()

    for task_id, task in agent.task_manager.tasks.items():
        print(f"Task {task_id}: {task.status}")
        if task.result:
            print(f"Result: {task.result}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <filter|raw> <url>")
        sys.exit(1)
    content_type = sys.argv[1].lower()
    if content_type not in ["filter", "raw"]:
        print("Usage: python main.py <filter|raw> <url>")
        sys.exit(1)
    url = sys.argv[2]
    asyncio.run(main(content_type, url)) 