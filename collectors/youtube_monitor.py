from pytz import timezone
from googleapiclient.discovery import build
from datetime import datetime
from typing import List, Dict

class YoutubeMonitor:
    def __init__(self, api_key: str, channels: List[str]):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.channels = channels
        self._channel_ids = {}
    
    def get_channel_id(self, handle: str) -> str:
        if handle in self._channel_ids:
            return self._channel_ids[handle]

        request = self.youtube.search().list(
            part="snippet",
            q=handle,
            type="channel",
            maxResults=1
        )

        response = request.execute()
        if response['items']:
            c_id = response['items'][0]['snippet']['channelId']
            self._channel_ids[handle] = c_id
            return c_id
        return None
    
    def check_for_new_videos(self, hours_ago: int = 24) -> List[Dict]:
        """Check subscribed channels for vidoes published in last X hours"""

        new_videos = []
        for handle in self.channels:
            channel_id = self.get_channel_id(handle)
            if not channel_id:
                print(f"Could not find channel for {handle}")
                continue
        
            request = self.youtube.search().list(
                part="snippet",
                channelId=channel_id,
                order="date",
                type="video",
                publishedAfter=self._get_time_str(hours_ago),
                maxResults=3
            )

            response = request.execute()

            for item in response.get('items', []):
                new_videos.append({
                    'title': item['snippet']['title'],
                    'channel': handle, 
                    'video_id': item['id'].get('videoId', ''),
                    'published_at': item['snippet']['publishedAt']
                })
        return new_videos
    
    def _get_time_str(self, hours_ago: int) -> str:
        from datetime import timedelta
        dt = datetime.now(timezone('UTC')) - timedelta(hours=hours_ago)
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
