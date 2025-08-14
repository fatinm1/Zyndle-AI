from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration - PostgreSQL for production, SQLite for development
def get_database_url():
    """Get database URL with fallback to SQLite for development"""
    # Check for Railway PostgreSQL URL first
    railway_db_url = os.getenv('DATABASE_URL')
    if railway_db_url and railway_db_url.startswith('postgresql://'):
        print("✅ Using Railway PostgreSQL database")
        return railway_db_url
    
    # Check for custom PostgreSQL connection
    pg_host = os.getenv('POSTGRES_HOST', 'localhost')
    pg_port = os.getenv('POSTGRES_PORT', '5432')
    pg_user = os.getenv('POSTGRES_USER', 'postgres')
    pg_password = os.getenv('POSTGRES_PASSWORD', '')
    pg_database = os.getenv('POSTGRES_DB', 'zyndle_ai')
    
    if all([pg_host, pg_user, pg_database]):
        pg_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
        print("✅ Using custom PostgreSQL database")
        return pg_url
    
    # Fallback to SQLite for development
    sqlite_url = 'sqlite:///./zyndle_ai.db'
    print("⚠️ Using SQLite database (development mode)")
    return sqlite_url

# Get database URL
DATABASE_URL = get_database_url()

# Create engine with PostgreSQL-specific settings
if DATABASE_URL.startswith('postgresql://'):
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False  # Set to True for SQL debugging
    )
    print("🔧 PostgreSQL engine configured with connection pooling")
else:
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )
    print("🔧 SQLite engine configured")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    video_analyses = relationship("VideoAnalysis", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")
    quiz_sessions = relationship("QuizSession", back_populates="user")
    notes = relationship("Note", back_populates="user")
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

class VideoAnalysis(Base):
    __tablename__ = "video_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, unique=True, index=True)
    title = Column(String)
    channel = Column(String)
    duration = Column(String)
    summary = Column(Text)
    transcript = Column(Text)
    chapters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="video_analyses")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, index=True)
    question = Column(Text)
    answer = Column(Text)
    sources = Column(JSON)
    confidence = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="chat_sessions")

class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, index=True)
    questions = Column(JSON)
    user_answers = Column(JSON)
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="quiz_sessions")

class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="notes")

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!") 