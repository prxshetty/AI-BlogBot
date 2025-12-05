from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import os
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeProcessor:
    def __init__(self):
        self.output_dir = "captions"
        os.makedirs(self.output_dir, exist_ok=True)

    async def process_video(self, video_id: str) -> Optional[dict]:
        """
        Process a YouTube video by fetching its captions.
        Returns a dictionary containing the processed content.
        """
        try:
            logger.info(f"🎥 Processing YouTube video: {video_id}")
            transcript = self._fetch_transcript(video_id)
            
            if not transcript:
                return None

            # Convert transcript to plain text
            content = "\n".join([item.text for item in transcript])
            
            # Save captions to file
            output_file = os.path.join(self.output_dir, f"{video_id}.txt")
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(content)
            
            logger.info(f"✅ Successfully processed video {video_id}")
            logger.info(f"📝 Captions saved to: {output_file}")
            
            return {
                'content': content,
                'video_id': video_id,
                'source_type': 'youtube'
            }

        except Exception as e:
            logger.error(f"❌ Error processing video {video_id}: {str(e)}")
            return None

    def _fetch_transcript(self, video_id: str):
        """Fetch transcript for a video, trying both manual and auto-generated captions."""
        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            
            try:
                logger.info("🔍 Searching for manual captions...")
                transcript = transcript_list.find_manually_created_transcript(['en']).fetch()
                logger.info("✅ Manual captions found!")
                return transcript
            except NoTranscriptFound:
                logger.info("⚠️ No manual captions found. Trying auto-generated captions...")
                transcript = transcript_list.find_generated_transcript(['en']).fetch()
                logger.info("✅ Auto-generated captions found!")
                return transcript
                
        except NoTranscriptFound:
            logger.error("❌ No captions available (manual or auto-generated)")
        except TranscriptsDisabled:
            logger.error("❌ Captions are disabled for this video")
        except Exception as e:
            logger.error(f"❌ Error fetching transcript: {str(e)}")
        
        return None 