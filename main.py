import asyncio
import os
from dotenv import load_dotenv
from ai_agent import AIAgent

load_dotenv()

def get_user_input():
    print("\n=== Blog Content Scraper ===")
    while True:
        print("\nSelect content filter method:")
        print("1. raw - Get raw content")
        print("2. filter - Get filtered content")
        print("3. exit - Exit the program")
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "3":
            print("\nExiting program...")
            exit(0)
        elif choice == "1":
            content_type = "raw"
            break
        elif choice == "2":
            content_type = "filter"
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")
    
    # Get URL
    while True:
        url = input("\nEnter the website URL to scrape (or 'exit' to quit): ").strip()
        if url.lower() == 'exit':
            print("\nExiting program...")
            exit(0)
        elif url:
            if not url.startswith(('http://', 'https://', 'file://', 'raw:')):
                url = 'https://' + url.lstrip('/')
            break
        else:
            print("\nURL cannot be empty. Please try again.")
    
    return content_type, url

async def main():
    while True:
        try:
            content_type, url = get_user_input()
            
            print(f"\nInitializing scraping with:")
            print(f"Filter Method: {content_type}")
            print(f"URL: {url}")
            
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
            
            print("\nStarting content scraping and generation...")
            await agent.run()

            print("\nTask Results:")
            for task_id, task in agent.task_manager.tasks.items():
                print(f"\nTask: {task_id}")
                print(f"Status: {task.status.value}")
                if task.error:
                    print(f"Error: {task.error}")
                elif task.result:
                    if isinstance(task.result, dict):
                        print("Content length:", len(task.result.get('content', '')))
                    else:
                        print("Content length:", len(str(task.result)))
            
            # Ask if user wants to continue
            while True:
                choice = input("\nWould you like to scrape another URL? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    print("\nExiting program...")
                    return
                else:
                    print("\nPlease enter 'y' or 'n'")
        
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            while True:
                choice = input("\nWould you like to try again? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    print("\nExiting program...")
                    return
                else:
                    print("\nPlease enter 'y' or 'n'")

if __name__ == "__main__":
    print("Press Ctrl+C to cancel at any time.")
    asyncio.run(main()) 