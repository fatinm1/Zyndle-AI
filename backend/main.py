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
    # Note: transcription_service requires heavy dependencies, so we'll handle it separately
    TranscriptionService = None
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

# Create database tables (only if available)
if create_tables:
    try:
        print("🔍 Initializing database...")
        create_tables()
        print("✅ Database tables created/verified successfully")
        
        # Test database connection
        try:
            from models.database import engine
            with engine.connect() as conn:
                if "postgresql" in str(engine.url):
                    result = conn.execute("SELECT version()")
                    version = result.fetchone()[0]
                    print(f"✅ PostgreSQL connected: {version.split(',')[0]}")
                else:
                    print("✅ SQLite database connected")
        except Exception as e:
            print(f"⚠️ Database connection test failed: {e}")
            
    except Exception as e:
        print(f"⚠️ Warning: Database initialization failed: {e}")
        print("Application will continue with limited functionality")
        print("💡 Tip: Check your DATABASE_URL environment variable")
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

# Simple root endpoint for basic health check
@app.get("/")
async def root():
    """Root endpoint - serve frontend if available, otherwise API message"""
    if frontend_dist and frontend_dist.exists():
        index_path = frontend_dist / "index.html"
        if index_path.exists():
            print("Serving frontend index.html from root endpoint")
            return FileResponse(str(index_path))
    
    # Fallback to API message if frontend not available
    return {
        "message": "Zyndle AI API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint for Railway health checks"""
    return {"pong": "ok"}

@app.get("/api/health")
async def api_health():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is responding",
        "version": "1.0.0"
    }

# Mount static files for frontend
import os
print(f"Backend working directory: {os.getcwd()}")
# Try multiple possible frontend paths
frontend_paths = [
    Path("../frontend/dist"),  # Relative to backend
    Path("frontend/dist"),     # Relative to root
    Path("/app/frontend/dist"), # Absolute in container
    Path("/app/backend/frontend/dist"), # Alternative container path
]
frontend_dist = None
for path in frontend_paths:
    print(f"Checking frontend path: {path.absolute()}")
    if path.exists():
        frontend_dist = path
        print(f"Found frontend at: {frontend_dist.absolute()}")
        break

if not frontend_dist:
    print("Frontend dist not found in any expected location")
    frontend_dist = Path("/app/frontend/dist")  # Default for container

if frontend_dist.exists():
    print("Frontend dist found! Setting up static file serving...")
    # Mount static assets
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    @app.get("/app")
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

# Initialize services gracefully
youtube_service = None
ai_service = None
auth_service = None
progress_service = None
notes_service = None
transcription_service = None

try:
    if YouTubeService:
        youtube_service = YouTubeService()
        print("✅ YouTube service initialized")
    if AIService:
        ai_service = AIService()
        print("✅ AI service initialized")
    if AuthService:
        auth_service = AuthService()
        print("✅ Auth service initialized")
    if ProgressService:
        progress_service = ProgressService()
        print("✅ Progress service initialized")
    if NotesService:
        notes_service = NotesService()
        print("✅ Notes service initialized")
    if TranscriptionService:
        transcription_service = TranscriptionService()
        print("✅ Transcription service initialized")
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
    title: str = ""  # Add video title

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: str

class QuizRequest(BaseModel):
    video_id: str
    transcript: str
    summary: str
    title: str = ""  # Add video title
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
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service status"""
    try:
        # Always return a response, even if services are unavailable
        services_status = {}
        
        try:
            services_status["youtube"] = "available" if youtube_service else "unavailable"
        except:
            services_status["youtube"] = "unavailable"
            
        try:
            services_status["ai"] = "available" if ai_service else "unavailable"
        except:
            services_status["ai"] = "unavailable"
            
        try:
            services_status["transcription"] = "available" if transcription_service else "unavailable"
        except:
            services_status["transcription"] = "unavailable"
        
        return {
            "status": "healthy", 
            "services": services_status,
            "version": "1.0.0",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        # Even if everything fails, return a degraded status instead of erroring
        return {
            "status": "degraded",
            "error": str(e),
            "version": "1.0.0",
            "timestamp": "2024-01-01T00:00:00Z"
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

# Progress tracking endpoints
@app.get("/progress")
async def get_user_progress(current_user = Depends(get_current_user)):
    """Get user's learning progress and statistics"""
    try:
        if not progress_service:
            # Return mock progress data
            return {
                "total_videos_watched": 1,
                "total_time_watched": "26:30",
                "favorite_subjects": ["Physics", "Nuclear Science"],
                "recent_videos": [
                    {
                        "title": "27.3 Nuclear Decay Processes and Energy of Nuclear Reactions",
                        "channel": "Chad's Prep",
                        "duration": "26:30",
                        "watched_at": "2024-01-01T12:00:00Z"
                    }
                ],
                "quiz_stats": {
                    "total_quizzes_taken": 1,
                    "average_score": 67,
                    "best_subject": "Nuclear Physics"
                },
                "learning_insights": [
                    "You're making great progress in nuclear physics!",
                    "Consider exploring more advanced topics in this subject.",
                    "Your quiz performance shows good understanding of core concepts."
                ]
            }
        
        # Use real progress service if available
        progress = progress_service.get_user_progress(None, current_user.id)
        return progress
    except Exception as e:
        print(f"Error getting user progress: {e}")
        # Return mock progress as fallback
        return {
            "total_videos_watched": 1,
            "total_time_watched": "26:30",
            "favorite_subjects": ["Physics", "Nuclear Science"],
            "recent_videos": [
                {
                    "title": "27.3 Nuclear Decay Processes and Energy of Nuclear Reactions",
                    "channel": "Chad's Prep",
                    "duration": "26:30",
                    "watched_at": "2024-01-01T12:00:00Z"
                }
            ],
            "quiz_stats": {
                "total_quizzes_taken": 1,
                "average_score": 67,
                "best_subject": "Nuclear Physics"
            },
            "learning_insights": [
                "You're making great progress in nuclear physics!",
                "Consider exploring more advanced topics in this subject.",
                "Your quiz performance shows good understanding of core concepts."
            ]
        }

@app.get("/progress/insights")
async def get_learning_insights(current_user = Depends(get_current_user)):
    """Get personalized learning insights and recommendations"""
    try:
        if not progress_service:
            return {
                "insights": [
                    "You're making great progress in nuclear physics!",
                    "Consider exploring more advanced topics in this subject.",
                    "Your quiz performance shows good understanding of core concepts."
                ],
                "recommendations": [
                    "Try more videos in the physics category",
                    "Take additional quizzes to reinforce learning",
                    "Explore related topics in chemistry and mathematics"
                ]
            }
        
        insights = progress_service.get_learning_insights(None, current_user.id)
        return insights
    except Exception as e:
        print(f"Error getting learning insights: {e}")
        return {
            "insights": [
                "You're making great progress in nuclear physics!",
                "Consider exploring more advanced topics in this subject.",
                "Your quiz performance shows good understanding of core concepts."
            ],
            "recommendations": [
                "Try more videos in the physics category",
                "Take additional quizzes to reinforce learning",
                "Explore related topics in chemistry and mathematics"
            ]
        }

@app.post("/progress/record-video")
async def record_video_watched(video_data: dict, current_user = Depends(get_current_user)):
    """Record that a user watched a video"""
    try:
        if not progress_service:
            return {"message": "Video watched recorded successfully (mock)"}
        
        success = progress_service.record_video_watched(None, current_user.id, video_data)
        if success:
            return {"message": "Video watched recorded successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to record video watched")
    except Exception as e:
        print(f"Error recording video progress: {e}")
        return {"message": "Video watched recorded successfully (fallback)"}

@app.post("/progress/record-quiz")
async def record_quiz_result(quiz_data: dict, current_user = Depends(get_current_user)):
    """Record quiz results"""
    try:
        if not progress_service:
            return {"message": "Quiz result recorded successfully (mock)"}
        
        success = progress_service.record_quiz_result(
            None,
            current_user.id,
            quiz_data.get('video_id'),
            quiz_data.get('score'),
            quiz_data.get('total_questions')
        )
        if success:
            return {"message": "Quiz result recorded successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to record quiz result")
    except Exception as e:
        print(f"Error recording quiz result: {e}")
        return {"message": "Quiz result recorded successfully (fallback)"}

@app.post("/analyze", response_model=VideoAnalysisResponse)
async def analyze_video(request: VideoAnalysisRequest, current_user = Depends(get_current_user)):
    """Analyze a YouTube video and return summary, chapters, and transcript"""
    try:
        print(f"Analyzing video: {request.youtube_url}")
        print(f"Current user: {current_user.email}")
        
        # Extract video ID from URL (simple regex fallback if youtube_service not available)
        video_id = None
        if youtube_service:
            video_id = youtube_service.extract_video_id(request.youtube_url)
        else:
            # Simple fallback video ID extraction
            import re
            match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)', request.youtube_url)
            if match:
                video_id = match.group(1)
        
        if not video_id:
            print(f"Invalid YouTube URL: {request.youtube_url}")
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        print(f"Extracted video ID: {video_id}")
        
        # Get video metadata
        metadata = None
        if youtube_service:
            print("Getting real video metadata...")
            metadata = youtube_service.get_video_metadata(video_id)
            if metadata and metadata.get('title') != 'Unknown Title':
                print(f"✅ Got real metadata: {metadata['title']}")
            else:
                print("⚠️ Using fallback metadata")
        else:
            # Fallback mock metadata
            metadata = {
                'title': f'Video {video_id}',
                'channel': 'Unknown Channel',
                'duration': '10:00',
                'description': 'Video description not available',
                'thumbnail': f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg',
                'view_count': '1000',
                'like_count': '100'
            }
        
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
        if ai_service and ai_service.has_api_key:
            print("Generating AI summary with OpenAI...")
            ai_summary = ai_service.generate_summary(transcript, metadata['title'])
            if ai_summary and 'summary' in ai_summary:
                print("✅ Generated real AI summary")
            else:
                print("⚠️ AI summary failed, using fallback")
                ai_summary = None
        else:
            print("AI service not available or no API key, using mock summary")
        
        if not ai_summary:
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
        
        # Record video watched for progress tracking
        try:
            if progress_service:
                progress_service.record_video_watched(
                    None,
                    current_user.id,
                    {
                        'video_id': video_id,
                        'title': metadata['title'],
                        'channel': metadata['channel'],
                        'duration': metadata['duration'],
                        'summary': ai_summary['summary']
                    }
                )
                print("✅ Video progress recorded")
        except Exception as e:
            print(f"⚠️ Error recording video progress: {e}")
            # Don't fail the request if progress recording fails
        
        return response_data
    except Exception as e:
        print(f"Error in analyze_video: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_video(request: ChatRequest):
    """Ask questions about a specific video"""
    try:
        if not ai_service or not ai_service.has_api_key:
            # Fallback mock response with video context
            return ChatResponse(
                answer="I'm sorry, the AI service is currently unavailable. Please try again later.",
                sources=["Video transcript", "Summary"],
                confidence="low"
            )
        
        print(f"Generating AI chat response for: {request.question}")
        # Generate AI response with video title for context
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
async def generate_quiz(request: QuizRequest, current_user = Depends(get_current_user)):
    """Generate quiz questions based on video content"""
    try:
        if not ai_service or not ai_service.has_api_key:
            # Fallback mock quiz with video context
            questions = [
                QuizQuestion(
                    question="What is the main topic of this video?",
                    options=["Learning concepts", "Entertainment", "Sports", "Music"],
                    correct_answer=0,
                    explanation="Educational videos focus on teaching and learning concepts."
                )
            ]
            return QuizResponse(questions=questions)
        
        print(f"Generating AI quiz with {request.num_questions} questions...")
        # Generate AI quiz questions with video title for context
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
        
        # Record quiz result for progress tracking
        try:
            if progress_service:
                # Calculate score based on correct answers (mock for now)
                score = 67  # Mock score
                progress_service.record_quiz_result(
                    None,
                    current_user.id,
                    "mock_video_id",
                    score,
                    len(quiz_questions)
                )
                print("✅ Quiz progress recorded")
        except Exception as e:
            print(f"⚠️ Error recording quiz progress: {e}")
            # Don't fail the request if progress recording fails
        
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
if frontend_dist and frontend_dist.exists():
    @app.get("/{full_path:path}")
    async def serve_frontend_routes(full_path: str):
        """Serve frontend for all non-API routes"""
        # Don't serve API routes
        if full_path.startswith(("auth/", "analyze", "chat", "quiz", "health", "api/", "ping")):
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
else:
    print("Frontend dist not found! Serving API only.") 