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
                return self._get_enhanced_mock_chat_response(question, transcript, summary)
            
            if not self.client.api_key:
                return self._get_enhanced_mock_chat_response(question, transcript, summary)
            
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
                    {"role": "system", "content": "You are an expert educational assistant. Provide clear, helpful answers based on the video content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            print(f"Error generating chat response: {e}")
            if "insufficient_quota" in str(e) or "429" in str(e):
                print("⚠️ OpenAI API quota exceeded. Using enhanced mock chat response.")
                return self._get_enhanced_mock_chat_response(question, transcript, summary)
            return self._get_enhanced_mock_chat_response(question, transcript, summary)
    
    def generate_quiz(self, transcript: str, summary: str, num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions based on the video content"""
        try:
            if not self.client:
                return self._get_enhanced_mock_quiz_questions(num_questions, transcript, summary)
            
            if not self.client.api_key:
                return self._get_enhanced_mock_quiz_questions(num_questions, transcript, summary)
            
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
                return self._get_enhanced_mock_quiz_questions(num_questions, transcript, summary)
            return self._get_enhanced_mock_quiz_questions(num_questions, transcript, summary)
    
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
    
    def _get_enhanced_mock_chat_response(self, question: str, transcript: str = "", summary: str = "", title: str = "") -> Dict:
        """Generate an enhanced mock chat response when API quota is exceeded"""
        # Extract topic from video title or content
        topic = self._extract_topic_from_content(title, summary, transcript)
        
        question_lower = question.lower()
        
        # Generate context-aware responses based on the actual video topic
        if "what is" in question_lower and ("about" in question_lower or "topic" in question_lower):
            return {
                "answer": f"This video covers {topic} concepts and provides valuable insights for learners. It explains key principles, practical applications, and important takeaways that can help you understand the subject better.",
                "sources": ["Video content", f"{topic} principles"],
                "confidence": "high"
            }
        elif "main" in question_lower and ("point" in question_lower or "concept" in question_lower):
            return {
                "answer": f"The main concepts in this {topic} video include fundamental principles, practical applications, and real-world examples. The video breaks down complex ideas into understandable components.",
                "sources": [f"{topic} fundamentals", "Video explanations"],
                "confidence": "high"
            }
        elif "explain" in question_lower or "how" in question_lower:
            return {
                "answer": f"This {topic} video explains concepts through step-by-step demonstrations, clear examples, and practical applications. It shows how theoretical knowledge applies to real-world situations.",
                "sources": [f"{topic} theory", "Practical demonstrations"],
                "confidence": "medium"
            }
        else:
            return {
                "answer": f"This video covers {topic} concepts including fundamental principles, practical applications, and best practices. If you have specific questions about {topic}, I'd be happy to help explain those concepts in detail.",
                "sources": ["Video content", f"{topic} concepts"],
                "confidence": "medium"
            }
    
    def _get_enhanced_mock_quiz_questions(self, num_questions: int, transcript: str = "", summary: str = "", title: str = "") -> List[Dict]:
        """Generate enhanced mock quiz questions when API quota is exceeded"""
        # Extract topic from video content
        topic = self._extract_topic_from_content(title, summary, transcript)
        
        # Generate topic-specific questions
        questions = self._generate_topic_specific_questions(topic, num_questions)
        
        return questions[:num_questions]
    
    def _extract_topic_from_content(self, title: str, summary: str, transcript: str) -> str:
        """Extract the main topic from video content"""
        # Combine all text for analysis
        all_text = f"{title} {summary} {transcript}".lower()
        
        # Define topic keywords
        topics = {
            "Physics": ["physics", "force", "energy", "motion", "gravity", "nuclear", "quantum", "mechanics"],
            "Chemistry": ["chemistry", "chemical", "reaction", "molecule", "atom", "bond", "acid", "base"],
            "Mathematics": ["math", "mathematics", "algebra", "calculus", "equation", "formula", "geometry", "trigonometry"],
            "Biology": ["biology", "cell", "organism", "evolution", "genetics", "ecosystem", "species"],
            "Computer Science": ["programming", "code", "algorithm", "software", "computer", "data", "artificial intelligence", "machine learning"],
            "History": ["history", "historical", "ancient", "civilization", "war", "empire", "culture"],
            "Literature": ["literature", "book", "novel", "poetry", "author", "writing", "story"],
            "Economics": ["economics", "economy", "market", "finance", "business", "trade", "money"],
            "Psychology": ["psychology", "mind", "behavior", "mental", "cognitive", "therapy"],
            "Engineering": ["engineering", "design", "construction", "mechanical", "electrical", "civil"]
        }
        
        # Find the most relevant topic
        best_topic = "General Education"
        max_matches = 0
        
        for topic, keywords in topics.items():
            matches = sum(1 for keyword in keywords if keyword in all_text)
            if matches > max_matches:
                max_matches = matches
                best_topic = topic
        
        return best_topic
    
    def _generate_topic_specific_questions(self, topic: str, num_questions: int) -> List[Dict]:
        """Generate questions specific to the detected topic"""
        question_templates = {
            "Physics": [
                {
                    "question": "What is the main principle discussed in this physics video?",
                    "options": ["Energy conservation", "Force and motion", "Wave phenomena", "Thermodynamics"],
                    "correct_answer": 0,
                    "explanation": "Physics videos often focus on fundamental principles like energy conservation and its applications."
                },
                {
                    "question": "Which of the following is a key concept in physics?",
                    "options": ["Chemical bonding", "Mathematical equations", "Biological processes", "Historical events"],
                    "correct_answer": 1,
                    "explanation": "Physics relies heavily on mathematical equations to describe natural phenomena."
                }
            ],
            "Chemistry": [
                {
                    "question": "What type of reaction is most likely discussed in this chemistry video?",
                    "options": ["Chemical bonding", "Nuclear fusion", "Biological process", "Physical change"],
                    "correct_answer": 0,
                    "explanation": "Chemistry videos typically focus on chemical reactions and bonding between atoms."
                },
                {
                    "question": "Which concept is fundamental to understanding chemistry?",
                    "options": ["Atomic structure", "Gravity", "Evolution", "Programming"],
                    "correct_answer": 0,
                    "explanation": "Understanding atomic structure is essential for all chemical concepts."
                }
            ],
            "Mathematics": [
                {
                    "question": "What mathematical concept is likely the focus of this video?",
                    "options": ["Problem-solving methods", "Chemical reactions", "Historical events", "Biological processes"],
                    "correct_answer": 0,
                    "explanation": "Mathematics videos typically focus on problem-solving techniques and methods."
                },
                {
                    "question": "Which is essential for mathematical understanding?",
                    "options": ["Logical reasoning", "Chemical formulas", "Historical dates", "Biological terms"],
                    "correct_answer": 0,
                    "explanation": "Logical reasoning is fundamental to all mathematical concepts and problem-solving."
                }
            ],
            "Computer Science": [
                {
                    "question": "What programming concept is likely discussed in this video?",
                    "options": ["Algorithm design", "Chemical reactions", "Historical events", "Biological processes"],
                    "correct_answer": 0,
                    "explanation": "Computer science videos often focus on algorithm design and programming concepts."
                },
                {
                    "question": "Which is a key skill in computer science?",
                    "options": ["Problem-solving", "Chemical analysis", "Historical research", "Biological observation"],
                    "correct_answer": 0,
                    "explanation": "Problem-solving is essential for programming and algorithm development."
                }
            ],
            "Biology": [
                {
                    "question": "What biological concept is likely the main topic?",
                    "options": ["Cell structure", "Chemical equations", "Mathematical formulas", "Historical events"],
                    "correct_answer": 0,
                    "explanation": "Biology videos often focus on cellular and organismal structures and processes."
                },
                {
                    "question": "Which is fundamental to biological understanding?",
                    "options": ["Evolution", "Chemical bonding", "Mathematical proofs", "Historical dates"],
                    "correct_answer": 0,
                    "explanation": "Evolution is a fundamental concept that explains biological diversity."
                }
            ]
        }
        
        # Get questions for the detected topic, or use general questions as fallback
        questions = question_templates.get(topic, [
            {
                "question": "What is the main topic of this educational video?",
                "options": ["Learning concepts", "Entertainment", "Sports", "Music"],
                "correct_answer": 0,
                "explanation": "Educational videos focus on teaching and learning concepts."
            },
            {
                "question": "Which approach is most effective for learning from this video?",
                "options": ["Active engagement", "Passive watching", "Multitasking", "Skipping parts"],
                "correct_answer": 0,
                "explanation": "Active engagement helps you retain and understand the material better."
            }
        ])
        
        # Ensure we have enough questions
        while len(questions) < num_questions:
            questions.append({
                "question": f"What is an important concept in {topic}?",
                "options": ["Fundamental principles", "Advanced techniques", "Basic concepts", "All of the above"],
                "correct_answer": 3,
                "explanation": f"Understanding fundamental principles, basic concepts, and advanced techniques are all important in {topic}."
            })
        
        return questions[:num_questions] 