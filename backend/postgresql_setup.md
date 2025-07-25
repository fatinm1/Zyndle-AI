# PostgreSQL Setup Guide for Zyndle AI

## Prerequisites
- Windows 10/11
- Administrator privileges

## Step 1: Install PostgreSQL

### Download and Install:
1. Go to: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Download PostgreSQL 15 or 16 for Windows x64
3. Run the installer as Administrator
4. Follow the installation wizard

### Installation Settings:
- **Installation Directory**: `C:\Program Files\PostgreSQL\15` (default)
- **Data Directory**: `C:\Program Files\PostgreSQL\15\data` (default)
- **Password**: Set a strong password for the `postgres` user (remember this!)
- **Port**: 5432 (default)
- **Locale**: Use default

## Step 2: Add PostgreSQL to PATH

After installation, add PostgreSQL to your system PATH:
1. Open System Properties → Advanced → Environment Variables
2. Edit the "Path" variable
3. Add: `C:\Program Files\PostgreSQL\15\bin`
4. Click OK to save

## Step 3: Create Database and User

### Option A: Using pgAdmin (GUI)
1. Open pgAdmin 4
2. Connect to PostgreSQL server
3. Right-click on "Login/Group Roles" → Create → Login/Group Role
4. Create user `zyndle_user` with password `zyndle_password_2024`
5. Right-click on "Databases" → Create → Database
6. Create database `zyndle_ai` with owner `zyndle_user`

### Option B: Using Command Line
1. Open Command Prompt as Administrator
2. Navigate to PostgreSQL bin directory:
   ```cmd
   cd "C:\Program Files\PostgreSQL\15\bin"
   ```
3. Run the setup script:
   ```cmd
   psql -U postgres -f "C:\Users\GAMER\LearnWise_AI\backend\setup_postgresql.sql"
   ```

## Step 4: Configure Environment Variables

Create a `.env` file in the `backend` directory with:

```env
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://zyndle_user:zyndle_password_2024@localhost:5432/zyndle_ai

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# YouTube Data API Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here

# JWT Secret Key (change this in production!)
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## Step 5: Test the Connection

After setup, test the connection:

```bash
# In the backend directory
python -c "
from models.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT version()'))
    print('PostgreSQL connected successfully!')
    print(result.fetchone()[0])
"
```

## Step 6: Start the Application

```bash
# In the backend directory
python main.py
```

## Troubleshooting

### Common Issues:

1. **"psql is not recognized"**
   - Add PostgreSQL bin directory to PATH
   - Restart Command Prompt

2. **"Connection refused"**
   - Check if PostgreSQL service is running
   - Verify port 5432 is not blocked by firewall

3. **"Authentication failed"**
   - Verify username/password in DATABASE_URL
   - Check if user exists in PostgreSQL

4. **"Database does not exist"**
   - Run the setup script to create database
   - Verify database name in DATABASE_URL

### Useful Commands:

```bash
# Check PostgreSQL service status
sc query postgresql-x64-15

# Start PostgreSQL service
net start postgresql-x64-15

# Stop PostgreSQL service
net stop postgresql-x64-15

# Connect to PostgreSQL
psql -U postgres -d postgres

# List databases
\l

# List users
\du
```

## Security Notes

- Change the default password in production
- Use environment variables for sensitive data
- Consider using connection pooling for production
- Regularly backup your database 