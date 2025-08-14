# 🗄️ PostgreSQL Setup Guide for Zyndle AI

## Overview
This guide will help you set up PostgreSQL for your Zyndle AI application on Railway, replacing the current SQLite database.

## 🚀 Quick Setup on Railway

### 1. Add PostgreSQL Service
1. Go to your Railway project dashboard
2. Click "New Service" → "Database" → "PostgreSQL"
3. Wait for the service to be created
4. Copy the `DATABASE_URL` from the PostgreSQL service variables

### 2. Update Environment Variables
Add these environment variables to your backend service:
```
DATABASE_URL=postgresql://username:password@host:port/database
```

### 3. Deploy the Updated Backend
The backend will automatically:
- Connect to PostgreSQL using the `DATABASE_URL`
- Create all necessary tables on first run
- Use connection pooling for better performance

## 🔧 Manual Setup (Alternative)

### Option 1: Local PostgreSQL
```bash
# Install PostgreSQL
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/

# Create database
sudo -u postgres psql
CREATE DATABASE zyndle_ai;
CREATE USER zyndle_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE zyndle_ai TO zyndle_user;
\q
```

### Option 2: Docker PostgreSQL
```bash
docker run --name zyndle-postgres \
  -e POSTGRES_DB=zyndle_ai \
  -e POSTGRES_USER=zyndle_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:15
```

## 📊 Database Schema

The application will automatically create these tables:

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `full_name`: User's full name
- `hashed_password`: Encrypted password
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Video Analyses Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `video_id`: YouTube video ID
- `title`: Video title
- `channel`: Channel name
- `duration`: Video duration
- `summary`: AI-generated summary
- `transcript`: Video transcript
- `chapters`: JSON array of video chapters

### Chat Sessions Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `video_id`: Associated video
- `question`: User's question
- `answer`: AI response
- `sources`: JSON array of sources
- `confidence`: AI confidence level

### Quiz Sessions Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `video_id`: Associated video
- `questions`: JSON array of quiz questions
- `user_answers`: JSON array of user answers
- `score`: Quiz score

### Notes Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `video_id`: Associated video
- `title`: Note title
- `content`: Note content
- `created_at`, `updated_at`: Timestamps

## 🔍 Testing the Setup

### 1. Check Database Connection
```bash
cd backend
python setup_postgresql.py
```

### 2. Verify Tables Created
```bash
# Connect to PostgreSQL
psql $DATABASE_URL

# List tables
\dt

# Check table structure
\d users
\d video_analyses
```

### 3. Test API Endpoints
```bash
# Health check
curl https://your-app.railway.app/health

# Detailed health check
curl https://your-app.railway.app/health/detailed
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Connection Refused
- Check if PostgreSQL service is running
- Verify `DATABASE_URL` format
- Ensure firewall allows connections

#### 2. Authentication Failed
- Verify username/password in `DATABASE_URL`
- Check user permissions
- Ensure database exists

#### 3. Table Creation Failed
- Check user has CREATE privileges
- Verify database exists and is accessible
- Check for syntax errors in models

### Debug Commands
```bash
# Check environment variables
echo $DATABASE_URL

# Test connection manually
python -c "
from models.database import engine
with engine.connect() as conn:
    result = conn.execute('SELECT version()')
    print('Connected:', result.fetchone()[0])
"

# Check logs
railway logs
```

## 📈 Performance Optimization

### Connection Pooling
- Pool size: 5 connections
- Max overflow: 10 connections
- Pool recycle: 300 seconds
- Pool pre-ping: Enabled

### Indexes
The following indexes are automatically created:
- `users.email` (unique)
- `video_analyses.video_id` (unique)
- `video_analyses.user_id`
- `chat_sessions.user_id`
- `quiz_sessions.user_id`
- `notes.user_id`

## 🔒 Security Considerations

### Environment Variables
- Never commit `DATABASE_URL` to version control
- Use Railway's built-in environment variable management
- Rotate passwords regularly

### Database Access
- Use least privilege principle
- Limit database user permissions
- Enable SSL connections in production

## 📚 Additional Resources

- [Railway PostgreSQL Documentation](https://docs.railway.app/databases/postgresql)
- [SQLAlchemy PostgreSQL Guide](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html)
- [PostgreSQL Best Practices](https://www.postgresql.org/docs/current/admin.html)

## 🎯 Next Steps

After setting up PostgreSQL:
1. Test all API endpoints
2. Verify data persistence
3. Monitor database performance
4. Set up database backups
5. Configure monitoring and alerts
