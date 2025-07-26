#!/usr/bin/env python3
"""
Startup script for Zyndle AI Backend
This script handles proper application startup and health checks
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def main():
    """Main startup function"""
    print("🚀 Starting Zyndle AI Backend...")
    
    # Set default port
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"📡 Server will run on {host}:{port}")
    print(f"🌍 Environment: {os.getenv('RAILWAY_ENVIRONMENT', 'development')}")
    
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️ Warning: Missing environment variables: {missing_vars}")
        print("Some features may not work properly")
    
    # Start the server
    try:
        uvicorn.run(
            "backend.main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 