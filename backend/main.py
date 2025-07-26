from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Import our services and models
try:
    from services.youtube_service import YouTubeService
    from services.ai_service import AIService
    from services.auth_service import AuthService
    from services.progress_service import ProgressService
    from services.notes_service import NotesService
    from services.transcription_service import TranscriptionService
    from models.database import get_db, create_tables, User
    print("✅ All imports successful")
except ImportError as e:
    print(f"⚠️ Warning: Some imports failed: {e}")
    print("Application will start with limited functionality")
    # Set services to None - they'll be handled gracefully
    YouTubeService = None
    AIService = None
    AuthService = None
    ProgressService = None
    NotesService = None
    TranscriptionService = None
    get_db = None
    create_tables = None
    User = None

# Load environment variables
load_dotenv()

# Create database tables
if create_tables:
    try:
        create_tables()
        print("✅ Database tables created/verified successfully")
    except Exception as e:
        print(f"⚠️ Warning: Database initialization failed: {e}")
        print("Application will continue with limited functionality")
else:
    print("⚠️ Warning: Database not available")

app = FastAPI(
    title="Zyndle AI API",
    description="AI-powered learning companion for YouTube videos",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:3000",
        "https://*.railway.app",
        "https://*.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
import os
print(f"Backend working directory: {os.getcwd()}")
frontend_dist = Path("../frontend/dist")
print(f"Looking for frontend at: {frontend_dist.absolute()}")
print(f"Frontend dist exists: {frontend_dist.exists()}")

if frontend_dist.exists():
    print("Frontend dist found! Setting up static file serving...")
    # Mount static assets
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend index.html"""
        index_path = frontend_dist / "index.html"
        print(f"Looking for index.html at: {index_path.absolute()}")
        if index_path.exists():
            print("Serving frontend index.html")
            return FileResponse(str(index_path))
        else:
            print("index.html not found, serving API message")
            return {"message": "Zyndle AI API is running!"}
else:
    print("Frontend dist not found! Serving API only.")
    @app.get("/")
    async def root():
        return {"message": "Zyndle AI API is running!"}

# Initialize services
youtube_service = None
ai_service = None
auth_service = None
progress_service = None
notes_service = None
transcription_service = None

try:
    if YouTubeService:
        youtube_service = YouTubeService()
    if AIService:
        ai_service = AIService()
    if AuthService:
        auth_service = AuthService()
    if ProgressService:
        progress_service = ProgressService()
    if NotesService:
        notes_service = NotesService()
    if TranscriptionService:
        transcription_service = TranscriptionService()
    print("✅ All available services initialized successfully")
except Exception as e:
    print(f"❌ Error initializing services: {e}")
    print("Application will continue with limited functionality")

# Security
security = HTTPBearer(auto_error=False)

# Pydantic models for authentication
class UserRegister(BaseModel):
    email: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: str

# Pydantic models for video analysis
class VideoAnalysisRequest(BaseModel):
    youtube_url: str

class VideoAnalysisResponse(BaseModel):
    title: str
    channel: str
    duration: str
    summary: str
    chapters: List[dict]
    transcript: str
    thumbnail: Optional[str] = None
    view_count: Optional[str] = None
    like_count: Optional[str] = None

class ChatRequest(BaseModel):
    question: str
    video_id: str
    transcript: str
    summary: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: str

class QuizRequest(BaseModel):
    video_id: str
    transcript: str
    summary: str
    num_questions: int = 5

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class QuizResponse(BaseModel):
    questions: List[QuizQuestion]

# Simple dependency to get current user (for now, just return a mock user)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # For now, return a mock user to allow the application to work
    # In production, you would validate the token and get the real user
    class MockUser:
        def __init__(self):
            self.id = 1
            self.email = "demo@example.com"
            self.full_name = "Demo User"
    
    # If no credentials provided, still return mock user
    if not credentials:
        return MockUser()
    
    # If credentials provided, validate the token (simplified)
    try:
        # For now, accept any token that starts with "mock_token"
        if credentials.credentials and credentials.credentials.startswith("mock_token"):
            return MockUser()
        else:
            # Return mock user anyway for now
            return MockUser()
    except Exception as e:
        print(f"Token validation error: {e}")
        # Return mock user anyway for now
        return MockUser()

@app.get("/health")
async def health_check():
    """Simple health check endpoint that doesn't depend on external services"""
    return {
        "status": "healthy", 
        "message": "Zyndle AI API is running",
        "version": "1.0.0"
    }

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service status"""
    try:
        return {
            "status": "healthy", 
            "services": {
                "youtube": "available" if youtube_service else "unavailable", 
                "ai": "available" if ai_service else "unavailable",
                "transcription": "available" if transcription_service else "unavailable"
            },
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "version": "1.0.0"
        }

# Authentication endpoints (simplified for now)
@app.post("/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    """Register a new user (simplified version)"""
    try:
        # For now, just return a mock token
        return {
            "access_token": "mock_token_123",
            "token_type": "bearer",
            "user_id": 1,
            "email": user_data.email,
            "full_name": user_data.full_name
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login user (simplified version)"""
    try:
        # For now, just return a mock token
        return {
            "access_token": "mock_token_123",
            "token_type": "bearer",
            "user_id": 1,
            "email": user_data.email,
            "full_name": "Demo User"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "created_at": "2024-01-01T00:00:00Z"
    }

@app.post("/auth/logout")
async def logout():
    """Logout user (simplified version)"""
    return {"message": "Logged out successfully"}

@app.post("/analyze", response_model=VideoAnalysisResponse)
async def analyze_video(request: VideoAnalysisRequest, current_user = Depends(get_current_user)):
    """Analyze a YouTube video and return summary, chapters, and transcript"""
    try:
        print(f"Analyzing video: {request.youtube_url}")
        print(f"Current user: {current_user.email}")
        
        if not youtube_service:
            print("YouTube service not available")
            raise HTTPException(status_code=500, detail="YouTube service not available")
        
        # Extract video ID from URL
        video_id = youtube_service.extract_video_id(request.youtube_url)
        if not video_id:
            print(f"Invalid YouTube URL: {request.youtube_url}")
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        print(f"Extracted video ID: {video_id}")
        
        # Get video metadata
        metadata = youtube_service.get_video_metadata(video_id)
        print(f"Got metadata: {metadata.get('title', 'Unknown')}")
        
        # Get real transcript using transcription service
        transcript = None
        if transcription_service:
            print("Attempting to get real transcript...")
            transcript = youtube_service.get_video_transcript(video_id)
        
        # Fallback to mock transcript if real transcription fails
        if not transcript:
            print(f"Warning: Failed to get real transcript for video {video_id}, using mock transcript")
            transcript = f"This is a transcript for {metadata['title']}. The video covers important concepts and provides valuable insights for learners."
        
        # Generate AI summary based on real transcript
        ai_summary = None
        if ai_service:
            print("Generating AI summary...")
            ai_summary = ai_service.generate_summary(transcript, metadata['title'])
        else:
            print("AI service not available, using mock summary")
            # Fallback mock summary
            ai_summary = {
                "summary": f"This video covers important concepts related to {metadata['title']}. The content is well-structured and provides valuable insights for learners.",
                "chapters": [
                    {"title": "Introduction", "start": 0, "end": 180, "description": "Overview and context"},
                    {"title": "Main Concepts", "start": 180, "end": 480, "description": "Core principles explained"},
                    {"title": "Examples", "start": 480, "end": 780, "description": "Practical demonstrations"},
                    {"title": "Conclusion", "start": 780, "end": 930, "description": "Summary and next steps"}
                ]
            }
        
        # Prepare response data
        response_data = {
            "title": metadata['title'],
            "channel": metadata['channel'],
            "duration": metadata['duration'],
            "summary": ai_summary['summary'],
            "chapters": ai_summary['chapters'],
            "transcript": transcript,
            "thumbnail": metadata.get('thumbnail'),
            "view_count": metadata.get('view_count'),
            "like_count": metadata.get('like_count')
        }
        
        print(f"Returning response with title: {response_data['title']}")
        return response_data
    except Exception as e:
        print(f"Error in analyze_video: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_video(request: ChatRequest):
    """Ask questions about a specific video"""
    try:
        if not ai_service:
            # Fallback mock response
            return ChatResponse(
                answer="I'm sorry, the AI service is currently unavailable. Please try again later.",
                sources=["Video transcript", "Summary"],
                confidence="low"
            )
        
        # Generate AI response
        response = ai_service.chat_with_video(
            request.question, 
            request.transcript, 
            request.summary
        )
        
        return ChatResponse(
            answer=response['answer'],
            sources=response['sources'],
            confidence=response['confidence']
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """Generate quiz questions based on video content"""
    try:
        if not ai_service:
            # Fallback mock quiz
            questions = [
                QuizQuestion(
                    question="What is the main topic of this video?",
                    options=["Machine Learning", "Web Development", "Cooking", "Music"],
                    correct_answer=0,
                    explanation="The video primarily focuses on machine learning concepts."
                )
            ]
            return QuizResponse(questions=questions)
        
        # Generate AI quiz questions
        questions = ai_service.generate_quiz(
            request.transcript, 
            request.summary, 
            request.num_questions
        )
        
        # Convert to Pydantic models
        quiz_questions = [
            QuizQuestion(
                question=q['question'],
                options=q['options'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation']
            ) for q in questions
        ]
        
        return QuizResponse(questions=quiz_questions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/videos/{video_id}/metadata")
async def get_video_metadata(video_id: str):
    """Get metadata for a specific video"""
    try:
        if not youtube_service:
            raise HTTPException(status_code=500, detail="YouTube service not available")
        
        metadata = youtube_service.get_video_metadata(video_id)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/videos/{video_id}/transcript")
async def get_video_transcript(video_id: str, current_user = Depends(get_current_user)):
    """Get transcript for a specific video (for testing)"""
    try:
        if not youtube_service:
            raise HTTPException(status_code=500, detail="YouTube service not available")
        
        transcript = youtube_service.get_video_transcript(video_id)
        if transcript:
            return {
                "video_id": video_id,
                "transcript": transcript,
                "length": len(transcript)
            }
        else:
            raise HTTPException(status_code=404, detail="Transcript not available")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Catch-all route for SPA routing - must be at the very end
if frontend_dist.exists():
    @app.get("/{full_path:path}")
    async def serve_frontend_routes(full_path: str):
        """Serve frontend for all non-API routes"""
        # Don't serve API routes
        if full_path.startswith(("auth/", "analyze", "chat", "quiz", "health", "api/")):
            raise HTTPException(status_code=404, detail="Not found")
        
        # Try to serve static files first
        static_path = frontend_dist / full_path
        if static_path.exists() and static_path.is_file():
            return FileResponse(str(static_path))
        
        # Fall back to index.html for SPA routes
        index_path = frontend_dist / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        else:
            return {"message": "Zyndle AI API is running!"} 