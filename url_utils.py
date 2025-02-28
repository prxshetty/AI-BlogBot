import re
from urllib.parse import urlparse, parse_qs

class URLProcessor:
    @staticmethod
    def get_url_type(url: str) -> tuple[str, str]:
        """
        Determines the type of URL and extracts relevant ID if applicable.
        Returns: (url_type, id)
        """
        if not url:
            return "invalid", ""

        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url.lstrip('/')

        # YouTube URL patterns
        youtube_patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]+)',
            r'youtube\.com\/shorts\/([a-zA-Z0-9_-]+)'
        ]

        for pattern in youtube_patterns:
            match = re.search(pattern, url)
            if match:
                return "youtube", match.group(1)

        # If no match found, assume it's a regular website
        return "website", url

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validates if the URL is properly formatted."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False 