import asyncio
import os
from dotenv import load_dotenv
from ai_agent import AIAgent

load_dotenv()

async def main(url: str):
    agent = AIAgent(llm_provider="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
    agent.task_manager.add_task(
        task_id="scrape_blog",
        description=f"scrape:{url}",
        dependencies=[]
    )
    # agent.task_manager.add_task(
    #     task_id="generate_blog_post",
    #     description="generate:blog_post",
    #     dependencies=["scrape_blog"]
    # )
    await agent.run()

    for task_id, task in agent.task_manager.tasks.items():
        print(f"Task {task_id}: {task.status}")
        if task.result:
            print(f"Result: {task.result}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    asyncio.run(main(url)) 