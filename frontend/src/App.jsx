import { useState } from 'react'
import { motion } from 'framer-motion'
import { Play, Brain, MessageCircle, BookOpen, Zap, ChevronRight } from 'lucide-react'
import authService from './authService'
// import './App.css'

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [videoData, setVideoData] = useState(null)
  const [showVideoInput, setShowVideoInput] = useState(false)
  const [showAuth, setShowAuth] = useState(false)
  const [showDemo, setShowDemo] = useState(false)
  const [authMode, setAuthMode] = useState('signin') // 'signin' or 'register'

  const handleAnalyze = async () => {
    if (!youtubeUrl) return
    
    setIsAnalyzing(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await authService.authenticatedFetch(`${apiUrl}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ youtube_url: youtubeUrl }),
      })
      
      const data = await response.json()
      setVideoData(data)
    } catch (error) {
      console.error('Error analyzing video:', error)
      if (error.message === 'Authentication expired') {
        // Redirect to login if token expired
        setShowAuth(true)
        setAuthMode('signin')
      }
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleSignIn = () => {
    setAuthMode('signin')
    setShowAuth(true)
  }

  const handleGetStarted = () => {
    setAuthMode('register')
    setShowAuth(true)
  }

  const handleWatchDemo = () => {
    setShowDemo(true)
  }

  const handleBackToHome = () => {
    setShowVideoInput(false)
    setShowAuth(false)
    setShowDemo(false)
    setVideoData(null)
    setYoutubeUrl('')
  }

  const handleAuthSuccess = () => {
    setShowAuth(false)
    setShowVideoInput(true)
  }

  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI Summarization",
      description: "Get intelligent summaries and chapter breakdowns of any YouTube video"
    },
    {
      icon: <MessageCircle className="w-8 h-8" />,
      title: "Ask Me Anything",
      description: "Chat with an AI tutor about the video content"
    },
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: "Interactive Quizzes",
      description: "Test your knowledge with AI-generated quizzes and flashcards"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Smart Notes",
      description: "Take notes with AI assistance and export to your favorite tools"
    }
  ]

  if (videoData) {
    return <VideoWorkspace videoData={videoData} onBack={handleBackToHome} />
  }

  if (showAuth) {
    return <AuthPage mode={authMode} onSuccess={handleAuthSuccess} onBack={handleBackToHome} />
  }

  if (showDemo) {
    return <DemoPage onBack={handleBackToHome} />
  }

  if (showVideoInput) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
        {/* Navigation */}
        <nav className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-2"
            >
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold text-gradient">Zyndle AI</span>
            </motion.div>
            
            <motion.button
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              onClick={handleBackToHome}
              className="px-6 py-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg hover:bg-white/20 transition-all duration-300"
            >
              ← Back to Home
            </motion.button>
          </div>
        </nav>

        {/* Video Input Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto"
          >
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Start Your Learning Journey
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed">
              Paste any YouTube URL below and let AI transform it into an interactive learning experience
            </p>

            {/* Video Input */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="max-w-2xl mx-auto"
            >
              <div className="glass-dark rounded-2xl p-8">
                <div className="flex space-x-4">
                  <input
                    type="text"
                    placeholder="Paste a YouTube URL here..."
                    value={youtubeUrl}
                    onChange={(e) => setYoutubeUrl(e.target.value)}
                    className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleAnalyze}
                    disabled={isAnalyzing}
                    className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300 disabled:opacity-50 flex items-center space-x-2"
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        <span>Analyzing...</span>
                      </>
                    ) : (
                      <>
                        <Play className="w-5 h-5" />
                        <span>Analyze Video</span>
                      </>
                    )}
                  </motion.button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </section>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2"
          >
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5" />
            </div>
            <span className="text-xl font-bold text-gradient">Zyndle AI</span>
          </motion.div>
          
          <motion.button
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={handleSignIn}
            className="px-6 py-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg hover:bg-white/20 transition-all duration-300"
          >
            Sign In
          </motion.button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-4xl mx-auto"
        >
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            Turn YouTube into Your{' '}
            <span className="text-gradient">Personal Tutor</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed">
            Transform any YouTube video into an interactive learning experience with AI-powered summaries, 
            quizzes, and personalized tutoring.
          </p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleGetStarted}
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-300 flex items-center space-x-2"
            >
              <Play className="w-5 h-5" />
              <span>Start Learning</span>
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleWatchDemo}
              className="px-8 py-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg font-semibold text-lg hover:bg-white/20 transition-all duration-300"
            >
              Watch Demo
            </motion.button>
          </motion.div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">Powerful Learning Features</h2>
          <p className="text-xl text-gray-300">Everything you need to master any topic</p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              whileHover={{ y: -5 }}
              className="glass-dark rounded-xl p-6 text-center hover:neon-glow transition-all duration-300"
            >
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-300">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">How It Works</h2>
          <p className="text-xl text-gray-300">Three simple steps to transform your learning</p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="text-center"
          >
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
              1
            </div>
            <h3 className="text-xl font-semibold mb-2">Paste YouTube URL</h3>
            <p className="text-gray-300">Simply copy and paste any educational YouTube video link</p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="text-center"
          >
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
              2
            </div>
            <h3 className="text-xl font-semibold mb-2">AI Analysis</h3>
            <p className="text-gray-300">Our AI processes the video and creates summaries, chapters, and quizzes</p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9 }}
            className="text-center"
          >
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
              3
            </div>
            <h3 className="text-xl font-semibold mb-2">Learn Interactively</h3>
            <p className="text-gray-300">Chat with AI tutor, take quizzes, and track your progress</p>
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="text-center"
        >
          <div className="glass-dark rounded-2xl p-12 max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Learning?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of students who are already learning smarter with Zyndle AI
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleGetStarted}
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-300 flex items-center space-x-2 mx-auto"
            >
              <span>Get Started Free</span>
              <ChevronRight className="w-5 h-5" />
            </motion.button>
          </div>
        </motion.div>
      </section>
    </div>
  )
}

// Video Workspace Component
function VideoWorkspace({ videoData, onBack }) {
  const [activeTab, setActiveTab] = useState('summary')
  const [chatMessage, setChatMessage] = useState('')
  const [chatHistory, setChatHistory] = useState([])

  const handleChat = async () => {
    if (!chatMessage.trim()) return
    
    const newMessage = { role: 'user', content: chatMessage }
    setChatHistory([...chatHistory, newMessage])
    setChatMessage('')
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await authService.authenticatedFetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          question: chatMessage, 
          video_id: 'sample',
          transcript: videoData.transcript,
          summary: videoData.summary
        }),
      })
      
      const data = await response.json()
      setChatHistory(prev => [...prev, { role: 'assistant', content: data.answer }])
    } catch (error) {
      console.error('Error sending message:', error)
      // Add error message to chat
      setChatHistory(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }])
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button 
                onClick={onBack}
                className="text-blue-400 hover:text-blue-300"
              >
                ← Back to Home
              </button>
              <h1 className="text-xl font-semibold">{videoData.title}</h1>
            </div>
            <div className="text-sm text-gray-400">
              {videoData.channel} • {videoData.duration}
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Video Player */}
          <div className="lg:col-span-2">
            <div className="bg-black rounded-lg aspect-video mb-6 flex items-center justify-center">
              <div className="text-center">
                <Play className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                <p className="text-gray-400">Video Player Placeholder</p>
              </div>
            </div>

            {/* Chapters */}
            <div className="glass-dark rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">Chapters</h3>
              <div className="space-y-2">
                {videoData.chapters.map((chapter, index) => (
                  <button
                    key={index}
                    className="w-full text-left p-3 rounded-lg hover:bg-white/10 transition-colors"
                  >
                    <div className="flex justify-between items-center">
                      <span>{chapter.title}</span>
                      <span className="text-sm text-gray-400">
                        {Math.floor(chapter.start / 60)}:{(chapter.start % 60).toString().padStart(2, '0')}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Right Panel */}
          <div className="space-y-6">
            {/* Tabs */}
            <div className="glass-dark rounded-lg p-1">
              <div className="flex space-x-1">
                {['summary', 'chat', 'quiz'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                      activeTab === tab 
                        ? 'bg-blue-500 text-white' 
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    {tab.charAt(0).toUpperCase() + tab.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Tab Content */}
            <div className="glass-dark rounded-lg p-6 min-h-[400px]">
              {activeTab === 'summary' && (
                <div>
                  <h3 className="text-lg font-semibold mb-4">Summary</h3>
                  <p className="text-gray-300 leading-relaxed">{videoData.summary}</p>
                </div>
              )}

              {activeTab === 'chat' && (
                <div className="flex flex-col h-full">
                  <h3 className="text-lg font-semibold mb-4">Ask Me Anything</h3>
                  
                  {/* Chat History */}
                  <div className="flex-1 space-y-4 mb-4 overflow-y-auto">
                    {chatHistory.map((message, index) => (
                      <div
                        key={index}
                        className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-xs p-3 rounded-lg ${
                            message.role === 'user'
                              ? 'bg-blue-500 text-white'
                              : 'bg-gray-700 text-gray-200'
                          }`}
                        >
                          {message.content}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Chat Input */}
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={chatMessage}
                      onChange={(e) => setChatMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleChat()}
                      placeholder="Ask a question..."
                      className="flex-1 bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                      onClick={handleChat}
                      className="px-4 py-2 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors"
                    >
                      Send
                    </button>
                  </div>
                </div>
              )}

              {activeTab === 'quiz' && (
                <div>
                  <h3 className="text-lg font-semibold mb-4">Quiz</h3>
                  <p className="text-gray-300">Quiz feature coming soon...</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Auth Page Component
function AuthPage({ mode, onSuccess, onBack }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentMode, setCurrentMode] = useState(mode)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    
    try {
      if (currentMode === 'register') {
        await authService.register(email, name, password)
      } else {
        await authService.login(email, password)
      }
      onSuccess()
    } catch (error) {
      setError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const toggleMode = () => {
    setCurrentMode(currentMode === 'signin' ? 'register' : 'signin')
    setEmail('')
    setPassword('')
    setName('')
    setError('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white flex items-center justify-center">
      <div className="w-full max-w-md">
        {/* Navigation */}
        <div className="text-center mb-8">
          <button 
            onClick={onBack}
            className="text-blue-400 hover:text-blue-300 mb-4"
          >
            ← Back to Home
          </button>
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5" />
            </div>
            <span className="text-xl font-bold text-gradient">Zyndle AI</span>
          </div>
        </div>

        {/* Auth Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-dark rounded-2xl p-8"
        >
          <h2 className="text-2xl font-bold text-center mb-6">
            {currentMode === 'signin' ? 'Welcome Back' : 'Create Your Account'}
          </h2>
          
          {error && (
            <div className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-300 text-sm">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            {currentMode === 'register' && (
              <div>
                <label className="block text-sm font-medium mb-2">Full Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter your full name"
                  required
                />
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your email"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your password"
                required
              />
            </div>
            
            <motion.button
              type="submit"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              disabled={isLoading}
              className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300 disabled:opacity-50 flex items-center justify-center space-x-2"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Loading...</span>
                </>
              ) : (
                <span>{currentMode === 'signin' ? 'Sign In' : 'Create Account'}</span>
              )}
            </motion.button>
          </form>
          
          <div className="mt-6 text-center">
            <p className="text-gray-300">
              {currentMode === 'signin' ? "Don't have an account? " : "Already have an account? "}
              <button
                onClick={toggleMode}
                className="text-blue-400 hover:text-blue-300 font-medium"
              >
                {currentMode === 'signin' ? 'Sign up' : 'Sign in'}
              </button>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

// Demo Page Component
function DemoPage({ onBack }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2"
          >
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5" />
            </div>
            <span className="text-xl font-bold text-gradient">Zyndle AI</span>
          </motion.div>
          
          <motion.button
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={onBack}
            className="px-6 py-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg hover:bg-white/20 transition-all duration-300"
          >
            ← Back to Home
          </motion.button>
        </div>
      </nav>

      {/* Demo Content */}
      <section className="container mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-4xl mx-auto"
        >
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            See Zyndle AI in Action
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed">
            Watch how our AI transforms a YouTube video into an interactive learning experience
          </p>

          {/* Demo Video */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="max-w-4xl mx-auto"
          >
            <div className="glass-dark rounded-2xl p-8">
              <div className="aspect-video bg-black rounded-lg mb-6 overflow-hidden">
                <iframe
                  width="100%"
                  height="100%"
                  src="https://www.youtube.com/embed/dQw4w9WgXcQ?rel=0&modestbranding=1"
                  title="Zyndle AI Demo"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="rounded-lg"
                ></iframe>
              </div>
              
              <div className="text-center mb-8">
                <h3 className="text-xl font-semibold mb-2">Sample Educational Video</h3>
                <p className="text-gray-300">This will show a walkthrough of Zyndle AI features</p>
              </div>
              
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <Brain className="w-6 h-6" />
                  </div>
                  <h3 className="font-semibold mb-2">AI Analysis</h3>
                  <p className="text-sm text-gray-300">Watch how AI processes and summarizes content</p>
                </div>
                
                <div className="text-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <MessageCircle className="w-6 h-6" />
                  </div>
                  <h3 className="font-semibold mb-2">Interactive Chat</h3>
                  <p className="text-sm text-gray-300">See the AI tutor in action</p>
                </div>
                
                <div className="text-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <BookOpen className="w-6 h-6" />
                  </div>
                  <h3 className="font-semibold mb-2">Quiz Generation</h3>
                  <p className="text-sm text-gray-300">Experience AI-generated quizzes</p>
                </div>
              </div>
              
              <div className="mt-8 text-center">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={onBack}
                  className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300"
                >
                  Try It Yourself
                </motion.button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </section>
    </div>
  )
}

export default App
