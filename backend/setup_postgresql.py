#!/usr/bin/env python3
"""
PostgreSQL Setup Script for Zyndle AI
This script sets up the PostgreSQL database and creates all necessary tables
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def setup_postgresql():
    """Set up PostgreSQL database and tables"""
    print("🚀 Setting up PostgreSQL database for Zyndle AI...")
    
    try:
        # Import database models
        from models.database import create_tables, engine, Base
        
        # Test database connection
        print("🔍 Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute("SELECT version()")
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
        
        # Create all tables
        print("🔨 Creating database tables...")
        create_tables()
        print("✅ All tables created successfully!")
        
        # Verify tables exist
        print("🔍 Verifying table creation...")
        with engine.connect() as conn:
            result = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = [row[0] for row in result.fetchall()]
            print(f"✅ Tables found: {', '.join(tables)}")
        
        print("🎉 PostgreSQL setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up PostgreSQL: {e}")
        return False

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = ['DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the setup")
        return False
    
    print("✅ All required environment variables are set")
    return True

if __name__ == "__main__":
    load_dotenv()
    
    if not check_environment():
        sys.exit(1)
    
    success = setup_postgresql()
    if not success:
        sys.exit(1)
