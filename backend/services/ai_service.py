import os
from typing import List, Dict, Optional
from openai import OpenAI
import json

class AIService:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            try:
                self.client = OpenAI(api_key=api_key)
                self.model = "gpt-3.5-turbo"  # Can be upgraded to gpt-4 for better results
                self.has_api_key = True
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.client = None
                self.has_api_key = False
        else:
            print("Warning: OPENAI_API_KEY not set. Using mock responses.")
            self.client = None
            self.has_api_key = False
    
    def generate_summary(self, transcript: str, title: str) -> Dict:
        """Generate a comprehensive summary of the video content"""
        try:
            if not self.client:
                return self._get_mock_summary(title)
            
            if not self.client.api_key:
                return self._get_mock_summary(title)
            
            prompt = f"""
            Please analyze this video transcript and provide:
            1. A comprehensive summary (2-3 paragraphs)
            2. Key points and takeaways
            3. Suggested chapters with timestamps (if possible)
            
            Video Title: {title}
            Transcript: {transcript[:3000]}...
            
            Format your response as JSON:
            {{
                "summary": "comprehensive summary here",
                "key_points": ["point1", "point2", "point3"],
                "chapters": [
                    {{"title": "Chapter 1", "start": 0, "end": 180, "description": "..."}},
                    {{"title": "Chapter 2", "start": 180, "end": 480, "description": "..."}}
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content analyzer. Provide clear, structured summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._get_mock_summary(title)
    
    def chat_with_video(self, question: str, transcript: str, summary: str) -> Dict:
        """Generate a contextual response based on the video content"""
        try:
            if not self.client:
                return self._get_mock_chat_response(question)
            
            if not self.client.api_key:
                return self._get_mock_chat_response(question)
            
            prompt = f"""
            Based on this video content, answer the user's question.
            
            Video Summary: {summary}
            Video Transcript: {transcript[:2000]}...
            
            User Question: {question}
            
            Provide a helpful, accurate response based on the video content. If the question cannot be answered from the video, say so politely.
            
            Format your response as JSON:
            {{
                "answer": "your detailed answer here",
                "sources": ["relevant part of transcript or summary"],
                "confidence": "high/medium/low"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI tutor. Answer questions based on the provided video content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            print(f"Error generating chat response: {e}")
            return self._get_mock_chat_response(question)
    
    def generate_quiz(self, transcript: str, summary: str, num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions based on the video content"""
        try:
            if not self.client:
                return self._get_mock_quiz_questions(num_questions)
            
            if not self.client.api_key:
                return self._get_mock_quiz_questions(num_questions)
            
            prompt = f"""
            Create {num_questions} multiple choice questions based on this video content.
            
            Video Summary: {summary}
            Video Transcript: {transcript[:2000]}...
            
            Create questions that test understanding of key concepts. Include:
            - 4 options per question
            - Correct answer (0-3 index)
            - Brief explanation
            
            Format as JSON array:
            [
                {{
                    "question": "What is the main topic?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 0,
                    "explanation": "Explanation of why this is correct"
                }}
            ]
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert quiz creator. Create educational, engaging questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self._get_mock_quiz_questions(num_questions)
    
    def _get_mock_summary(self, title: str) -> Dict:
        """Return mock summary for development"""
        return {
            "summary": f"This video covers important concepts related to {title}. The content is well-structured and provides valuable insights for learners.",
            "key_points": [
                "Introduction to core concepts",
                "Practical applications",
                "Best practices and tips",
                "Common pitfalls to avoid"
            ],
            "chapters": [
                {"title": "Introduction", "start": 0, "end": 180, "description": "Overview and context"},
                {"title": "Main Concepts", "start": 180, "end": 480, "description": "Core principles explained"},
                {"title": "Examples", "start": 480, "end": 780, "description": "Practical demonstrations"},
                {"title": "Conclusion", "start": 780, "end": 930, "description": "Summary and next steps"}
            ]
        }
    
    def _get_mock_chat_response(self, question: str) -> Dict:
        """Return mock chat response for development"""
        mock_answers = {
            "What is the main topic?": "The main topic is artificial intelligence and machine learning concepts.",
            "Explain the first chapter": "The first chapter introduces the fundamental concepts and provides context for the rest of the video.",
            "What are the key takeaways?": "The key takeaways include understanding basic principles, practical applications, and best practices."
        }
        
        answer = mock_answers.get(question, "I'm sorry, I don't have enough context to answer that specific question.")
        
        return {
            "answer": answer,
            "sources": ["Video transcript", "Summary"],
            "confidence": "medium"
        }
    
    def _get_mock_quiz_questions(self, num_questions: int) -> List[Dict]:
        """Return mock quiz questions for development"""
        questions = [
            {
                "question": "What is the main topic of this video?",
                "options": ["Machine Learning", "Web Development", "Cooking", "Music"],
                "correct_answer": 0,
                "explanation": "The video primarily focuses on machine learning concepts."
            },
            {
                "question": "Which of the following is NOT a type of machine learning?",
                "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Quantum Computing"],
                "correct_answer": 3,
                "explanation": "Quantum computing is a computing paradigm, not a type of machine learning."
            },
            {
                "question": "What is the purpose of training data in machine learning?",
                "options": ["To test the model", "To teach the model", "To deploy the model", "To visualize results"],
                "correct_answer": 1,
                "explanation": "Training data is used to teach the model patterns and relationships."
            }
        ]
        
        return questions[:num_questions] 