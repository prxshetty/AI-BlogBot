from pytz import timezone
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeMonitor:
    def __init__(self, api_key: str, channels: List[str]):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.channels = channels
        self._channel_ids = {}
    
    def get_channel_id(self, handle: str) -> str:
        if handle in self._channel_ids:
            return self._channel_ids[handle]

        if handle.startswith('@'):
            request = self.youtube.channels().list(
                part="id",
                forHandle=handle
            )
            response = request.execute()
            if response.get('items'):
                c_id = response['items'][0]['id']
                self._channel_ids[handle] = c_id
                return c_id

        # Fallback to search if handle doesn't start with @
        request = self.youtube.search().list(
            part="snippet",
            q=handle,
            type="channel",
            maxResults=1
        )

        response = request.execute()
        if response.get('items'):
            c_id = response['items'][0]['snippet']['channelId']
            self._channel_ids[handle] = c_id
            return c_id
        return None
    
    def check_for_new_videos(self, hours_ago: int = 72) -> List[Dict]:
        """Check subscribed channels for vidoes published in last X hours"""

        new_videos = []
        for handle in self.channels:
            channel_id = self.get_channel_id(handle)
            if not channel_id:
                print(f"Could not find channel for {handle}")
                continue
        
            # The uploads playlist ID is the channel ID with the second character changed to 'U'
            uploads_playlist_id = "UU" + channel_id[2:]
            
            request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=5
            )

            response = request.execute()
            
            cutoff_time = datetime.now(timezone('UTC')) - timedelta(hours=hours_ago)

            for item in response.get('items', []):
                published_str = item['snippet']['publishedAt']
                # publishedAt is in the format "2024-02-05T00:00:00Z"
                published_dt = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone('UTC'))
                
                if published_dt >= cutoff_time:
                    video_id = item['snippet']['resourceId'].get('videoId', '')
                    new_videos.append({
                        'title': item['snippet']['title'],
                        'channel': handle, 
                        'video_id': video_id,
                        'youtube_url': f"https://youtube.com/watch?v={video_id}",
                        'published_at': published_str
                    })
        return new_videos
    
    def get_transcript(self, video_id: str) -> Optional[str]:
        """Fetch English transcript for a given video ID"""
        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id).find_transcript(['en']).fetch()
            # Join all text pieces
            full_transcript = " ".join([t.text for t in transcript_list])
            return full_transcript
        except Exception as e:
            print(f"⚠️ Could not fetch transcript for {video_id}: {e}")
            return None
    
    def _get_time_str(self, hours_ago: int) -> str:
        from datetime import timedelta
        dt = datetime.now(timezone('UTC')) - timedelta(hours=hours_ago)
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
