from data_models import TopicCollection
from collectors.serper import SerperCollector
from collectors.youtube_monitor import YoutubeMonitor
import asyncio
import yaml

class MonitorService:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        keys = self.config['api_keys']

        self.yt_monitor = YoutubeMonitor(keys['youtube'],
        self.config['youtube_channels'])
        self.store = DataStore()

        self.collectors = [
            SerperCollector(keys['serper']),
        ]

        async def run(self):
            print(" Checking Youtube channels for new content...")
            new_videos = self.yt_monitor.check_for_new_videos()

            if not new_videos:
                print("No new videos found")
                return
            
            for video in new_videos:
                print(f" Found new video: {video['title']}({video['channel']})")
                confirm = input("Run data collection for this topic? (y/n)")
                if confirm.lower() == 'y':
                    await self.collect_data(video['title'], video['video_id'])

        async def collect_data(self, topic: str, video_id: str):
            print("Starting collection for: {topic}")

            collection = TopicCollection(topic=topic, keywords=topic.split())

            tasks = [c.collect(topic) for c in self.collectors]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for res in results:
                if isinstance(res, list):
                    collection.sources.extend(res)
                else:
                    print("Collection error: {res}")

            topic_id = self.store.save_topic(collection)
            print(f"data saved! topic id: {topic_id}")
            print(f"Total sources collected: {len(collection.sources)}")

if __name__ == "__main__":
    service = MonitorService()
    asyncio.run(service.run())
