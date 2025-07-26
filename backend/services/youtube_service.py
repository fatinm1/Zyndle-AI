import re
import requests
from typing import Dict, Optional
import os
# Try to import transcription service, but don't fail if it's not available
try:
    from .transcription_service import TranscriptionService
    TRANSCRIPTION_AVAILABLE = True
except ImportError:
    TranscriptionService = None
    TRANSCRIPTION_AVAILABLE = False

class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if TRANSCRIPTION_AVAILABLE:
            self.transcription_service = TranscriptionService()
        else:
            self.transcription_service = None
    
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
        """Get video metadata from YouTube Data API or yt-dlp"""
        # Try YouTube Data API first if we have an API key
        if self.api_key:
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
                print(f"Error fetching video metadata from YouTube API: {e}")
        
        # Fallback to yt-dlp for metadata
        try:
            yt_info = self.transcription_service.get_video_info(video_id)
            if yt_info:
                return {
                    'title': yt_info.get('title', 'Unknown Title'),
                    'channel': yt_info.get('uploader', 'Unknown Channel'),
                    'duration': self._format_duration(yt_info.get('duration', 0)),
                    'description': yt_info.get('description', ''),
                    'thumbnail': yt_info.get('thumbnail', ''),
                    'view_count': str(yt_info.get('view_count', 0)),
                    'like_count': str(yt_info.get('like_count', 0))
                }
        except Exception as e:
            print(f"Error fetching video metadata from yt-dlp: {e}")
        
        # Final fallback to mock data
        return self._get_mock_metadata(video_id)
    
    def get_video_transcript(self, video_id: str) -> Optional[str]:
        """Get real transcript for a video"""
        try:
            return self.transcription_service.get_video_transcript(video_id)
        except Exception as e:
            print(f"Error getting video transcript: {e}")
            return None
    
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
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in seconds to readable format"""
        if not seconds:
            return "0:00"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
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