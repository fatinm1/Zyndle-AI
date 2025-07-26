from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from models.database import User, VideoAnalysis, QuizSession
from datetime import datetime, timedelta

class ProgressService:
    def __init__(self):
        pass
    
    def get_user_progress(self, db: Session, user_id: int) -> Dict:
        """Get comprehensive user progress statistics"""
        try:
            # Get user's video analysis history
            video_analyses = db.query(VideoAnalysis).filter(VideoAnalysis.user_id == user_id).all()
            
            # Get user's quiz history
            quiz_sessions = db.query(QuizSession).filter(QuizSession.user_id == user_id).all()
            
            # Calculate statistics
            total_videos_watched = len(video_analyses)
            total_quizzes_taken = len(quiz_sessions)
            
            # Calculate average quiz score
            total_score = sum(quiz.score for quiz in quiz_sessions if quiz.score is not None)
            average_score = total_score / total_quizzes_taken if total_quizzes_taken > 0 else 0
            
            # Get recent activity (last 7 days)
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_videos = [v for v in video_analyses if v.created_at >= week_ago]
            recent_quizzes = [q for q in quiz_sessions if q.created_at >= week_ago]
            
            # Get learning streak (consecutive days with activity)
            streak = self._calculate_learning_streak(video_analyses, quiz_sessions)
            
            return {
                "total_videos_watched": total_videos_watched,
                "total_quizzes_taken": total_quizzes_taken,
                "average_quiz_score": round(average_score, 1),
                "recent_videos": len(recent_videos),
                "recent_quizzes": len(recent_quizzes),
                "learning_streak": streak,
                "total_learning_time": self._calculate_total_time(video_analyses),
                "favorite_topics": self._get_favorite_topics(video_analyses),
                "recent_activity": self._get_recent_activity(video_analyses, quiz_sessions)
            }
        except Exception as e:
            print(f"Error getting user progress: {e}")
            return self._get_mock_progress()
    
    def record_video_watched(self, db: Session, user_id: int, video_data: Dict) -> bool:
        """Record that a user watched a video"""
        try:
            video_analysis = VideoAnalysis(
                user_id=user_id,
                video_id=video_data.get('video_id'),
                title=video_data.get('title'),
                channel=video_data.get('channel'),
                duration=video_data.get('duration'),
                summary=video_data.get('summary'),
                created_at=datetime.utcnow()
            )
            db.add(video_analysis)
            db.commit()
            return True
        except Exception as e:
            print(f"Error recording video watched: {e}")
            db.rollback()
            return False
    
    def record_quiz_result(self, db: Session, user_id: int, video_id: str, score: int, total_questions: int) -> bool:
        """Record quiz results"""
        try:
            quiz_session = QuizSession(
                user_id=user_id,
                video_id=video_id,
                score=score,
                total_questions=total_questions,
                created_at=datetime.utcnow()
            )
            db.add(quiz_session)
            db.commit()
            return True
        except Exception as e:
            print(f"Error recording quiz result: {e}")
            db.rollback()
            return False
    
    def get_learning_insights(self, db: Session, user_id: int) -> Dict:
        """Get personalized learning insights"""
        try:
            video_analyses = db.query(VideoAnalysis).filter(VideoAnalysis.user_id == user_id).all()
            quiz_sessions = db.query(QuizSession).filter(QuizSession.user_id == user_id).all()
            
            # Analyze learning patterns
            topics = self._get_favorite_topics(video_analyses)
            weak_areas = self._identify_weak_areas(quiz_sessions)
            recommendations = self._generate_recommendations(video_analyses, quiz_sessions)
            
            return {
                "favorite_topics": topics,
                "weak_areas": weak_areas,
                "recommendations": recommendations,
                "learning_style": self._analyze_learning_style(video_analyses, quiz_sessions)
            }
        except Exception as e:
            print(f"Error getting learning insights: {e}")
            return self._get_mock_insights()
    
    def _calculate_learning_streak(self, video_analyses: List, quiz_sessions: List) -> int:
        """Calculate consecutive days with learning activity"""
        try:
            # Combine all activity dates
            activity_dates = set()
            for video in video_analyses:
                activity_dates.add(video.created_at.date())
            for quiz in quiz_sessions:
                activity_dates.add(quiz.created_at.date())
            
            if not activity_dates:
                return 0
            
            # Sort dates and find longest streak
            sorted_dates = sorted(activity_dates, reverse=True)
            current_streak = 0
            current_date = datetime.utcnow().date()
            
            for date in sorted_dates:
                if date == current_date - timedelta(days=current_streak):
                    current_streak += 1
                else:
                    break
            
            return current_streak
        except Exception as e:
            print(f"Error calculating learning streak: {e}")
            return 0
    
    def _calculate_total_time(self, video_analyses: List) -> int:
        """Calculate total learning time in minutes"""
        total_minutes = 0
        for video in video_analyses:
            if video.duration:
                # Parse duration (format: "15:30" or "1:23:45")
                parts = video.duration.split(':')
                if len(parts) == 2:
                    total_minutes += int(parts[0]) + int(parts[1]) / 60
                elif len(parts) == 3:
                    total_minutes += int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
        return round(total_minutes)
    
    def _get_favorite_topics(self, video_analyses: List) -> List[str]:
        """Extract favorite topics from video titles"""
        topics = []
        for video in video_analyses:
            if video.title:
                # Simple topic extraction (can be improved with NLP)
                title_lower = video.title.lower()
                if 'machine learning' in title_lower or 'ml' in title_lower:
                    topics.append('Machine Learning')
                elif 'python' in title_lower:
                    topics.append('Python Programming')
                elif 'javascript' in title_lower or 'js' in title_lower:
                    topics.append('JavaScript')
                elif 'react' in title_lower:
                    topics.append('React')
                elif 'ai' in title_lower or 'artificial intelligence' in title_lower:
                    topics.append('Artificial Intelligence')
                else:
                    topics.append('General Learning')
        
        # Return top 3 most common topics
        from collections import Counter
        topic_counts = Counter(topics)
        return [topic for topic, count in topic_counts.most_common(3)]
    
    def _identify_weak_areas(self, quiz_sessions: List) -> List[str]:
        """Identify areas where user struggles based on quiz scores"""
        weak_areas = []
        low_score_quizzes = [q for q in quiz_sessions if q.score and q.score < 70]
        
        if len(low_score_quizzes) > 0:
            weak_areas.append("Quiz Performance")
        
        if len(quiz_sessions) < 5:
            weak_areas.append("Quiz Participation")
        
        return weak_areas
    
    def _generate_recommendations(self, video_analyses: List, quiz_sessions: List) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        if len(video_analyses) < 3:
            recommendations.append("Try watching more educational videos to build a strong foundation")
        
        if len(quiz_sessions) < 2:
            recommendations.append("Take more quizzes to test your understanding and track progress")
        
        low_scores = [q for q in quiz_sessions if q.score and q.score < 70]
        if len(low_scores) > 0:
            recommendations.append("Focus on reviewing topics where you scored lower on quizzes")
        
        if len(video_analyses) > 10:
            recommendations.append("Great progress! Consider exploring advanced topics in your favorite subjects")
        
        return recommendations
    
    def _analyze_learning_style(self, video_analyses: List, quiz_sessions: List) -> str:
        """Analyze user's learning style based on activity patterns"""
        if len(quiz_sessions) > len(video_analyses) * 0.8:
            return "Quiz-focused learner"
        elif len(video_analyses) > 10:
            return "Visual learner"
        else:
            return "Balanced learner"
    
    def _get_recent_activity(self, video_analyses: List, quiz_sessions: List) -> List[Dict]:
        """Get recent learning activity"""
        recent_activity = []
        
        # Combine and sort recent activities
        for video in video_analyses[-5:]:  # Last 5 videos
            recent_activity.append({
                "type": "video_watched",
                "title": video.title,
                "date": video.created_at.isoformat(),
                "description": f"Watched {video.title}"
            })
        
        for quiz in quiz_sessions[-5:]:  # Last 5 quizzes
            recent_activity.append({
                "type": "quiz_taken",
                "score": quiz.score,
                "date": quiz.created_at.isoformat(),
                "description": f"Quiz score: {quiz.score}%"
            })
        
        # Sort by date and return recent 10 activities
        recent_activity.sort(key=lambda x: x["date"], reverse=True)
        return recent_activity[:10]
    
    def _get_mock_progress(self) -> Dict:
        """Return mock progress data for development"""
        return {
            "total_videos_watched": 5,
            "total_quizzes_taken": 3,
            "average_quiz_score": 85.0,
            "recent_videos": 2,
            "recent_quizzes": 1,
            "learning_streak": 3,
            "total_learning_time": 120,
            "favorite_topics": ["Machine Learning", "Python Programming"],
            "recent_activity": [
                {"type": "video_watched", "title": "Introduction to ML", "date": "2024-01-15T10:00:00Z"},
                {"type": "quiz_taken", "score": 90, "date": "2024-01-14T15:30:00Z"}
            ]
        }
    
    def _get_mock_insights(self) -> Dict:
        """Return mock insights for development"""
        return {
            "favorite_topics": ["Machine Learning", "Python Programming"],
            "weak_areas": ["Advanced Concepts"],
            "recommendations": [
                "Try watching more educational videos",
                "Take more quizzes to test understanding"
            ],
            "learning_style": "Visual learner"
        } 