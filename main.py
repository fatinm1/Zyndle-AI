#!/usr/bin/env python3
"""
Zyndle AI - Main Entry Point
This file helps Railway/Nixpacks detect this as a Python project.
The actual application is in the backend/ directory.
"""

import os
import sys
import subprocess

def main():
    """Redirect to the backend main.py"""
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    backend_main = os.path.join(backend_dir, 'main.py')
    
    if os.path.exists(backend_main):
        # Change to backend directory and run main.py
        os.chdir(backend_dir)
        subprocess.run([sys.executable, 'main.py'])
    else:
        print("Error: backend/main.py not found!")
        sys.exit(1)

if __name__ == "__main__":
    main() 