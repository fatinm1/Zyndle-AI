from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from models.database import User, Note
from datetime import datetime

class NotesService:
    def __init__(self):
        pass
    
    def create_note(self, db: Session, user_id: int, video_id: str, content: str, title: str = None) -> Dict:
        """Create a new note for a user"""
        try:
            note = Note(
                user_id=user_id,
                video_id=video_id,
                title=title or f"Note on {video_id}",
                content=content,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(note)
            db.commit()
            db.refresh(note)
            
            return {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "video_id": note.video_id,
                "created_at": note.created_at.isoformat(),
                "updated_at": note.updated_at.isoformat()
            }
        except Exception as e:
            print(f"Error creating note: {e}")
            db.rollback()
            raise e
    
    def get_user_notes(self, db: Session, user_id: int, video_id: str = None) -> List[Dict]:
        """Get all notes for a user, optionally filtered by video"""
        try:
            query = db.query(Note).filter(Note.user_id == user_id)
            
            if video_id:
                query = query.filter(Note.video_id == video_id)
            
            notes = query.order_by(Note.updated_at.desc()).all()
            
            return [
                {
                    "id": note.id,
                    "title": note.title,
                    "content": note.content,
                    "video_id": note.video_id,
                    "created_at": note.created_at.isoformat(),
                    "updated_at": note.updated_at.isoformat()
                }
                for note in notes
            ]
        except Exception as e:
            print(f"Error getting user notes: {e}")
            return []
    
    def update_note(self, db: Session, user_id: int, note_id: int, content: str, title: str = None) -> Dict:
        """Update an existing note"""
        try:
            note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
            
            if not note:
                raise ValueError("Note not found or access denied")
            
            note.content = content
            if title:
                note.title = title
            note.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(note)
            
            return {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "video_id": note.video_id,
                "created_at": note.created_at.isoformat(),
                "updated_at": note.updated_at.isoformat()
            }
        except Exception as e:
            print(f"Error updating note: {e}")
            db.rollback()
            raise e
    
    def delete_note(self, db: Session, user_id: int, note_id: int) -> bool:
        """Delete a note"""
        try:
            note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
            
            if not note:
                raise ValueError("Note not found or access denied")
            
            db.delete(note)
            db.commit()
            return True
        except Exception as e:
            print(f"Error deleting note: {e}")
            db.rollback()
            return False
    
    def search_notes(self, db: Session, user_id: int, query: str) -> List[Dict]:
        """Search notes by content or title"""
        try:
            notes = db.query(Note).filter(
                Note.user_id == user_id,
                (Note.content.ilike(f"%{query}%") | Note.title.ilike(f"%{query}%"))
            ).order_by(Note.updated_at.desc()).all()
            
            return [
                {
                    "id": note.id,
                    "title": note.title,
                    "content": note.content,
                    "video_id": note.video_id,
                    "created_at": note.created_at.isoformat(),
                    "updated_at": note.updated_at.isoformat()
                }
                for note in notes
            ]
        except Exception as e:
            print(f"Error searching notes: {e}")
            return []
    
    def get_note_by_id(self, db: Session, user_id: int, note_id: int) -> Optional[Dict]:
        """Get a specific note by ID"""
        try:
            note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
            
            if not note:
                return None
            
            return {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "video_id": note.video_id,
                "created_at": note.created_at.isoformat(),
                "updated_at": note.updated_at.isoformat()
            }
        except Exception as e:
            print(f"Error getting note by ID: {e}")
            return None 