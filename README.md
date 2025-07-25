# Zyndle AI - AI Learning Companion for YouTube

🎓 **Turn YouTube into Your Personal Tutor**

Zyndle AI is an AI-powered web application that transforms any YouTube video into an interactive, personalized learning experience. The platform helps students not just watch—but understand, retain, and apply knowledge.

## ✨ Features

### 🎯 Core Features
- **🔗 YouTube Video Input**: Paste any YouTube URL and get instant analysis
- **📝 AI-Powered Summarization**: Get intelligent summaries and chapter breakdowns
- **❓ Ask-Me-Anything Chatbot**: Chat with an AI tutor about video content
- **🧠 Interactive Quizzes**: Test your knowledge with AI-generated questions
- **📈 Learning Dashboard**: Track your progress and learning history
- **🌍 Multilingual Support**: Auto-translate content into multiple languages

### 🎨 Design Features
- **🌑 Dark Mode**: Modern, futuristic dark theme with glassmorphism effects
- **✨ Animations**: Smooth Framer Motion animations and micro-interactions
- **📱 Responsive**: Works perfectly on desktop, tablet, and mobile
- **♿ Accessible**: Built with accessibility in mind

## 🛠️ Tech Stack

### Frontend
- **React 18** with Vite for fast development
- **TailwindCSS** for styling and responsive design
- **Framer Motion** for animations
- **Lucide React** for beautiful icons
- **Glassmorphism** design with backdrop blur effects

### Backend
- **FastAPI** for high-performance API
- **OpenAI/Claude** for AI-powered features
- **LangChain** for AI orchestration
- **ChromaDB** for vector search
- **PostgreSQL** for data persistence
- **Whisper** for video transcription

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Zyndle AI
   ```

2. **Set up the Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

3. **Set up the Backend**
   ```bash
   cd backend
   # Activate virtual environment
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start the server
   python main.py
   ```
   The backend API will be available at `http://localhost:8000`

4. **Environment Variables**
   Create a `.env` file in the backend directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   YOUTUBE_API_KEY=your_youtube_api_key_here
   DATABASE_URL=your_database_url_here
   ```

## 📖 Usage

1. **Landing Page**: Visit the homepage and paste a YouTube URL
2. **Video Analysis**: Click "Analyze Video" to process the content
3. **Learning Workspace**: 
   - View AI-generated summaries and chapters
   - Chat with the AI tutor about the content
   - Take interactive quizzes
   - Track your learning progress

## 🏗️ Project Structure

```
Zyndle AI/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # Utility functions
│   │   ├── App.jsx          # Main application component
│   │   └── index.css        # Global styles
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── api/             # API route handlers
│   │   ├── services/        # Business logic
│   │   ├── models/          # Data models
│   │   └── db/              # Database configuration
│   ├── main.py              # FastAPI application entry point
│   └── requirements.txt     # Python dependencies
└── README.md               # Project documentation
```

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Development
```bash
cd backend
venv\Scripts\activate
python main.py       # Start development server
```

### API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Landing page with YouTube input
- ✅ Video analysis and summarization
- ✅ Basic chatbot functionality
- ✅ Quiz generation
- ✅ Modern UI with dark theme

### Phase 2 (Next)
- 🔄 User authentication and profiles
- 🔄 Advanced note-taking features
- 🔄 Export functionality (PDF, Notion, Google Docs)
- 🔄 Learning progress tracking
- 🔄 Multilingual support

### Phase 3 (Future)
- 🔄 Chrome extension
- 🔄 Community features
- 🔄 AI tutor scheduling
- 🔄 Advanced analytics
- 🔄 Mobile app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the AI capabilities
- YouTube for the video platform
- The open-source community for the amazing tools and libraries

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the documentation
- Contact the development team

---

**Made with ❤️ for better learning experiences**
