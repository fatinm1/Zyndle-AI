#!/bin/bash

# Zyndle AI Backend Dependencies Installation Script
# This script installs system dependencies required for video processing

echo "🔧 Installing Zyndle AI Backend Dependencies..."

# Detect operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "📦 Detected Linux system"
    
    # Update package list
    sudo apt-get update
    
    # Install FFmpeg and other dependencies
    sudo apt-get install -y ffmpeg python3-pip python3-venv
    
    echo "✅ Linux dependencies installed successfully!"
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "🍎 Detected macOS system"
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    # Install FFmpeg
    brew install ffmpeg
    
    echo "✅ macOS dependencies installed successfully!"
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash, Cygwin, etc.)
    echo "🪟 Detected Windows system"
    echo "⚠️  For Windows, please install FFmpeg manually:"
    echo "   1. Download FFmpeg from: https://ffmpeg.org/download.html"
    echo "   2. Extract to a folder (e.g., C:\\ffmpeg)"
    echo "   3. Add the bin folder to your PATH environment variable"
    echo "   4. Restart your terminal"
    
else
    echo "❓ Unknown operating system: $OSTYPE"
    echo "Please install FFmpeg manually for your system."
fi

echo ""
echo "📋 Next steps:"
echo "1. Create a virtual environment: python -m venv venv"
echo "2. Activate the virtual environment:"
echo "   - Windows: venv\\Scripts\\activate"
echo "   - macOS/Linux: source venv/bin/activate"
echo "3. Install Python dependencies: pip install -r requirements.txt"
echo "4. Set up environment variables in .env file"
echo ""
echo "🎉 Setup complete! You can now run the backend server." 