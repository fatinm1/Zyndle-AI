import React from 'react'

const ZyndleLogo = ({ size = 40, className = "" }) => {
  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      <svg 
        width={size} 
        height={size} 
        viewBox="0 0 100 100" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Four blade-like shapes arranged in a circle */}
        {/* Top-right blade */}
        <path 
          d="M50 50 L75 25 L85 30 L60 55 Z" 
          fill="url(#gradient1)"
        />
        
        {/* Bottom-right blade */}
        <path 
          d="M50 50 L75 75 L70 85 L45 60 Z" 
          fill="url(#gradient2)"
        />
        
        {/* Bottom-left blade */}
        <path 
          d="M50 50 L25 75 L15 70 L40 45 Z" 
          fill="url(#gradient3)"
        />
        
        {/* Top-left blade */}
        <path 
          d="M50 50 L25 25 L30 15 L55 40 Z" 
          fill="url(#gradient4)"
        />
        
        {/* Central Z */}
        <path 
          d="M32 28 L68 28 L42 42 L58 42 L32 56 L68 56" 
          stroke="#00D4FF" 
          strokeWidth="3.5" 
          strokeLinecap="round" 
          strokeLinejoin="round"
          fill="none"
        />
        
        {/* Gradients for the blades */}
        <defs>
          <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00D4FF" />
            <stop offset="100%" stopColor="#1E3A8A" />
          </linearGradient>
          <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00D4FF" />
            <stop offset="100%" stopColor="#1E3A8A" />
          </linearGradient>
          <linearGradient id="gradient3" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00D4FF" />
            <stop offset="100%" stopColor="#1E3A8A" />
          </linearGradient>
          <linearGradient id="gradient4" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00D4FF" />
            <stop offset="100%" stopColor="#1E3A8A" />
          </linearGradient>
        </defs>
      </svg>
      <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
        Zyndle AI
      </span>
    </div>
  )
}

export default ZyndleLogo