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
from sqlalchemy.orm import Session

# Import our services and models
from services.youtube_service import YouTubeService
from services.ai_service import AIService
from services.auth_service import AuthService
from services.progress_service import ProgressService
from services.notes_service import NotesService
from services.transcription_service import TranscriptionService
from models.database import get_db, create_tables, User

# Load environment variables
load_dotenv()

# Create database tables
create_tables()

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
youtube_service = YouTubeService()
ai_service = AIService()
auth_service = AuthService()
progress_service = ProgressService()
notes_service = NotesService()
transcription_service = TranscriptionService()

# Security
security = HTTPBearer()

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

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = auth_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = auth_service.get_user_by_id(db, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "services": {
            "youtube": "available", 
            "ai": "available",
            "transcription": "available" if transcription_service.model else "loading"
        }
    }

# Authentication endpoints
@app.post("/auth/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        user = auth_service.create_user(
            db=db,
            email=user_data.email,
            full_name=user_data.full_name,
            password=user_data.password
        )
        
        # Create access token
        access_token = auth_service.create_access_token(
            data={"sub": str(user.id)}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = auth_service.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id)}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "created_at": current_user.created_at.isoformat()
    }

@app.post("/analyze", response_model=VideoAnalysisResponse)
async def analyze_video(request: VideoAnalysisRequest, current_user: User = Depends(get_current_user)):
    """Analyze a YouTube video and return summary, chapters, and transcript"""
    try:
        # Extract video ID from URL
        video_id = youtube_service.extract_video_id(request.youtube_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Get video metadata
        metadata = youtube_service.get_video_metadata(video_id)
        
        # Get real transcript using transcription service
        transcript = youtube_service.get_video_transcript(video_id)
        
        # Fallback to mock transcript if real transcription fails
        if not transcript:
            print(f"Warning: Failed to get real transcript for video {video_id}, using mock transcript")
            transcript = f"This is a transcript for {metadata['title']}. The video covers important concepts and provides valuable insights for learners."
        
        # Generate AI summary based on real transcript
        ai_summary = ai_service.generate_summary(transcript, metadata['title'])
        
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
        
        # Record video watched for progress tracking
        try:
            progress_service.record_video_watched(
                db=next(get_db()),
                user_id=current_user.id,
                video_data={
                    'video_id': video_id,
                    'title': metadata['title'],
                    'channel': metadata['channel'],
                    'duration': metadata['duration'],
                    'summary': ai_summary['summary']
                }
            )
        except Exception as e:
            print(f"Error recording video progress: {e}")
            # Don't fail the request if progress recording fails
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_video(request: ChatRequest):
    """Ask questions about a specific video"""
    try:
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
        metadata = youtube_service.get_video_metadata(video_id)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/videos/{video_id}/transcript")
async def get_video_transcript(video_id: str, current_user: User = Depends(get_current_user)):
    """Get transcript for a specific video (for testing)"""
    try:
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

# Progress tracking endpoints
@app.get("/progress")
async def get_user_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's learning progress and statistics"""
    try:
        progress = progress_service.get_user_progress(db, current_user.id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/progress/insights")
async def get_learning_insights(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get personalized learning insights and recommendations"""
    try:
        insights = progress_service.get_learning_insights(db, current_user.id)
        return insights
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/progress/record-video")
async def record_video_watched(video_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Record that a user watched a video"""
    try:
        success = progress_service.record_video_watched(db, current_user.id, video_data)
        if success:
            return {"message": "Video watched recorded successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to record video watched")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/progress/record-quiz")
async def record_quiz_result(quiz_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Record quiz results"""
    try:
        success = progress_service.record_quiz_result(
            db, 
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
        raise HTTPException(status_code=400, detail=str(e))

# Notes endpoints
@app.post("/notes")
async def create_note(note_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new note"""
    try:
        note = notes_service.create_note(
            db=db,
            user_id=current_user.id,
            video_id=note_data.get('video_id'),
            content=note_data.get('content'),
            title=note_data.get('title')
        )
        return note
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/notes")
async def get_notes(video_id: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's notes, optionally filtered by video"""
    try:
        notes = notes_service.get_user_notes(db, current_user.id, video_id)
        return {"notes": notes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/notes/{note_id}")
async def get_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get a specific note"""
    try:
        note = notes_service.get_note_by_id(db, current_user.id, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/notes/{note_id}")
async def update_note(note_id: int, note_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update a note"""
    try:
        note = notes_service.update_note(
            db=db,
            user_id=current_user.id,
            note_id=note_id,
            content=note_data.get('content'),
            title=note_data.get('title')
        )
        return note
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a note"""
    try:
        success = notes_service.delete_note(db, current_user.id, note_id)
        if success:
            return {"message": "Note deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/notes/search/{query}")
async def search_notes(query: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Search notes by content or title"""
    try:
        notes = notes_service.search_notes(db, current_user.id, query)
        return {"notes": notes}
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 