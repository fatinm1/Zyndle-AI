import re
import requests
from typing import Dict, Optional
import os

class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_video_metadata(self, video_id: str) -> Dict:
        """Get video metadata from YouTube Data API"""
        if not self.api_key:
            # Return mock data if no API key
            return self._get_mock_metadata(video_id)
        
        try:
            url = f"https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,contentDetails,statistics',
                'id': video_id,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data['items']:
                item = data['items'][0]
                snippet = item['snippet']
                content_details = item['contentDetails']
                
                return {
                    'title': snippet['title'],
                    'channel': snippet['channelTitle'],
                    'duration': self._parse_duration(content_details['duration']),
                    'description': snippet['description'],
                    'thumbnail': snippet['thumbnails']['high']['url'],
                    'view_count': item['statistics'].get('viewCount', 0),
                    'like_count': item['statistics'].get('likeCount', 0)
                }
        except Exception as e:
            print(f"Error fetching video metadata: {e}")
            return self._get_mock_metadata(video_id)
    
    def _parse_duration(self, duration: str) -> str:
        """Parse ISO 8601 duration to readable format"""
        import re
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
        if match:
            hours, minutes, seconds = match.groups()
            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0
            seconds = int(seconds) if seconds else 0
            
            if hours > 0:
                return f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes}:{seconds:02d}"
        return "0:00"
    
    def _get_mock_metadata(self, video_id: str) -> Dict:
        """Return mock metadata for development"""
        mock_videos = {
            "dQw4w9WgXcQ": {
                "title": "Rick Astley - Never Gonna Give You Up",
                "channel": "Rick Astley",
                "duration": "3:33",
                "description": "A classic pop song about commitment and loyalty in relationships.",
                "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
                "view_count": "1234567890",
                "like_count": "9876543"
            }
        }
        
        return mock_videos.get(video_id, {
            "title": "Sample Educational Video",
            "channel": "Educational Channel",
            "duration": "15:30",
            "description": "This video covers important concepts in machine learning and artificial intelligence.",
            "thumbnail": "https://i.ytimg.com/vi/sample/hqdefault.jpg",
            "view_count": "1000000",
            "like_count": "50000"
        }) 