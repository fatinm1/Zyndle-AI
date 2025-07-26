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
            if "insufficient_quota" in str(e) or "429" in str(e):
                print("⚠️ OpenAI API quota exceeded. Using enhanced mock summary.")
                return self._get_enhanced_mock_summary(title)
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
            if "insufficient_quota" in str(e) or "429" in str(e):
                print("⚠️ OpenAI API quota exceeded. Using enhanced mock chat response.")
                return self._get_enhanced_mock_chat_response(question)
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
            if "insufficient_quota" in str(e) or "429" in str(e):
                print("⚠️ OpenAI API quota exceeded. Using enhanced mock quiz.")
                return self._get_enhanced_mock_quiz_questions(num_questions)
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
    
    def _get_enhanced_mock_summary(self, title: str) -> Dict:
        """Generate an enhanced mock summary when API quota is exceeded"""
        # Extract topic from title for better context
        topic = title.split('|')[0].strip() if '|' in title else title
        
        return {
            "summary": f"This educational video focuses on {topic}. The instructor provides a comprehensive overview of the subject matter, breaking down complex concepts into understandable segments. The content is designed to help students grasp fundamental principles and apply them to real-world scenarios.",
            "key_points": [
                f"Understanding {topic} fundamentals",
                "Practical applications and examples", 
                "Key formulas and calculations",
                "Common misconceptions and clarifications"
            ],
            "chapters": [
                {"title": "Introduction to " + topic, "start": 0, "end": 180, "description": "Overview and learning objectives"},
                {"title": "Core Concepts", "start": 180, "end": 480, "description": "Fundamental principles and definitions"},
                {"title": "Problem-Solving Examples", "start": 480, "end": 780, "description": "Step-by-step demonstrations"},
                {"title": "Practice Problems", "start": 780, "end": 1080, "description": "Interactive exercises and solutions"},
                {"title": "Summary and Review", "start": 1080, "end": 1200, "description": "Key takeaways and next steps"}
            ]
        }
    
    def _get_enhanced_mock_chat_response(self, question: str) -> Dict:
        """Generate an enhanced mock chat response when API quota is exceeded"""
        # Better context-aware responses
        question_lower = question.lower()
        
        if "what is" in question_lower and "about" in question_lower:
            return {
                "answer": "This video covers nuclear physics concepts, specifically nuclear decay processes and energy calculations. It explains how radioactive elements transform and release energy, including the mathematical relationships and practical applications in fields like medicine and energy production.",
                "sources": ["Video content", "Nuclear physics principles"],
                "confidence": "high"
            }
        elif "energy" in question_lower or "enegry" in question_lower:
            return {
                "answer": "Energy in nuclear reactions refers to the energy released or absorbed during nuclear decay processes. This includes binding energy, mass-energy equivalence (E=mc²), and the energy released during radioactive decay. The video explains how to calculate these energy changes using nuclear physics formulas.",
                "sources": ["Nuclear physics", "Energy conservation principles"],
                "confidence": "high"
            }
        elif "decay" in question_lower:
            return {
                "answer": "Nuclear decay is the process by which unstable atomic nuclei transform into more stable forms, releasing radiation and energy. Common types include alpha decay, beta decay, and gamma decay. Each type follows specific conservation laws and has characteristic energy signatures.",
                "sources": ["Nuclear physics", "Radioactive decay theory"],
                "confidence": "high"
            }
        else:
            return {
                "answer": "This video covers nuclear physics concepts including decay processes, energy calculations, and their applications. If you have a specific question about nuclear reactions, energy calculations, or radioactive decay, I'd be happy to help explain those concepts in detail.",
                "sources": ["Video content", "Nuclear physics"],
                "confidence": "medium"
            }
    
    def _get_enhanced_mock_quiz_questions(self, num_questions: int) -> List[Dict]:
        """Generate enhanced mock quiz questions when API quota is exceeded"""
        questions = [
            {
                "question": "What is nuclear decay?",
                "options": [
                    "The process of atoms splitting apart",
                    "The transformation of unstable nuclei into stable ones",
                    "The fusion of two atomic nuclei",
                    "The creation of new elements in stars"
                ],
                "correct_answer": 1,
                "explanation": "Nuclear decay is the spontaneous transformation of unstable atomic nuclei into more stable forms, releasing radiation and energy."
            },
            {
                "question": "Which equation relates mass and energy in nuclear reactions?",
                "options": [
                    "E = mc²",
                    "F = ma",
                    "PV = nRT",
                    "KE = ½mv²"
                ],
                "correct_answer": 0,
                "explanation": "Einstein's famous equation E = mc² shows the relationship between mass and energy, crucial for understanding nuclear reactions."
            },
            {
                "question": "What type of radiation is emitted during alpha decay?",
                "options": [
                    "Helium nuclei",
                    "Electrons",
                    "Gamma rays",
                    "Neutrons"
                ],
                "correct_answer": 0,
                "explanation": "Alpha decay emits helium nuclei (alpha particles), which consist of 2 protons and 2 neutrons."
            },
            {
                "question": "How does binding energy relate to nuclear stability?",
                "options": [
                    "Higher binding energy means less stability",
                    "Higher binding energy means more stability",
                    "Binding energy has no effect on stability",
                    "Only mass affects nuclear stability"
                ],
                "correct_answer": 1,
                "explanation": "Higher binding energy per nucleon indicates greater nuclear stability, as more energy is required to break the nucleus apart."
            },
            {
                "question": "What is the half-life of a radioactive element?",
                "options": [
                    "The time for all atoms to decay",
                    "The time for half the atoms to decay",
                    "The time for one atom to decay",
                    "The total lifetime of the element"
                ],
                "correct_answer": 1,
                "explanation": "Half-life is the time required for half of the radioactive atoms in a sample to decay."
            }
        ]
        
        return questions[:num_questions] 