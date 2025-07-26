import React from 'react'

const ZyndleLogo = ({ size = 48, className = "" }) => {
  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      <svg 
        width={size} 
        height={size} 
        viewBox="0 0 100 100" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Background glow effect */}
        <defs>
          <radialGradient id="glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#00D4FF" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#00D4FF" stopOpacity="0" />
          </radialGradient>
          
          {/* Gradient for the main Z */}
          <linearGradient id="zGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00D4FF" />
            <stop offset="50%" stopColor="#60A5FA" />
            <stop offset="100%" stopColor="#A78BFA" />
          </linearGradient>
          
          {/* Gradient for particles */}
          <linearGradient id="particleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00D4FF" />
            <stop offset="100%" stopColor="#1E3A8A" />
          </linearGradient>
        </defs>

        {/* Background glow */}
        <circle cx="50" cy="50" r="45" fill="url(#glow)" />
        
        {/* Main stylized Z */}
        <path 
          d="M25 25 L75 25 L35 45 L65 45 L25 65 L75 65" 
          stroke="url(#zGradient)" 
          strokeWidth="4" 
          strokeLinecap="round" 
          strokeLinejoin="round"
          fill="none"
          filter="drop-shadow(0 0 8px #00D4FF)"
        />
        
        {/* Floating particles around the Z */}
        {/* Top particles */}
        <circle cx="20" cy="15" r="2" fill="url(#particleGradient)" opacity="0.8">
          <animate attributeName="opacity" values="0.8;0.3;0.8" dur="2s" repeatCount="indefinite" />
        </circle>
        <circle cx="80" cy="20" r="1.5" fill="url(#particleGradient)" opacity="0.6">
          <animate attributeName="opacity" values="0.6;0.2;0.6" dur="1.5s" repeatCount="indefinite" />
        </circle>
        
        {/* Middle particles */}
        <circle cx="15" cy="50" r="1.8" fill="url(#particleGradient)" opacity="0.7">
          <animate attributeName="opacity" values="0.7;0.4;0.7" dur="2.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="85" cy="55" r="1.2" fill="url(#particleGradient)" opacity="0.5">
          <animate attributeName="opacity" values="0.5;0.1;0.5" dur="1.8s" repeatCount="indefinite" />
        </circle>
        
        {/* Bottom particles */}
        <circle cx="25" cy="80" r="1.5" fill="url(#particleGradient)" opacity="0.6">
          <animate attributeName="opacity" values="0.6;0.3;0.6" dur="2.2s" repeatCount="indefinite" />
        </circle>
        <circle cx="75" cy="85" r="2.2" fill="url(#particleGradient)" opacity="0.8">
          <animate attributeName="opacity" values="0.8;0.4;0.8" dur="1.7s" repeatCount="indefinite" />
        </circle>
        
        {/* Corner accent particles */}
        <circle cx="10" cy="10" r="1" fill="#00D4FF" opacity="0.4">
          <animate attributeName="opacity" values="0.4;0.1;0.4" dur="3s" repeatCount="indefinite" />
        </circle>
        <circle cx="90" cy="10" r="1" fill="#00D4FF" opacity="0.4">
          <animate attributeName="opacity" values="0.4;0.1;0.4" dur="2.8s" repeatCount="indefinite" />
        </circle>
        <circle cx="10" cy="90" r="1" fill="#00D4FF" opacity="0.4">
          <animate attributeName="opacity" values="0.4;0.1;0.4" dur="2.6s" repeatCount="indefinite" />
        </circle>
        <circle cx="90" cy="90" r="1" fill="#00D4FF" opacity="0.4">
          <animate attributeName="opacity" values="0.4;0.1;0.4" dur="3.2s" repeatCount="indefinite" />
        </circle>
        
        {/* Energy lines connecting some particles */}
        <path 
          d="M20 15 L35 45" 
          stroke="#00D4FF" 
          strokeWidth="0.5" 
          opacity="0.3"
        />
        <path 
          d="M80 20 L65 45" 
          stroke="#00D4FF" 
          strokeWidth="0.5" 
          opacity="0.3"
        />
        <path 
          d="M25 80 L35 45" 
          stroke="#00D4FF" 
          strokeWidth="0.5" 
          opacity="0.3"
        />
        <path 
          d="M75 85 L65 45" 
          stroke="#00D4FF" 
          strokeWidth="0.5" 
          opacity="0.3"
        />
      </svg>
      <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
        Zyndle AI
      </span>
    </div>
  )
}

export default ZyndleLogo