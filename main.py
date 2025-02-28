import asyncio
import os
from dotenv import load_dotenv
from ai_agent import AIAgent
from url_utils import URLProcessor
from youtube_processor import YouTubeProcessor
import logging
from rich.console import Console
from rich.panel import Panel
from utils import save_content_to_file
from task_manager import TaskStatus

console = Console()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def print_welcome():
    welcome_text = """
    =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    🤖 Blog Content Generator 🤖
    *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
    Generate blog posts from:
    - 🌐 Websites
    - 📺 YouTube Videos
    """
    console.print(Panel(welcome_text, title="Welcome", border_style="blue"))

def get_user_input():
    while True:
        url = input("\n🔗 Enter URL (website or YouTube video): ").strip()
        if url.lower() == 'exit':
            console.print("\n👋 Goodbye!", style="bold blue")
            exit(0)
        
        url_processor = URLProcessor()
        if url and url_processor.validate_url(url):
            url_type, identifier = url_processor.get_url_type(url)
            if url_type == "website":
                while True:
                    print("\n📝 Select content filter method:")
                    console.print("[1] raw - Get raw content")
                    console.print("[2] filter - Get filtered content")
                    console.print("[3] exit - Exit the program")
                    choice = input("\n👉 Enter your choice (1-3): ").strip()
            
                    if choice == "3":
                        console.print("\n👋 Goodbye!", style="bold blue")
                        exit(0)
                    elif choice in ["1", "2"]:
                        content_type = "raw" if choice == "1" else "filter"
                        break
                    else:
                        console.print("❌ Invalid choice. Please enter 1, 2, or 3.", style="bold red")
            else:
                content_type = None
            
            while True:
                print("\n📝 Select blog type:")
                console.print("[1] Standard Blog Post")
                console.print("[2] Opinionated Tech Blog Post")
                blog_choice = input("\n👉 Enter your choice (1-2): ").strip()
                
                if blog_choice in ["1", "2"]:
                    blog_type = "standard" if blog_choice == "1" else "opinionated"
                    break
                else:
                    console.print("❌ Invalid choice. Please enter 1 or 2.", style="bold red")
            
            return content_type, url, url_type, identifier, blog_type
        else:
            console.print("❌ Invalid URL. Please enter a valid URL or 'exit' to quit.", style="bold red")

async def main():
    print_welcome()
    
    while True:
        try:
            content_type, url, url_type, identifier, blog_type = get_user_input()
            
            console.print(f"\n🔍 Processing {'YouTube video' if url_type == 'youtube' else 'website'}: {url}", style="bold blue")
            
            agent = AIAgent(llm_provider="llama-3.3-70b-versatile")

            if url_type == "youtube":
                agent.task_manager.add_task(
                    task_id="youtube_transcript",
                    description=f"youtube_transcript_{identifier}",
                    dependencies=[]
                )
                agent.task_manager.add_task(
                    task_id="generate_blog_post",
                    description=f"generate:{blog_type}",
                    dependencies=["youtube_transcript"],
                )
                youtube_processor = YouTubeProcessor()
                transcript = await youtube_processor.process_video(identifier)
                
                if not transcript:
                    raise ValueError("Failed to process YouTube video")                
                youtube_task = agent.task_manager.tasks["youtube_transcript"]
                youtube_task.result = {
                    'content': transcript,
                    'source_type': 'youtube'
                }
                youtube_task.status = TaskStatus.COMPLETED
                
            else:
                agent.task_manager.add_task(
                    task_id="scrape_blog",
                    description=f"scrape_{content_type}_{url}",
                    dependencies=[]
                )
                agent.task_manager.add_task(
                    task_id="generate_blog_post",
                    description=f"generate:{blog_type}",
                    dependencies=["scrape_blog"]
                )            
            console.print("\nStarting content processing and generation...", style="bold blue")
            await agent.run()            
            generate_task = agent.task_manager.tasks["generate_blog_post"]
            if generate_task.status == TaskStatus.FAILED:
                raise ValueError(generate_task.error or "Failed to generate blog post")
            
            blog_content = generate_task.result
            if not blog_content or not isinstance(blog_content, str):
                raise ValueError("Generated content is empty or invalid")          
            file_prefix = f"youtube_{identifier}" if url_type == "youtube" else "blog"
            save_content_to_file(blog_content, file_prefix)
            console.print(f"\n📝 Blog post saved successfully.", style="bold green")
            
            while True:
                choice = input("\nWould you like to process another URL? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    console.print("\n👋 Goodbye!", style="bold blue")
                    return
                else:
                    console.print("\nPlease enter 'y' or 'n'", style="bold red")
                    
        except KeyboardInterrupt:
            console.print("\n\nOperation cancelled by user.", style="bold yellow")
            return
        except Exception as e:
            console.print(f"\n❌ An error occurred: {str(e)}", style="bold red")
            logger.error(f"Error processing content: {str(e)}", exc_info=True)
            while True:
                choice = input("\nWould you like to try again? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    console.print("\n👋 Goodbye!", style="bold blue")
                    return
                else:
                    console.print("\nPlease enter 'y' or 'n'", style="bold red")

if __name__ == "__main__":
    console.print("ℹPress Ctrl+C to cancel at any time.\n", style="bold blue")
    asyncio.run(main())