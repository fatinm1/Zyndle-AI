#!/usr/bin/env python3
"""
Zyndle AI - Main Entry Point
This file serves both the backend API and frontend static files.
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def build_frontend():
    """Build the frontend if not already built"""
    frontend_dir = Path("frontend")
    dist_dir = frontend_dir / "dist"
    
    if not dist_dir.exists():
        print("Building frontend...")
        try:
            # Install frontend dependencies
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            # Build frontend
            subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
            print("Frontend built successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error building frontend: {e}")
            return False
    return True

def start_backend():
    """Start the backend server"""
    backend_dir = Path("backend")
    backend_main = backend_dir / "main.py"
    
    if backend_main.exists():
        print("Starting backend server...")
        os.chdir(backend_dir)
        subprocess.run([sys.executable, "main.py"])
    else:
        print("Error: backend/main.py not found!")
        sys.exit(1)

def main():
    """Main entry point - build frontend and start backend"""
    print("Zyndle AI - Starting application...")
    
    # Build frontend first
    if not build_frontend():
        print("Failed to build frontend, starting backend only...")
    
    # Start backend (which will also serve frontend static files)
    start_backend()

if __name__ == "__main__":
    main() 