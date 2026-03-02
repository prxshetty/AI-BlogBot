import os
import asyncio
import yaml
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from core.models import TopicCollection
from collectors.serper import SerperCollector
from collectors.youtube_monitor import YoutubeMonitor

load_dotenv()

class MonitorService:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.yt_monitor = YoutubeMonitor(
            os.environ.get("YOUTUBE_API_KEY"),
            self.config.get('youtube_channels', [])
        )
        
        # Ensure output directory exists
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

        self.collectors = [
            SerperCollector(os.environ.get("SERPER_API_KEY")),
        ]

    async def run(self):
        print(" Checking Youtube channels for new content...")
        new_videos = self.yt_monitor.check_for_new_videos()

        if not new_videos:
            print("No new videos found")
            return
        
        for video in new_videos:
            print(f" Found new video: {video['title']}({video['channel']})")
            confirm = input("Run data collection for this topic? (y/n): ")
            if confirm.lower() == 'y':
                await self.collect_data(video['title'], video.get('video_id'))

    async def collect_data(self, topic: str, video_id: str):
        print(f"Starting collection for: {topic}")

        collection = TopicCollection(topic=topic, keywords=topic.split())

        # 1. Fetch YouTube Transcript first
        print("  🎥 Fetching YouTube transcript...")
        transcript = self.yt_monitor.get_transcript(video_id)
        if transcript:
            from core.models import SourceContent
            collection.sources.append(SourceContent(
                source_type='youtube_transcript',
                source_url=f"https://youtube.com/watch?v={video_id}",
                title=f"{topic} (Transcript)",
                content=transcript,
                timestamp=datetime.now()
            ))
            print("  ✅ Transcript fetched successfully.")
        else:
            print("  ❌ No transcript found.")

        # 2. Add Serper Context
        tasks = [c.collect(topic) for c in self.collectors]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for res in results:
            if isinstance(res, list):
                collection.sources.extend(res)
            else:
                print(f"Collection error: {res}")

        # 3. Dump to local JSON file
        self._dump_to_file(collection, video_id)
        print(f"Total sources collected: {len(collection.sources)}")

    def _dump_to_file(self, collection: TopicCollection, video_id: str):
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_title = "".join([c for c in collection.topic if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        safe_title = safe_title.replace(' ', '_')[:30]
        filename = f"{date_str}_{safe_title}_{video_id}.json"
        
        filepath = self.output_dir / filename
        
        data = {
            "topic": collection.topic,
            "keywords": collection.keywords,
            "sources": [
                {
                    "source_type": s.source_type,
                    "source_url": s.source_url,
                    "title": s.title,
                    "content": s.content,
                    "author": s.author,
                    "timestamp": s.timestamp.isoformat() if s.timestamp else None,
                    "metadata": s.metadata
                }
                for s in collection.sources
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"data saved! file path: {filepath}")

if __name__ == "__main__":
    service = MonitorService()
    asyncio.run(service.run())
