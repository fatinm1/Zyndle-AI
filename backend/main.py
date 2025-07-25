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
frontend_dist = Path("../frontend/dist")
if frontend_dist.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dist)), name="static")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend index.html"""
        index_path = frontend_dist / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        else:
            return {"message": "Zyndle AI API is running!"}
else:
    @app.get("/")
    async def root():
        return {"message": "Zyndle AI API is running!"}

# Initialize services
youtube_service = YouTubeService()
ai_service = AIService()
auth_service = AuthService()

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
    return {"status": "healthy", "services": {"youtube": "available", "ai": "available"}}

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
        
        # Generate mock transcript (in production, you'd use Whisper or similar)
        mock_transcript = f"This is a transcript for {metadata['title']}. The video covers important concepts and provides valuable insights for learners."
        
        # Generate AI summary
        ai_summary = ai_service.generate_summary(mock_transcript, metadata['title'])
        
        return {
            "title": metadata['title'],
            "channel": metadata['channel'],
            "duration": metadata['duration'],
            "summary": ai_summary['summary'],
            "chapters": ai_summary['chapters'],
            "transcript": mock_transcript,
            "thumbnail": metadata.get('thumbnail'),
            "view_count": metadata.get('view_count'),
            "like_count": metadata.get('like_count')
        }
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 