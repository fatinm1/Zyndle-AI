import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Play, Brain, MessageCircle, BookOpen, Zap, ChevronRight, Star } from 'lucide-react'
import authService from './authService'
import ZyndleLogo from './components/ZyndleLogo'
// import './App.css'

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [videoData, setVideoData] = useState(null)
  const [showVideoInput, setShowVideoInput] = useState(false)
  const [showAuth, setShowAuth] = useState(false)

  const [showProgress, setShowProgress] = useState(false)
  const [authMode, setAuthMode] = useState('signin') // 'signin' or 'register'
  const [demoMode, setDemoMode] = useState(false) // New demo mode state

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



  const handleBackToHome = () => {
    setShowVideoInput(false)
    setShowAuth(false)
    setShowProgress(false)
    setVideoData(null)
    setYoutubeUrl('')
    
    // Always go back to home page, regardless of authentication status
    // The home page will show different content based on authentication
  }

  const handleShowProgress = () => {
    setShowProgress(true)
  }

  const handleAuthSuccess = () => {
    setShowAuth(false)
    setShowVideoInput(true)
  }

  const handleDemoMode = () => {
    setDemoMode(true)
    // Create demo video data
    const demoData = {
      title: "Nuclear Physics: Decay Processes and Energy",
      channel: "Physics Academy",
      duration: "15:32",
      summary: "This comprehensive video explores nuclear physics fundamentals, covering binding energy, mass defect, and various decay processes. It explains how nuclear reactions can release energy according to Einstein's E=mc² equation, with practical examples and clear visualizations.",
      chapters: [
        { title: "Introduction to Nuclear Physics", start: 0, end: 135, description: "Overview of atomic structure and nuclear forces" },
        { title: "Nuclear Binding Energy", start: 135, end: 390, description: "Understanding nuclear stability and mass defect" },
        { title: "Types of Nuclear Decay", start: 390, end: 690, description: "Alpha, beta, and gamma decay processes" },
        { title: "Energy Release in Reactions", start: 690, end: 930, description: "E=mc² and practical applications" }
      ],
      transcript: "Welcome to our exploration of nuclear physics. Today we'll dive deep into the fascinating world of atomic nuclei and their behavior. Nuclear physics is fundamental to understanding everything from power generation to medical imaging. Let's start with the concept of nuclear binding energy. When protons and neutrons come together to form a nucleus, they release energy. This is the binding energy that holds the nucleus together. The mass of the nucleus is actually less than the sum of its individual particles. This mass difference, called the mass defect, is converted to energy according to Einstein's famous equation E=mc². Nuclear decay occurs when unstable nuclei transform into more stable forms. Alpha decay releases helium nuclei, beta decay changes neutrons to protons, and gamma decay releases high-energy electromagnetic radiation. Each type of decay has different characteristics and energy implications. Understanding these processes is crucial for applications like nuclear power, medical treatments, and dating archaeological finds. The energy released in nuclear reactions is enormous compared to chemical reactions, making nuclear power an efficient energy source. However, it also requires careful control and safety measures. As we continue exploring nuclear physics, remember that these fundamental principles govern everything from the stars above to the atoms within us.",
      thumbnail: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&h=225&fit=crop",
      view_count: "125K",
      like_count: "2.1K"
    }
    setVideoData(demoData)
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
    return <VideoWorkspace videoData={videoData} onBack={handleBackToHome} demoMode={demoMode} />
  }

  if (showAuth) {
    return <AuthPage mode={authMode} onSuccess={handleAuthSuccess} onBack={handleBackToHome} />
  }



  if (showProgress) {
    return <ProgressDashboard onBack={handleBackToHome} />
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
              <ZyndleLogo />
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
            <ZyndleLogo />
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-4"
          >
            {authService.isAuthenticated() ? (
              <>
                <button
                  onClick={handleShowProgress}
                  className="px-4 py-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg hover:bg-white/20 transition-all duration-300"
                >
                  View Progress
                </button>
                <button
                  onClick={() => setShowVideoInput(true)}
                  className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-300"
                >
                  Continue Analysis
                </button>
                <button
                  onClick={() => {
                    authService.logout()
                    window.location.reload()
                  }}
                  className="px-4 py-2 bg-red-500/20 border border-red-500/30 rounded-lg hover:bg-red-500/30 transition-all duration-300"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <button
                onClick={handleSignIn}
                className="px-6 py-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg hover:bg-white/20 transition-all duration-300"
              >
                Sign In
              </button>
            )}
          </motion.div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center relative overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          {/* Floating Orbs */}
          <div className="absolute top-20 left-20 w-32 h-32 bg-gradient-to-r from-blue-400/20 to-purple-400/20 rounded-full blur-xl animate-pulse"></div>
          <div className="absolute top-40 right-32 w-24 h-24 bg-gradient-to-r from-purple-400/20 to-pink-400/20 rounded-full blur-xl animate-pulse delay-1000"></div>
          <div className="absolute bottom-32 left-1/3 w-28 h-28 bg-gradient-to-r from-green-400/20 to-blue-400/20 rounded-full blur-xl animate-pulse delay-2000"></div>
          
          {/* Animated Grid */}
          <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.1)_1px,transparent_1px)] bg-[size:50px_50px] animate-pulse"></div>
        </div>

        <div className="container mx-auto px-6 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="text-center"
          >
            {/* Enhanced Logo Animation */}
            <motion.div 
              initial={{ scale: 0.8, rotate: -5 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="mb-8 flex justify-center"
            >
              <div className="relative">
                <ZyndleLogo />
                {/* Glow Effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full blur-2xl opacity-30 animate-pulse"></div>
              </div>
            </motion.div>

            {/* Enhanced Main Headline */}
            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.3 }}
              className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
            >
              <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-pulse">
                Transform
              </span>
              <br />
              <span className="text-white">Any YouTube Video</span>
              <br />
              <span className="bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                Into Learning Magic
              </span>
            </motion.h1>

            {/* Enhanced Subtitle */}
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.6 }}
              className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed"
            >
              Experience the future of learning with AI-powered video analysis, 
              <span className="text-blue-400 font-semibold"> interactive quizzes</span>, 
              <span className="text-purple-400 font-semibold"> smart summaries</span>, and 
              <span className="text-green-400 font-semibold"> personalized insights</span>
            </motion.p>

            {/* Enhanced CTA Buttons */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.9 }}
              className="flex flex-col sm:flex-row gap-6 justify-center items-center"
            >
              {isAuthenticated ? (
                <>
                  <motion.button
                    whileHover={{ 
                      scale: 1.05,
                      boxShadow: "0 20px 40px rgba(59, 130, 246, 0.3)"
                    }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowVideoInput(true)}
                    className="group relative px-10 py-5 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl font-bold text-xl text-white overflow-hidden transition-all duration-300"
                  >
                    <span className="relative z-10 flex items-center space-x-3">
                      <span>Continue Learning</span>
                      <ChevronRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
                    </span>
                    {/* Animated Background */}
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    {/* Shine Effect */}
                    <div className="absolute inset-0 -skew-x-12 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ 
                      scale: 1.05,
                      boxShadow: "0 20px 40px rgba(168, 85, 247, 0.3)"
                    }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleDemoMode}
                    className="group relative px-10 py-5 bg-white/10 backdrop-blur-xl border-2 border-white/20 rounded-2xl font-bold text-xl text-white hover:bg-white/20 transition-all duration-300 overflow-hidden"
                  >
                    <span className="relative z-10 flex items-center space-x-3">
                      <span className="text-2xl">🚀</span>
                      <span>Try Demo Mode</span>
                    </span>
                    {/* Glow Effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
                  </motion.button>
                </>
              ) : (
                <>
                  <motion.button
                    whileHover={{ 
                      scale: 1.05,
                      boxShadow: "0 20px 40px rgba(59, 130, 246, 0.3)"
                    }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleGetStarted}
                    className="group relative px-10 py-5 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl font-bold text-xl text-white overflow-hidden transition-all duration-300"
                  >
                    <span className="relative z-10 flex items-center space-x-3">
                      <Play className="w-6 h-6 group-hover:scale-110 transition-transform" />
                      <span>Start Learning Free</span>
                      <ChevronRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
                    </span>
                    {/* Animated Background */}
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    {/* Shine Effect */}
                    <div className="absolute inset-0 -skew-x-12 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ 
                      scale: 1.05,
                      boxShadow: "0 20px 40px rgba(168, 85, 247, 0.3)"
                    }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleDemoMode}
                    className="group relative px-10 py-5 bg-white/10 backdrop-blur-xl border-2 border-white/20 rounded-2xl font-bold text-xl text-white hover:bg-white/20 transition-all duration-300 overflow-hidden"
                  >
                    <span className="relative z-10 flex items-center space-x-3">
                      <span className="text-2xl">🚀</span>
                      <span>Try Demo Mode</span>
                    </span>
                    {/* Glow Effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
                  </motion.button>
                </>
              )}
            </motion.div>

            {/* Enhanced Social Proof */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 1.2 }}
              className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-8 text-gray-400"
            >
              <div className="flex items-center space-x-2">
                <div className="flex -space-x-2">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full border-2 border-gray-900"></div>
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full border-2 border-gray-900"></div>
                  <div className="w-8 h-8 bg-gradient-to-r from-pink-400 to-red-400 rounded-full border-2 border-gray-900"></div>
                </div>
                <span className="text-sm">Join 10,000+ learners</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                  ))}
                </div>
                <span className="text-sm">4.9/5 rating</span>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-6 py-20 relative">
        {/* Background Decoration */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-blue-900/10 to-transparent"></div>
        
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16 relative z-10"
        >
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-4xl md:text-6xl font-bold mb-6"
          >
            <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Powerful Learning
            </span>
            <br />
            <span className="text-white">Features</span>
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto"
          >
            Everything you need to master any topic with AI-powered intelligence
          </motion.p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 relative z-10">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30, scale: 0.9 }}
              whileInView={{ opacity: 1, y: 0, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 * index }}
              whileHover={{ 
                y: -10, 
                scale: 1.05,
                transition: { duration: 0.3 }
              }}
              className="group relative"
            >
              {/* Glow Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
              
              <div className="relative glass-dark rounded-2xl p-8 text-center hover:neon-glow transition-all duration-500 border border-white/10 group-hover:border-white/20">
                {/* Enhanced Icon Container */}
                <motion.div 
                  whileHover={{ rotate: 360, scale: 1.1 }}
                  transition={{ duration: 0.6 }}
                  className="w-20 h-20 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:shadow-2xl group-hover:shadow-blue-500/25 transition-all duration-500"
                >
                  <div className="text-white text-3xl">
                    {feature.icon}
                  </div>
                </motion.div>
                
                <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-blue-400 transition-colors duration-300">
                  {feature.title}
                </h3>
                <p className="text-gray-300 text-lg leading-relaxed group-hover:text-gray-200 transition-colors duration-300">
                  {feature.description}
                </p>
                
                {/* Hover Indicator */}
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 w-0 h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full group-hover:w-16 transition-all duration-500"></div>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-6 py-20 relative">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.3),transparent_50%)]"></div>
        </div>
        
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16 relative z-10"
        >
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-4xl md:text-6xl font-bold mb-6"
          >
            <span className="bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
              How It Works
            </span>
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto"
          >
            Three simple steps to transform your learning experience
          </motion.p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 relative z-10">
          {/* Step 1 */}
          <motion.div
            initial={{ opacity: 0, y: 30, scale: 0.9 }}
            whileInView={{ opacity: 1, y: 0, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="group relative text-center"
          >
            {/* Connection Line */}
            <div className="hidden md:block absolute top-16 right-0 w-full h-0.5 bg-gradient-to-r from-blue-500 to-transparent transform translate-x-1/2"></div>
            
            <div className="relative">
              {/* Enhanced Step Circle */}
              <motion.div 
                whileHover={{ scale: 1.1, rotate: 5 }}
                transition={{ duration: 0.3 }}
                className="w-24 h-24 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 text-3xl font-bold text-white shadow-2xl shadow-blue-500/25 group-hover:shadow-2xl group-hover:shadow-purple-500/25 transition-all duration-500"
              >
                1
              </motion.div>
              
              <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-blue-400 transition-colors duration-300">
                Paste YouTube URL
              </h3>
              <p className="text-gray-300 text-lg leading-relaxed group-hover:text-gray-200 transition-colors duration-300">
                Simply copy and paste any educational YouTube video link into our platform
              </p>
              
              {/* Hover Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10"></div>
            </div>
          </motion.div>
          
          {/* Step 2 */}
          <motion.div
            initial={{ opacity: 0, y: 30, scale: 0.9 }}
            whileInView={{ opacity: 1, y: 0, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="group relative text-center"
          >
            {/* Connection Line */}
            <div className="hidden md:block absolute top-16 left-0 w-full h-0.5 bg-gradient-to-l from-purple-500 to-transparent transform -translate-x-1/2"></div>
            <div className="hidden md:block absolute top-16 right-0 w-full h-0.5 bg-gradient-to-r from-purple-500 to-transparent transform translate-x-1/2"></div>
            
            <div className="relative">
              {/* Enhanced Step Circle */}
              <motion.div 
                whileHover={{ scale: 1.1, rotate: -5 }}
                transition={{ duration: 0.3 }}
                className="w-24 h-24 bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 rounded-full flex items-center justify-center mx-auto mb-6 text-3xl font-bold text-white shadow-2xl shadow-purple-500/25 group-hover:shadow-2xl group-hover:shadow-pink-500/25 transition-all duration-500"
              >
                2
              </motion.div>
              
              <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-purple-400 transition-colors duration-300">
                AI Analysis
              </h3>
              <p className="text-gray-300 text-lg leading-relaxed group-hover:text-gray-200 transition-colors duration-300">
                Our AI processes the video to create summaries, identify key topics, and generate insights
              </p>
              
              {/* Hover Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-pink-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10"></div>
            </div>
          </motion.div>
          
          {/* Step 3 */}
          <motion.div
            initial={{ opacity: 0, y: 30, scale: 0.9 }}
            whileInView={{ opacity: 1, y: 0, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="group relative text-center"
          >
            {/* Connection Line */}
            <div className="hidden md:block absolute top-16 left-0 w-full h-0.5 bg-gradient-to-l from-pink-500 to-transparent transform -translate-x-1/2"></div>
            
            <div className="relative">
              {/* Enhanced Step Circle */}
              <motion.div 
                whileHover={{ scale: 1.1, rotate: 5 }}
                transition={{ duration: 0.3 }}
                className="w-24 h-24 bg-gradient-to-r from-pink-500 via-red-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-6 text-3xl font-bold text-white shadow-2xl shadow-pink-500/25 group-hover:shadow-2xl group-hover:shadow-red-500/25 transition-all duration-500"
              >
                3
              </motion.div>
              
              <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-pink-400 transition-colors duration-300">
                Interactive Learning
              </h3>
              <p className="text-gray-300 text-lg leading-relaxed group-hover:text-gray-200 transition-colors duration-300">
                Engage with quizzes, chat with AI tutor, and take smart notes to master the content
              </p>
              
              {/* Hover Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-pink-500/5 to-red-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10"></div>
            </div>
          </motion.div>
        </div>
        
        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="text-center mt-16 relative z-10"
        >
          <motion.button
            whileHover={{ 
              scale: 1.05,
              boxShadow: "0 20px 40px rgba(59, 130, 246, 0.3)"
            }}
            whileTap={{ scale: 0.95 }}
            onClick={handleDemoMode}
            className="group relative px-12 py-5 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl font-bold text-xl text-white overflow-hidden transition-all duration-300"
          >
            <span className="relative z-10 flex items-center space-x-3">
              <span>🚀 Start Your Learning Journey</span>
              <ChevronRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
            </span>
            {/* Shine Effect */}
            <div className="absolute inset-0 -skew-x-12 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
          </motion.button>
        </motion.div>
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
            {authService.isAuthenticated() ? (
              <>
                <h2 className="text-3xl font-bold mb-4">Continue Your Learning Journey</h2>
                <p className="text-xl text-gray-300 mb-8">
                  Ready to dive into another educational video? Your progress is being tracked!
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowVideoInput(true)}
                    className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-300 flex items-center space-x-2"
                  >
                    <span>Continue Analysis</span>
                    <ChevronRight className="w-5 h-5" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleDemoMode}
                    className="px-8 py-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg font-semibold text-lg hover:bg-white/20 transition-all duration-300"
                  >
                    🚀 Try Demo Mode
                  </motion.button>
                </div>
              </>
            ) : (
              <>
                <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Learning?</h2>
                <p className="text-xl text-gray-300 mb-8">
                  Join thousands of students who are already learning smarter with Zyndle AI
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleGetStarted}
                    className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-300 flex items-center space-x-2"
                  >
                    <span>Get Started Free</span>
                    <ChevronRight className="w-5 h-5" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleDemoMode}
                    className="px-8 py-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-lg font-semibold text-lg hover:bg-white/20 transition-all duration-300"
                  >
                    🚀 Try Demo Mode
                  </motion.button>
                </div>
              </>
            )}
          </div>
        </motion.div>
      </section>
    </div>
  )
}

// Video Workspace Component
function VideoWorkspace({ videoData, onBack, demoMode }) {
  const [activeTab, setActiveTab] = useState('summary')
  const [chatMessage, setChatMessage] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [quizQuestions, setQuizQuestions] = useState([])
  const [quizAnswers, setQuizAnswers] = useState({})
  const [quizSubmitted, setQuizSubmitted] = useState(false)
  const [quizScore, setQuizScore] = useState(0)
  const [isLoadingQuiz, setIsLoadingQuiz] = useState(false)
  const [notes, setNotes] = useState([])
  const [newNote, setNewNote] = useState('')
  const [isLoadingNotes, setIsLoadingNotes] = useState(false)

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
          summary: videoData.summary,
          title: videoData.title || ''
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

  const loadQuiz = async () => {
    if (quizQuestions.length > 0) return // Already loaded
    
    setIsLoadingQuiz(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await authService.authenticatedFetch(`${apiUrl}/quiz`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          video_id: 'sample',
          transcript: videoData.transcript,
          summary: videoData.summary,
          title: videoData.title || '',
          num_questions: 5
        }),
      })
      
      const data = await response.json()
      setQuizQuestions(data.questions)
    } catch (error) {
      console.error('Error loading quiz:', error)
    } finally {
      setIsLoadingQuiz(false)
    }
  }

  const handleQuizAnswer = (questionIndex, answerIndex) => {
    setQuizAnswers(prev => ({
      ...prev,
      [questionIndex]: answerIndex
    }))
  }

  const submitQuiz = async () => {
    let correct = 0
    quizQuestions.forEach((question, index) => {
      if (quizAnswers[index] === question.correct_answer) {
        correct++
      }
    })
    const score = Math.round((correct / quizQuestions.length) * 100)
    setQuizScore(score)
    setQuizSubmitted(true)
    
    // Record quiz result for progress tracking
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      await authService.authenticatedFetch(`${apiUrl}/progress/record-quiz`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          video_id: 'sample',
          score: score,
          total_questions: quizQuestions.length
        }),
      })
    } catch (error) {
      console.error('Error recording quiz result:', error)
      // Don't show error to user, just log it
    }
  }

  const resetQuiz = () => {
    setQuizAnswers({})
    setQuizSubmitted(false)
    setQuizScore(0)
  }

  // Load quiz when tab is selected
  React.useEffect(() => {
    if (activeTab === 'quiz' && quizQuestions.length === 0) {
      loadQuiz()
    }
  }, [activeTab])

  // Load notes when tab is selected
  React.useEffect(() => {
    if (activeTab === 'notes' && notes.length === 0) {
      loadNotes()
    }
  }, [activeTab])

  const loadNotes = async () => {
    setIsLoadingNotes(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await authService.authenticatedFetch(`${apiUrl}/notes?video_id=sample`)
      const data = await response.json()
      setNotes(data.notes || [])
    } catch (error) {
      console.error('Error loading notes:', error)
    } finally {
      setIsLoadingNotes(false)
    }
  }

  const saveNote = async () => {
    if (!newNote.trim()) return
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await authService.authenticatedFetch(`${apiUrl}/notes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          video_id: 'sample',
          content: newNote,
          title: `Note on ${videoData.title}`
        }),
      })
      
      const savedNote = await response.json()
      setNotes([savedNote, ...notes])
      setNewNote('')
    } catch (error) {
      console.error('Error saving note:', error)
    }
  }

  const deleteNote = async (noteId) => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      await authService.authenticatedFetch(`${apiUrl}/notes/${noteId}`, {
        method: 'DELETE'
      })
      
      setNotes(notes.filter(note => note.id !== noteId))
    } catch (error) {
      console.error('Error deleting note:', error)
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
              {demoMode && (
                <span className="px-3 py-1 bg-gradient-to-r from-blue-500 to-purple-500 text-white text-xs font-medium rounded-full">
                  🚀 Demo Mode
                </span>
              )}
            </div>
            <div className="text-sm text-gray-400">
              {videoData.channel} • {videoData.duration}
            </div>
          </div>
        </div>
      </header>

      {demoMode && (
        <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 border-b border-blue-500/30">
          <div className="container mx-auto px-6 py-4">
            <div className="text-center">
              <p className="text-blue-300 font-medium">
                🎯 Demo Mode: Experience all Zyndle AI features with sample content
              </p>
              <p className="text-blue-200 text-sm mt-1">
                Try the chat, quiz, and notes features below to see how AI enhances learning
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="container mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Video Player */}
          <div className="lg:col-span-2">
            <div className="bg-black rounded-lg aspect-video mb-6 flex items-center justify-center overflow-hidden">
              {demoMode ? (
                <div className="text-center p-8">
                  <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Play className="w-12 h-12 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-white">Demo Mode Active</h3>
                  <p className="text-gray-300 mb-4">Experience Zyndle AI features with sample content</p>
                  <div className="flex items-center justify-center space-x-4 text-sm text-gray-400">
                    <span>🎯 AI Analysis</span>
                    <span>💬 Smart Chat</span>
                    <span>📝 Interactive Notes</span>
                  </div>
                </div>
              ) : (
                <div className="text-center">
                  <Play className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                  <p className="text-gray-400">Video Player Placeholder</p>
                </div>
              )}
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
                {['summary', 'chat', 'quiz', 'notes'].map((tab) => (
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
                  
                  {demoMode && (
                    <div className="mb-4 p-3 bg-blue-500/20 border border-blue-500/30 rounded-lg">
                      <p className="text-blue-200 text-sm">
                        💡 <strong>Demo Tip:</strong> Try asking about "nuclear binding energy", "decay processes", 
                        or "E=mc²" to see how the AI responds with contextual information from the video content.
                      </p>
                    </div>
                  )}
                  
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
                  
                  {demoMode && (
                    <div className="mb-4 p-3 bg-green-500/20 border border-green-500/30 rounded-lg">
                      <p className="text-green-200 text-sm">
                        🎯 <strong>Demo Quiz:</strong> Test your knowledge with these AI-generated questions about nuclear physics. 
                        Each question includes detailed explanations to help you learn.
                      </p>
                    </div>
                  )}
                  
                  {isLoadingQuiz ? (
                    <div className="text-center py-8">
                      <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                      <p className="text-gray-300">Loading quiz questions...</p>
                    </div>
                  ) : quizQuestions.length > 0 ? (
                    <div>
                      {!quizSubmitted ? (
                        <div>
                          <p className="text-gray-300 mb-4">Test your knowledge with these questions:</p>
                          <div className="space-y-6">
                            {quizQuestions.map((question, qIndex) => (
                              <div key={qIndex} className="border border-gray-700 rounded-lg p-4">
                                <h4 className="font-medium mb-3">{qIndex + 1}. {question.question}</h4>
                                <div className="space-y-2">
                                  {question.options.map((option, oIndex) => (
                                    <label key={oIndex} className="flex items-center space-x-3 cursor-pointer">
                                      <input
                                        type="radio"
                                        name={`question-${qIndex}`}
                                        checked={quizAnswers[qIndex] === oIndex}
                                        onChange={() => handleQuizAnswer(qIndex, oIndex)}
                                        className="text-blue-500 focus:ring-blue-500"
                                      />
                                      <span className="text-gray-300">{option}</span>
                                    </label>
                                  ))}
                                </div>
                              </div>
                            ))}
                          </div>
                          <button
                            onClick={submitQuiz}
                            disabled={Object.keys(quizAnswers).length < quizQuestions.length}
                            className="mt-6 w-full py-2 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            Submit Quiz
                          </button>
                        </div>
                      ) : (
                        <div>
                          <div className="text-center mb-6">
                            <h4 className="text-xl font-semibold mb-2">Quiz Results</h4>
                            <div className="text-3xl font-bold text-blue-500 mb-2">{quizScore}%</div>
                            <p className="text-gray-300">
                              You got {Math.round((quizScore / 100) * quizQuestions.length)} out of {quizQuestions.length} questions correct!
                            </p>
                          </div>
                          
                          <div className="space-y-4">
                            {quizQuestions.map((question, qIndex) => (
                              <div key={qIndex} className="border border-gray-700 rounded-lg p-4">
                                <h4 className="font-medium mb-2">{qIndex + 1}. {question.question}</h4>
                                <div className="space-y-1 mb-3">
                                  {question.options.map((option, oIndex) => (
                                    <div
                                      key={oIndex}
                                      className={`p-2 rounded ${
                                        oIndex === question.correct_answer
                                          ? 'bg-green-500/20 border border-green-500/30'
                                          : oIndex === quizAnswers[qIndex] && oIndex !== question.correct_answer
                                          ? 'bg-red-500/20 border border-red-500/30'
                                          : 'bg-gray-700/50'
                                      }`}
                                    >
                                      {option}
                                      {oIndex === question.correct_answer && (
                                        <span className="ml-2 text-green-400">✓ Correct</span>
                                      )}
                                      {oIndex === quizAnswers[qIndex] && oIndex !== question.correct_answer && (
                                        <span className="ml-2 text-red-400">✗ Your Answer</span>
                                      )}
                                    </div>
                                  ))}
                                </div>
                                <p className="text-sm text-gray-400">{question.explanation}</p>
                              </div>
                            ))}
                          </div>
                          
                          <button
                            onClick={resetQuiz}
                            className="mt-6 w-full py-2 bg-gray-600 rounded-lg hover:bg-gray-700 transition-colors"
                          >
                            Take Quiz Again
                          </button>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-gray-300">No quiz questions available.</p>
                  )}
                </div>
              )}

              {activeTab === 'notes' && (
                <div className="flex flex-col h-full">
                  <h3 className="text-lg font-semibold mb-4">Your Notes</h3>
                  
                  {demoMode && (
                    <div className="mb-4 p-3 bg-purple-500/20 border border-purple-500/30 rounded-lg">
                      <p className="text-purple-200 text-sm">
                        📝 <strong>Demo Notes:</strong> Experience the note-taking system with pre-loaded sample notes. 
                        Add your own notes to see how the AI organizes and categorizes your learning content.
                      </p>
                    </div>
                  )}
                  
                  {isLoadingNotes ? (
                    <div className="text-center py-8">
                      <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                      <p className="text-gray-300">Loading notes...</p>
                    </div>
                  ) : notes.length > 0 ? (
                    <div className="flex-1 space-y-4 overflow-y-auto">
                      {notes.map((note) => (
                        <div key={note.id} className="bg-gray-800 rounded-lg p-4">
                          <h4 className="font-medium mb-2">{note.title}</h4>
                          <p className="text-gray-300">{note.content}</p>
                          <button
                            onClick={() => deleteNote(note.id)}
                            className="mt-2 text-red-400 hover:text-red-300 text-sm"
                          >
                            Delete Note
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-300">No notes yet for this video. Add one!</p>
                  )}

                  {/* New Note Input */}
                  <div className="mt-6">
                    <textarea
                      value={newNote}
                      onChange={(e) => setNewNote(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && saveNote()}
                      placeholder="Add a new note..."
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows="3"
                    ></textarea>
                    <button
                      onClick={saveNote}
                      className="mt-2 w-full py-2 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors"
                    >
                      Save Note
                    </button>
                  </div>
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
            <ZyndleLogo />
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
  const [activeDemo, setActiveDemo] = useState('overview')
  const [chatMessage, setChatMessage] = useState('')
  const [chatHistory, setChatHistory] = useState([
    { role: 'assistant', content: "Hello! I'm your AI tutor. I can help you understand any topic from the video. What would you like to know about nuclear physics?" }
  ])
  const [quizAnswers, setQuizAnswers] = useState({})
  const [quizSubmitted, setQuizSubmitted] = useState(false)
  const [quizScore, setQuizScore] = useState(0)
  const [notes, setNotes] = useState([
    { id: 1, title: "Key Nuclear Concepts", content: "Nuclear binding energy, mass defect, and E=mc² relationship are fundamental to understanding nuclear reactions." },
    { id: 2, title: "Decay Processes", content: "Alpha, beta, and gamma decay each have different characteristics and energy implications." }
  ])
  const [newNote, setNewNote] = useState('')

  const handleChat = () => {
    if (!chatMessage.trim()) return
    
    const userMessage = { role: 'user', content: chatMessage }
    setChatHistory([...chatHistory, userMessage])
    
    // Simulate AI response based on the question
    const aiResponse = generateAIResponse(chatMessage)
    setChatHistory(prev => [...prev, { role: 'assistant', content: aiResponse }])
    setChatMessage('')
  }

  const generateAIResponse = (question) => {
    const responses = {
      'nuclear': "Nuclear physics deals with the structure and behavior of atomic nuclei. The key concept is that nuclei can release energy through processes like fission and fusion. Einstein's famous equation E=mc² shows how mass can be converted to energy.",
      'binding': "Nuclear binding energy is the energy required to separate a nucleus into its individual protons and neutrons. It's what holds the nucleus together and is related to the mass defect - the difference between the mass of the nucleus and the sum of its parts.",
      'decay': "Nuclear decay occurs when unstable nuclei transform into more stable forms. Alpha decay emits helium nuclei, beta decay changes neutrons to protons (or vice versa), and gamma decay releases high-energy electromagnetic radiation.",
      'energy': "Nuclear reactions can release enormous amounts of energy. In nuclear power plants, controlled fission reactions generate electricity. The energy comes from the mass difference between reactants and products, following E=mc².",
      'default': "That's a great question about nuclear physics! The video covers fundamental concepts like nuclear binding energy, decay processes, and how nuclear reactions can release energy. Would you like me to explain any specific aspect in more detail?"
    }
    
    const lowerQuestion = question.toLowerCase()
    for (const [key, response] of Object.entries(responses)) {
      if (lowerQuestion.includes(key)) {
        return response
      }
    }
    return responses.default
  }

  const handleQuizAnswer = (questionIndex, answerIndex) => {
    setQuizAnswers(prev => ({
      ...prev,
      [questionIndex]: answerIndex
    }))
  }

  const submitQuiz = () => {
    let correct = 0
    demoQuizQuestions.forEach((question, index) => {
      if (quizAnswers[index] === question.correct_answer) {
        correct++
      }
    })
    const score = Math.round((correct / demoQuizQuestions.length) * 100)
    setQuizScore(score)
    setQuizSubmitted(true)
  }

  const resetQuiz = () => {
    setQuizAnswers({})
    setQuizSubmitted(false)
    setQuizScore(0)
  }

  const saveNote = () => {
    if (!newNote.trim()) return
    const note = {
      id: Date.now(),
      title: `Note on Nuclear Physics`,
      content: newNote
    }
    setNotes([note, ...notes])
    setNewNote('')
  }

  const deleteNote = (noteId) => {
    setNotes(notes.filter(note => note.id !== noteId))
  }

  const demoQuizQuestions = [
    {
      question: "What is the main source of energy in nuclear reactions?",
      options: ["Chemical bonds", "Mass conversion", "Electromagnetic force", "Gravitational energy"],
      correct_answer: 1,
      explanation: "Nuclear reactions convert mass to energy according to Einstein's equation E=mc², where a small amount of mass can release enormous amounts of energy."
    },
    {
      question: "Which type of nuclear decay releases a helium nucleus?",
      options: ["Alpha decay", "Beta decay", "Gamma decay", "Neutron decay"],
      correct_answer: 0,
      explanation: "Alpha decay releases a helium nucleus (2 protons + 2 neutrons), which is the most massive type of nuclear radiation."
    },
    {
      question: "What does the 'c' represent in Einstein's equation E=mc²?",
      options: ["Charge", "Speed of light", "Constant", "Capacity"],
      correct_answer: 1,
      explanation: "The 'c' represents the speed of light in vacuum, which is approximately 3 × 10⁸ meters per second."
    },
    {
      question: "Nuclear binding energy is highest for which elements?",
      options: ["Light elements", "Medium-mass elements", "Heavy elements", "All elements equally"],
      correct_answer: 1,
      explanation: "Medium-mass elements (around iron-56) have the highest nuclear binding energy per nucleon, making them the most stable."
    },
    {
      question: "What happens during beta decay?",
      options: ["A neutron becomes a proton", "A proton becomes a neutron", "A helium nucleus is emitted", "High-energy photons are released"],
      correct_answer: 0,
      explanation: "During beta decay, a neutron in the nucleus transforms into a proton, releasing an electron and an antineutrino."
    }
  ]

  const demoFeatures = [
    {
      icon: "🧠",
      title: "AI-Powered Analysis",
      description: "Watch as our AI processes video content to extract key concepts, create summaries, and identify important topics."
    },
    {
      icon: "💬",
      title: "Interactive Chat",
      description: "Ask questions about any topic from the video and get intelligent, contextual responses from your AI tutor."
    },
    {
      icon: "📝",
      title: "Smart Summaries",
      description: "Get comprehensive summaries with chapter breakdowns, key points, and learning objectives automatically generated."
    },
    {
      icon: "🎯",
      title: "Adaptive Quizzes",
      description: "Test your knowledge with AI-generated quizzes that adapt to the video content and your learning level."
    },
    {
      icon: "📚",
      title: "Personalized Notes",
      description: "Take notes with AI assistance, organize your thoughts, and build a personal knowledge base."
    },
    {
      icon: "📊",
      title: "Progress Tracking",
      description: "Monitor your learning journey with detailed analytics, insights, and personalized recommendations."
    }
  ]

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
            <ZyndleLogo />
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
      <section className="container mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Experience <span className="text-gradient">Zyndle AI</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed">
            See how our AI transforms learning with this interactive demonstration
          </p>
          
          {/* Demo Navigation */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            {['overview', 'analysis', 'chat', 'quiz', 'notes'].map((tab) => (
              <motion.button
                key={tab}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setActiveDemo(tab)}
                className={`px-6 py-3 rounded-lg font-medium transition-all duration-300 ${
                  activeDemo === tab 
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white' 
                    : 'bg-white/10 backdrop-blur-md border border-white/20 text-gray-300 hover:bg-white/20'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Demo Content */}
        <motion.div
          key={activeDemo}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-6xl mx-auto"
        >
          {activeDemo === 'overview' && (
            <div className="glass-dark rounded-2xl p-8">
              <h2 className="text-3xl font-bold text-center mb-8">Interactive Learning Features</h2>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {demoFeatures.map((feature, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 * index }}
                    whileHover={{ y: -5 }}
                    className="glass-dark rounded-xl p-6 text-center hover:neon-glow transition-all duration-300"
                  >
                    <div className="text-4xl mb-4">{feature.icon}</div>
                    <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                    <p className="text-gray-300 text-sm leading-relaxed">{feature.description}</p>
                  </motion.div>
                ))}
              </div>
              
              <div className="text-center mt-8">
                <p className="text-gray-300 mb-4">Click on any feature above to see it in action!</p>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setActiveDemo('analysis')}
                  className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-300"
                >
                  Start Demo
                </motion.button>
              </div>
            </div>
          )}

          {activeDemo === 'analysis' && (
            <div className="glass-dark rounded-2xl p-8">
              <h2 className="text-3xl font-bold text-center mb-8">AI Video Analysis</h2>
              
              <div className="grid lg:grid-cols-2 gap-8">
                {/* Video Placeholder */}
                <div>
                  <div className="bg-black rounded-lg aspect-video mb-6 flex items-center justify-center overflow-hidden">
                    {demoMode ? (
                      <div className="text-center p-8">
                        <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                          <Play className="w-12 h-12 text-white" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2 text-white">Demo Mode Active</h3>
                        <p className="text-gray-300 mb-4">Experience Zyndle AI features with sample content</p>
                        <div className="flex items-center justify-center space-x-4 text-sm text-gray-400">
                          <span>🎯 AI Analysis</span>
                          <span>💬 Smart Chat</span>
                          <span>📝 Interactive Notes</span>
                        </div>
                      </div>
                    ) : (
                      <div className="text-center">
                        <Play className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                        <p className="text-gray-400">Video Player Placeholder</p>
                      </div>
                    )}
                  </div>
                  
                  <div className="glass-dark rounded-lg p-4">
                    <h4 className="font-semibold mb-2">Video Information</h4>
                    <div className="space-y-2 text-sm">
                      <p><span className="text-gray-400">Title:</span> Nuclear Decay Processes and Energy</p>
                      <p><span className="text-gray-400">Channel:</span> Physics Academy</p>
                      <p><span className="text-gray-400">Duration:</span> 15:32</p>
                      <p><span className="text-gray-400">Views:</span> 125K</p>
                    </div>
                  </div>
                </div>

                {/* Analysis Results */}
                <div>
                  <h3 className="text-xl font-semibold mb-4">AI Analysis Results</h3>
                  
                  <div className="space-y-4">
                    <div className="glass-dark rounded-lg p-4">
                      <h4 className="font-medium text-blue-400 mb-2">Summary</h4>
                      <p className="text-gray-300 text-sm">
                        This video explores nuclear physics fundamentals, covering binding energy, mass defect, 
                        and various decay processes. It explains how nuclear reactions can release energy 
                        according to Einstein's E=mc² equation.
                      </p>
                    </div>
                    
                    <div className="glass-dark rounded-lg p-4">
                      <h4 className="font-medium text-green-400 mb-2">Key Topics</h4>
                      <div className="flex flex-wrap gap-2">
                        {['Nuclear Binding Energy', 'Mass Defect', 'Alpha Decay', 'Beta Decay', 'E=mc²'].map((topic, index) => (
                          <span key={index} className="px-3 py-1 bg-green-500/20 border border-green-500/30 rounded-full text-sm">
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    <div className="glass-dark rounded-lg p-4">
                      <h4 className="font-medium text-purple-400 mb-2">Chapters</h4>
                      <div className="space-y-2">
                        {[
                          { title: "Introduction", time: "0:00", desc: "Overview of nuclear physics" },
                          { title: "Binding Energy", time: "2:15", desc: "Understanding nuclear stability" },
                          { title: "Decay Processes", time: "6:30", desc: "Alpha, beta, and gamma decay" },
                          { title: "Energy Release", time: "11:45", desc: "E=mc² and nuclear power" }
                        ].map((chapter, index) => (
                          <div key={index} className="flex justify-between items-center p-2 rounded hover:bg-white/5">
                            <div>
                              <p className="font-medium">{chapter.title}</p>
                              <p className="text-sm text-gray-400">{chapter.desc}</p>
                            </div>
                            <span className="text-sm text-gray-400">{chapter.time}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeDemo === 'chat' && (
            <div className="glass-dark rounded-2xl p-8">
              <h2 className="text-3xl font-bold text-center mb-8">AI Chat Tutor</h2>
              
              <div className="max-w-4xl mx-auto">
                <div className="glass-dark rounded-lg p-6 mb-6">
                  <h3 className="text-xl font-semibold mb-4">Chat with Your AI Tutor</h3>
                  <p className="text-gray-300 mb-4">
                    Ask questions about nuclear physics, the video content, or any related topics. 
                    The AI will provide contextual, educational responses.
                  </p>
                  
                  {/* Chat History */}
                  <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
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
                      placeholder="Ask about nuclear physics, binding energy, decay processes..."
                      className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                      onClick={handleChat}
                      className="px-6 py-3 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors font-medium"
                    >
                      Send
                    </button>
                  </div>
                </div>
                
                <div className="text-center">
                  <p className="text-gray-300 mb-4">Try asking about: nuclear binding energy, decay processes, or E=mc²</p>
                </div>
              </div>
            </div>
          )}

          {activeDemo === 'quiz' && (
            <div className="glass-dark rounded-2xl p-8">
              <h2 className="text-3xl font-bold text-center mb-8">Interactive Quiz</h2>
              
              <div className="max-w-4xl mx-auto">
                {!quizSubmitted ? (
                  <div>
                    <div className="text-center mb-8">
                      <h3 className="text-xl font-semibold mb-2">Test Your Knowledge</h3>
                      <p className="text-gray-300">
                        Answer these questions about nuclear physics to test your understanding of the video content.
                      </p>
                    </div>
                    
                    <div className="space-y-6">
                      {demoQuizQuestions.map((question, qIndex) => (
                        <div key={qIndex} className="glass-dark rounded-lg p-6">
                          <h4 className="font-medium mb-4 text-lg">
                            {qIndex + 1}. {question.question}
                          </h4>
                          <div className="space-y-3">
                            {question.options.map((option, oIndex) => (
                              <label key={oIndex} className="flex items-center space-x-3 cursor-pointer p-3 rounded-lg hover:bg-white/5 transition-colors">
                                <input
                                  type="radio"
                                  name={`question-${qIndex}`}
                                  checked={quizAnswers[qIndex] === oIndex}
                                  onChange={() => handleQuizAnswer(qIndex, oIndex)}
                                  className="text-blue-500 focus:ring-blue-500"
                                />
                                <span className="text-gray-300">{option}</span>
                              </label>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    <div className="text-center mt-8">
                      <button
                        onClick={submitQuiz}
                        disabled={Object.keys(quizAnswers).length < demoQuizQuestions.length}
                        className="px-8 py-3 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium text-lg"
                      >
                        Submit Quiz
                      </button>
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="text-center mb-8">
                      <h3 className="text-2xl font-semibold mb-4">Quiz Results</h3>
                      <div className="text-5xl font-bold text-blue-500 mb-2">{quizScore}%</div>
                      <p className="text-gray-300 text-lg">
                        You got {Math.round((quizScore / 100) * demoQuizQuestions.length)} out of {demoQuizQuestions.length} questions correct!
                      </p>
                    </div>
                    
                    <div className="space-y-6">
                      {demoQuizQuestions.map((question, qIndex) => (
                        <div key={qIndex} className="glass-dark rounded-lg p-6">
                          <h4 className="font-medium mb-3 text-lg">{qIndex + 1}. {question.question}</h4>
                          <div className="space-y-2 mb-4">
                            {question.options.map((option, oIndex) => (
                              <div
                                key={oIndex}
                                className={`p-3 rounded ${
                                  oIndex === question.correct_answer
                                    ? 'bg-green-500/20 border border-green-500/30'
                                    : oIndex === quizAnswers[qIndex] && oIndex !== question.correct_answer
                                    ? 'bg-red-500/20 border border-red-500/30'
                                    : 'bg-gray-700/50'
                                }`}
                              >
                                {option}
                                {oIndex === question.correct_answer && (
                                  <span className="ml-2 text-green-400">✓ Correct</span>
                                )}
                                {oIndex === quizAnswers[qIndex] && oIndex !== question.correct_answer && (
                                  <span className="ml-2 text-red-400">✗ Your Answer</span>
                                )}
                              </div>
                            ))}
                          </div>
                          <p className="text-sm text-gray-400 bg-gray-800/50 p-3 rounded">
                            <strong>Explanation:</strong> {question.explanation}
                          </p>
                        </div>
                      ))}
                    </div>
                    
                    <div className="text-center mt-8">
                      <button
                        onClick={resetQuiz}
                        className="px-8 py-3 bg-gray-600 rounded-lg hover:bg-gray-700 transition-colors font-medium text-lg"
                      >
                        Take Quiz Again
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeDemo === 'notes' && (
            <div className="glass-dark rounded-2xl p-8">
              <h2 className="text-3xl font-bold text-center mb-8">Smart Notes & Learning</h2>
              
              <div className="max-w-4xl mx-auto">
                <div className="grid lg:grid-cols-2 gap-8">
                  {/* Existing Notes */}
                  <div>
                    <h3 className="text-xl font-semibold mb-4">Your Notes</h3>
                    
                    <div className="space-y-4">
                      {notes.map((note) => (
                        <div key={note.id} className="glass-dark rounded-lg p-4">
                          <h4 className="font-medium mb-2 text-blue-400">{note.title}</h4>
                          <p className="text-gray-300 text-sm mb-3">{note.content}</p>
                          <button
                            onClick={() => deleteNote(note.id)}
                            className="text-red-400 hover:text-red-300 text-sm"
                          >
                            Delete Note
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Add New Note */}
                  <div>
                    <h3 className="text-xl font-semibold mb-4">Add New Note</h3>
                    
                    <div className="glass-dark rounded-lg p-4">
                      <textarea
                        value={newNote}
                        onChange={(e) => setNewNote(e.target.value)}
                        placeholder="Write your thoughts, questions, or key points from the video..."
                        className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        rows="4"
                      ></textarea>
                      
                      <button
                        onClick={saveNote}
                        className="mt-3 w-full py-2 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors font-medium"
                      >
                        Save Note
                      </button>
                    </div>
                    
                    <div className="mt-6 text-center">
                      <p className="text-gray-300 text-sm">
                        Notes are automatically organized by topic and can be exported to your favorite tools.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </section>
    </div>
  )
}

// Progress Dashboard Component
function ProgressDashboard({ onBack }) {
  const [progress, setProgress] = useState(null)
  const [insights, setInsights] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  React.useEffect(() => {
    loadProgressData()
  }, [])

  const loadProgressData = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      
      // Load progress data
      const progressResponse = await authService.authenticatedFetch(`${apiUrl}/progress`)
      const progressData = await progressResponse.json()
      setProgress(progressData)
      
      // Load insights
      const insightsResponse = await authService.authenticatedFetch(`${apiUrl}/progress/insights`)
      const insightsData = await insightsResponse.json()
      setInsights(insightsData)
    } catch (error) {
      console.error('Error loading progress data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-300">Loading your progress...</p>
        </div>
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
            <ZyndleLogo />
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

      {/* Progress Content */}
      <section className="container mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Your Learning <span className="text-gradient">Progress</span>
          </h1>
          <p className="text-xl text-gray-300">
            Track your learning journey and discover insights about your progress
          </p>
        </motion.div>

        {progress && (
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {/* Stats Cards */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="glass-dark rounded-xl p-6 text-center"
            >
              <div className="text-3xl font-bold text-blue-400 mb-2">{progress.total_videos_watched}</div>
              <p className="text-gray-300">Videos Watched</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="glass-dark rounded-xl p-6 text-center"
            >
              <div className="text-3xl font-bold text-green-400 mb-2">{progress.total_quizzes_taken}</div>
              <p className="text-gray-300">Quizzes Taken</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="glass-dark rounded-xl p-6 text-center"
            >
              <div className="text-3xl font-bold text-purple-400 mb-2">{progress.average_quiz_score}%</div>
              <p className="text-gray-300">Average Score</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="glass-dark rounded-xl p-6 text-center"
            >
              <div className="text-3xl font-bold text-yellow-400 mb-2">{progress.learning_streak}</div>
              <p className="text-gray-300">Day Streak</p>
            </motion.div>
          </div>
        )}

        {insights && (
          <div className="grid lg:grid-cols-2 gap-8">
            {/* Learning Insights */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="glass-dark rounded-xl p-6"
            >
              <h3 className="text-xl font-semibold mb-4">Learning Insights</h3>
              
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-blue-400 mb-2">Learning Style</h4>
                  <p className="text-gray-300">{insights.learning_style}</p>
                </div>

                <div>
                  <h4 className="font-medium text-green-400 mb-2">Favorite Topics</h4>
                  <div className="flex flex-wrap gap-2">
                    {insights.favorite_topics.map((topic, index) => (
                      <span key={index} className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full text-sm">
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-yellow-400 mb-2">Areas to Improve</h4>
                  <ul className="text-gray-300 space-y-1">
                    {insights.weak_areas.map((area, index) => (
                      <li key={index}>• {area}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </motion.div>

            {/* Recommendations */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="glass-dark rounded-xl p-6"
            >
              <h3 className="text-xl font-semibold mb-4">Recommendations</h3>
              
              <div className="space-y-3">
                {insights.recommendations.map((recommendation, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-300">{recommendation}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        )}

        {/* Recent Activity */}
        {progress && progress.recent_activity && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="mt-12"
          >
            <h3 className="text-2xl font-semibold mb-6 text-center">Recent Activity</h3>
            
            <div className="glass-dark rounded-xl p-6">
              <div className="space-y-4">
                {progress.recent_activity.map((activity, index) => (
                  <div key={index} className="flex items-center space-x-4 p-3 rounded-lg bg-white/5">
                    <div className={`w-3 h-3 rounded-full ${
                      activity.type === 'video_watched' ? 'bg-blue-400' : 'bg-green-400'
                    }`}></div>
                    <div className="flex-1">
                      <p className="text-gray-300">{activity.description}</p>
                      <p className="text-sm text-gray-500">
                        {new Date(activity.date).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </section>
    </div>
  )
}

export default App
