#!/usr/bin/env python3
"""
Simple test script to verify deployment functionality
"""

import requests
import time
import sys

def test_endpoints(base_url):
    """Test basic endpoints"""
    endpoints = [
        "/",
        "/ping", 
        "/health",
        "/api/health"
    ]
    
    print(f"Testing endpoints at {base_url}")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint}: {response.status_code}")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    print("🧪 Testing Zyndle AI API endpoints...")
    test_endpoints(base_url)
