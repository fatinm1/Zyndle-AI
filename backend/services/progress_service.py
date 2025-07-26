import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from sqlalchemy.orm import Session
from models.database import User, VideoAnalysis, QuizSession

class ProgressService:
    def __init__(self):
        # In-memory storage for user progress (in production, this would be a database)
        self.user_progress = {}
        self.video_history = {}
        self.quiz_history = {}
        print("✅ ProgressService initialized with in-memory storage")
    
    def get_user_progress(self, db: Session, user_id: int) -> Dict:
        """Get comprehensive user progress statistics"""
        try:
            # Get user's progress data
            user_data = self.user_progress.get(user_id, {
                'videos_watched': [],
                'quizzes_taken': [],
                'total_time': 0
            })
            
            videos_watched = user_data.get('videos_watched', [])
            quizzes_taken = user_data.get('quizzes_taken', [])
            
            # Calculate statistics
            total_videos = len(videos_watched)
            total_time = user_data.get('total_time', 0)
            
            # Get recent videos (last 5)
            recent_videos = videos_watched[-5:] if videos_watched else []
            
            # Calculate quiz statistics
            total_quizzes = len(quizzes_taken)
            average_score = 0
            if quizzes_taken:
                total_score = sum(quiz.get('score', 0) for quiz in quizzes_taken)
                average_score = total_score / total_quizzes
            
            # Determine favorite subjects based on video titles
            subjects = []
            for video in videos_watched:
                title = video.get('title', '').lower()
                if 'physics' in title or 'nuclear' in title:
                    subjects.append('Physics')
                elif 'chemistry' in title:
                    subjects.append('Chemistry')
                elif 'math' in title or 'mathematics' in title:
                    subjects.append('Mathematics')
                elif 'biology' in title:
                    subjects.append('Biology')
                elif 'computer' in title or 'programming' in title:
                    subjects.append('Computer Science')
            
            # Get unique subjects
            favorite_subjects = list(set(subjects))[:3]  # Top 3 subjects
            if not favorite_subjects:
                favorite_subjects = ['General Education']
            
            # Generate insights based on actual activity
            insights = []
            if total_videos > 0:
                insights.append(f"You've watched {total_videos} educational videos!")
            if total_quizzes > 0:
                insights.append(f"Great job taking {total_quizzes} quizzes with {average_score:.0f}% average score!")
            if total_time > 0:
                hours = total_time // 60
                minutes = total_time % 60
                insights.append(f"You've spent {hours}h {minutes}m learning!")
            
            if not insights:
                insights = ["Start your learning journey by analyzing your first video!"]
            
            return {
                "total_videos_watched": total_videos,
                "total_time_watched": f"{total_time // 60}:{total_time % 60:02d}",
                "favorite_subjects": favorite_subjects,
                "recent_videos": recent_videos,
                "quiz_stats": {
                    "total_quizzes_taken": total_quizzes,
                    "average_score": round(average_score),
                    "best_subject": favorite_subjects[0] if favorite_subjects else "General"
                },
                "learning_insights": insights
            }
            
        except Exception as e:
            print(f"Error getting user progress: {e}")
            return self._get_mock_progress()
    
    def get_learning_insights(self, db: Session, user_id: int) -> Dict:
        """Get personalized learning insights and recommendations"""
        try:
            user_data = self.user_progress.get(user_id, {
                'videos_watched': [],
                'quizzes_taken': []
            })
            
            videos_watched = user_data.get('videos_watched', [])
            quizzes_taken = user_data.get('quizzes_taken', [])
            
            insights = []
            recommendations = []
            
            if not videos_watched:
                insights.append("Welcome to Zyndle AI! Start by analyzing your first educational video.")
                recommendations = [
                    "Try analyzing a YouTube video in your favorite subject",
                    "Explore different topics to discover your learning preferences",
                    "Take quizzes after watching videos to test your understanding"
                ]
            else:
                total_videos = len(videos_watched)
                total_quizzes = len(quizzes_taken)
                
                insights.append(f"You've watched {total_videos} educational videos!")
                
                if total_quizzes > 0:
                    avg_score = sum(quiz.get('score', 0) for quiz in quizzes_taken) / total_quizzes
                    insights.append(f"Your quiz performance shows {avg_score:.0f}% average understanding!")
                    
                    if avg_score >= 80:
                        insights.append("Excellent comprehension! You're ready for more advanced topics.")
                        recommendations.append("Try more challenging videos in your favorite subjects")
                    elif avg_score >= 60:
                        insights.append("Good progress! Keep practicing to improve your understanding.")
                        recommendations.append("Review concepts you find challenging")
                    else:
                        insights.append("Keep practicing! Review the basics before moving to advanced topics.")
                        recommendations.append("Focus on fundamental concepts first")
                else:
                    insights.append("Try taking quizzes to test your understanding!")
                    recommendations.append("Take quizzes after watching videos")
                
                # Subject-specific recommendations
                subjects = set()
                for video in videos_watched:
                    title = video.get('title', '').lower()
                    if 'physics' in title:
                        subjects.add('Physics')
                    elif 'chemistry' in title:
                        subjects.add('Chemistry')
                    elif 'math' in title:
                        subjects.add('Mathematics')
                
                if subjects:
                    insights.append(f"You're exploring {', '.join(subjects)} - great subject diversity!")
                    recommendations.append(f"Continue exploring {list(subjects)[0]} topics")
                
                recommendations.extend([
                    "Set learning goals for consistent progress",
                    "Take notes while watching videos",
                    "Review previous videos to reinforce learning"
                ])
            
            return {
                "insights": insights,
                "recommendations": recommendations
            }
            
        except Exception as e:
            print(f"Error getting learning insights: {e}")
            return {
                "insights": ["Start your learning journey!"],
                "recommendations": ["Analyze your first video", "Take quizzes to test understanding"]
            }
    
    def record_video_watched(self, db: Session, user_id: int, video_data: Dict) -> bool:
        """Record that a user watched a video"""
        try:
            if user_id not in self.user_progress:
                self.user_progress[user_id] = {
                    'videos_watched': [],
                    'quizzes_taken': [],
                    'total_time': 0
                }
            
            # Parse duration to get minutes
            duration_str = video_data.get('duration', '0:00')
            duration_parts = duration_str.split(':')
            if len(duration_parts) == 2:
                minutes = int(duration_parts[0]) + int(duration_parts[1]) / 60
            elif len(duration_parts) == 3:
                minutes = int(duration_parts[0]) * 60 + int(duration_parts[1]) + int(duration_parts[2]) / 60
            else:
                minutes = 10  # Default 10 minutes
            
            # Create video record
            video_record = {
                'video_id': video_data.get('video_id', 'unknown'),
                'title': video_data.get('title', 'Unknown Video'),
                'channel': video_data.get('channel', 'Unknown Channel'),
                'duration': video_data.get('duration', '0:00'),
                'watched_at': datetime.now().isoformat(),
                'summary': video_data.get('summary', '')
            }
            
            # Add to user's video history
            self.user_progress[user_id]['videos_watched'].append(video_record)
            self.user_progress[user_id]['total_time'] += int(minutes)
            
            print(f"✅ Recorded video: {video_data.get('title', 'Unknown')} for user {user_id}")
            return True
            
        except Exception as e:
            print(f"Error recording video watched: {e}")
            return False
    
    def record_quiz_result(self, db: Session, user_id: int, video_id: str, score: int, total_questions: int) -> bool:
        """Record quiz results"""
        try:
            if user_id not in self.user_progress:
                self.user_progress[user_id] = {
                    'videos_watched': [],
                    'quizzes_taken': [],
                    'total_time': 0
                }
            
            # Create quiz record
            quiz_record = {
                'video_id': video_id,
                'score': score,
                'total_questions': total_questions,
                'percentage': round((score / total_questions) * 100),
                'taken_at': datetime.now().isoformat()
            }
            
            # Add to user's quiz history
            self.user_progress[user_id]['quizzes_taken'].append(quiz_record)
            
            print(f"✅ Recorded quiz: {score}/{total_questions} ({quiz_record['percentage']}%) for user {user_id}")
            return True
            
        except Exception as e:
            print(f"Error recording quiz result: {e}")
            return False
    
    def _get_mock_progress(self) -> Dict:
        """Return mock progress data for development"""
        return {
            "total_videos_watched": 0,
            "total_time_watched": "0:00",
            "favorite_subjects": ["Start Learning"],
            "recent_videos": [],
            "quiz_stats": {
                "total_quizzes_taken": 0,
                "average_score": 0,
                "best_subject": "None"
            },
            "learning_insights": ["Welcome to Zyndle AI! Start by analyzing your first video."]
        } 