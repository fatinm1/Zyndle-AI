"""
Configuration settings for video transcription
"""

import os
from typing import Dict, Any

class TranscriptionConfig:
    """Configuration for video transcription settings"""
    
    # Whisper model settings
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')  # Options: tiny, base, small, medium, large
    
    # Audio processing settings
    AUDIO_QUALITY = os.getenv('AUDIO_QUALITY', '192')  # kbps
    AUDIO_FORMAT = os.getenv('AUDIO_FORMAT', 'mp3')
    
    # Download settings
    MAX_VIDEO_DURATION = int(os.getenv('MAX_VIDEO_DURATION', '3600'))  # 1 hour in seconds
    DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', '300'))  # 5 minutes
    
    # Transcription settings
    LANGUAGE = os.getenv('WHISPER_LANGUAGE', None)  # Auto-detect if None
    TASK = os.getenv('WHISPER_TASK', 'transcribe')  # 'transcribe' or 'translate'
    
    # Caching settings
    ENABLE_CACHE = os.getenv('ENABLE_TRANSCRIPT_CACHE', 'true').lower() == 'true'
    CACHE_DIR = os.getenv('TRANSCRIPT_CACHE_DIR', './cache/transcripts')
    
    # Error handling
    MAX_RETRIES = int(os.getenv('TRANSCRIPT_MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('TRANSCRIPT_RETRY_DELAY', '5'))  # seconds
    
    @classmethod
    def get_whisper_options(cls) -> Dict[str, Any]:
        """Get Whisper transcription options"""
        options = {
            'model': cls.WHISPER_MODEL,
            'task': cls.TASK,
        }
        
        if cls.LANGUAGE:
            options['language'] = cls.LANGUAGE
            
        return options
    
    @classmethod
    def get_yt_dlp_options(cls) -> Dict[str, Any]:
        """Get yt-dlp download options"""
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': cls.AUDIO_FORMAT,
                'preferredquality': cls.AUDIO_QUALITY,
            }],
            'quiet': True,
            'no_warnings': True,
            'extractaudio': True,
            'audioformat': cls.AUDIO_FORMAT,
            'audioquality': cls.AUDIO_QUALITY,
        }
    
    @classmethod
    def validate_video_duration(cls, duration_seconds: int) -> bool:
        """Check if video duration is within limits"""
        return duration_seconds <= cls.MAX_VIDEO_DURATION 