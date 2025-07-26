@echo off
REM Zyndle AI Backend Dependencies Installation Script for Windows

echo 🔧 Installing Zyndle AI Backend Dependencies for Windows...

echo.
echo 📋 Prerequisites:
echo 1. Make sure you have Python 3.8+ installed
echo 2. Make sure you have FFmpeg installed and added to PATH
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ❌ FFmpeg not found in PATH
    echo.
    echo 📥 Please install FFmpeg:
    echo 1. Download from: https://ffmpeg.org/download.html
    echo 2. Extract to a folder (e.g., C:\ffmpeg)
    echo 3. Add the bin folder to your PATH environment variable
    echo 4. Restart this command prompt
    echo.
    pause
    exit /b 1
)

echo ✅ FFmpeg found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Python dependencies installed successfully!

echo.
echo 📋 Next steps:
echo 1. Create a .env file with your API keys
echo 2. Run the backend: python main.py
echo.
echo 🎉 Setup complete! You can now run the backend server.
pause 