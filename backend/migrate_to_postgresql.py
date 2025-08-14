#!/usr/bin/env python3
"""
Migration Script: SQLite to PostgreSQL
This script helps migrate existing data from SQLite to PostgreSQL
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def migrate_sqlite_to_postgresql():
    """Migrate data from SQLite to PostgreSQL"""
    print("🔄 Starting migration from SQLite to PostgreSQL...")
    
    try:
        # Check if we have both databases configured
        from models.database import engine, SessionLocal, Base
        
        # Check current database type
        current_db_url = str(engine.url)
        if "sqlite" not in current_db_url:
            print("✅ Already using PostgreSQL, no migration needed")
            return True
        
        print("⚠️ Currently using SQLite, checking for PostgreSQL configuration...")
        
        # Check for PostgreSQL environment variables
        pg_url = os.getenv('DATABASE_URL')
        if not pg_url or not pg_url.startswith('postgresql://'):
            print("❌ PostgreSQL DATABASE_URL not found")
            print("Please set DATABASE_URL to a PostgreSQL connection string")
            return False
        
        print("✅ PostgreSQL URL found, setting up migration...")
        
        # Create PostgreSQL engine
        from sqlalchemy import create_engine as create_pg_engine
        pg_engine = create_pg_engine(pg_url)
        
        # Test PostgreSQL connection
        with pg_engine.connect() as conn:
            result = conn.execute("SELECT version()")
            version = result.fetchone()[0]
            print(f"✅ PostgreSQL connected: {version.split(',')[0]}")
        
        # Create tables in PostgreSQL
        print("🔨 Creating tables in PostgreSQL...")
        Base.metadata.create_all(bind=pg_engine)
        print("✅ Tables created in PostgreSQL")
        
        # Here you would add data migration logic
        # For now, just create the tables
        print("💡 Tables created successfully!")
        print("💡 To migrate data, you'll need to:")
        print("   1. Export data from SQLite")
        print("   2. Import data to PostgreSQL")
        print("   3. Update your DATABASE_URL")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def check_migration_status():
    """Check if migration is needed and possible"""
    print("🔍 Checking migration status...")
    
    try:
        from models.database import engine
        current_db = str(engine.url)
        
        if "postgresql" in current_db:
            print("✅ Using PostgreSQL - no migration needed")
            return "postgresql"
        elif "sqlite" in current_db:
            print("⚠️ Using SQLite - migration to PostgreSQL recommended")
            return "sqlite"
        else:
            print("❓ Unknown database type")
            return "unknown"
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return "error"

if __name__ == "__main__":
    load_dotenv()
    
    status = check_migration_status()
    
    if status == "sqlite":
        print("\n🚀 Starting migration process...")
        success = migrate_sqlite_to_postgresql()
        if success:
            print("\n🎉 Migration setup completed!")
            print("Next steps:")
            print("1. Set DATABASE_URL to your PostgreSQL connection string")
            print("2. Restart your application")
            print("3. Verify data is accessible")
        else:
            print("\n❌ Migration failed")
            sys.exit(1)
    elif status == "postgresql":
        print("\n✅ Already using PostgreSQL!")
    else:
        print("\n❌ Cannot determine database status")
        sys.exit(1)
