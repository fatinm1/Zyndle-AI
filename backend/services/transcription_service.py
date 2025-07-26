import os
import tempfile
import yt_dlp
import whisper
from typing import Optional, Dict
import logging
import time
from config.transcription_config import TranscriptionConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self):
        self.model = None
        self._load_whisper_model()
    
    def _load_whisper_model(self):
        """Load Whisper model (lazy loading to avoid startup delays)"""
        try:
            logger.info(f"Loading Whisper model: {TranscriptionConfig.WHISPER_MODEL}")
            # Load model based on configuration
            self.model = whisper.load_model(TranscriptionConfig.WHISPER_MODEL)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            self.model = None
    
    def download_video_audio(self, video_id: str) -> Optional[str]:
        """Download video and extract audio to a temporary file"""
        try:
            # Create temporary file for audio
            temp_audio_file = tempfile.NamedTemporaryFile(
                suffix='.mp3', 
                delete=False,
                prefix=f'video_{video_id}_'
            )
            temp_audio_path = temp_audio_file.name
            temp_audio_file.close()
            
            # Configure yt-dlp options
            ydl_opts = TranscriptionConfig.get_yt_dlp_options()
            ydl_opts['outtmpl'] = temp_audio_path
            
            # Construct video URL
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            logger.info(f"Downloading audio for video: {video_id}")
            
            # Download the video/audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            # Check if file was created successfully
            if os.path.exists(temp_audio_path):
                logger.info(f"Audio downloaded successfully: {temp_audio_path}")
                return temp_audio_path
            else:
                logger.error("Audio file was not created")
                return None
                
        except Exception as e:
            logger.error(f"Error downloading video audio: {e}")
            # Clean up temp file if it exists
            if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
            return None
    
    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio file using Whisper"""
        try:
            if not self.model:
                logger.error("Whisper model not loaded")
                return None
            
            logger.info(f"Transcribing audio: {audio_file_path}")
            
            # Transcribe the audio
            whisper_options = TranscriptionConfig.get_whisper_options()
            result = self.model.transcribe(audio_file_path, **whisper_options)
            transcript = result["text"]
            
            logger.info(f"Transcription completed. Length: {len(transcript)} characters")
            return transcript
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None
    
    def get_video_transcript(self, video_id: str) -> Optional[str]:
        """Complete pipeline: download video and transcribe audio with retry logic"""
        temp_audio_path = None
        
        for attempt in range(TranscriptionConfig.MAX_RETRIES):
            try:
                logger.info(f"Attempt {attempt + 1}/{TranscriptionConfig.MAX_RETRIES} for video {video_id}")
                
                # Step 1: Check video duration before downloading
                video_info = self.get_video_info(video_id)
                if video_info and video_info.get('duration'):
                    duration_seconds = video_info['duration']
                    if not TranscriptionConfig.validate_video_duration(duration_seconds):
                        logger.error(f"Video too long: {duration_seconds} seconds (max: {TranscriptionConfig.MAX_VIDEO_DURATION})")
                        return None
                
                # Step 2: Download video audio
                temp_audio_path = self.download_video_audio(video_id)
                if not temp_audio_path:
                    logger.error("Failed to download video audio")
                    if attempt < TranscriptionConfig.MAX_RETRIES - 1:
                        time.sleep(TranscriptionConfig.RETRY_DELAY)
                        continue
                    return None
                
                # Step 3: Transcribe audio
                transcript = self.transcribe_audio(temp_audio_path)
                if not transcript:
                    logger.error("Failed to transcribe audio")
                    if attempt < TranscriptionConfig.MAX_RETRIES - 1:
                        time.sleep(TranscriptionConfig.RETRY_DELAY)
                        continue
                    return None
                
                logger.info(f"Successfully transcribed video {video_id} on attempt {attempt + 1}")
                return transcript
                
            except Exception as e:
                logger.error(f"Error in video transcript pipeline (attempt {attempt + 1}): {e}")
                if attempt < TranscriptionConfig.MAX_RETRIES - 1:
                    time.sleep(TranscriptionConfig.RETRY_DELAY)
                    continue
                return None
            finally:
                # Clean up temporary audio file
                if temp_audio_path and os.path.exists(temp_audio_path):
                    try:
                        os.unlink(temp_audio_path)
                        logger.info(f"Cleaned up temporary file: {temp_audio_path}")
                    except Exception as e:
                        logger.error(f"Error cleaning up temp file: {e}")
        
        return None
    
    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """Get video information without downloading"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'description': info.get('description'),
                    'uploader': info.get('uploader'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'thumbnail': info.get('thumbnail'),
                }
                
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None 