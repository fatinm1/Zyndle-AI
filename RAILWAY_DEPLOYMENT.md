# Railway Deployment Guide for Zyndle AI

This guide will help you deploy your Zyndle AI project (frontend, backend, and database) to Railway.

## 🚀 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Environment Variables**: Prepare your API keys

## 📋 Step-by-Step Deployment

### Step 1: Connect GitHub Repository

1. **Login to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `Zyndle-AI` repository

### Step 2: Add PostgreSQL Database

1. **Add Database Service**
   - In your Railway project, click "New Service"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically provision a PostgreSQL database

2. **Get Database URL**
   - Click on the PostgreSQL service
   - Go to "Connect" tab
   - Copy the "Postgres Connection URL"

### Step 3: Configure Environment Variables

1. **Go to Variables Tab**
   - In your main service, click "Variables"

2. **Add Required Variables**
   ```env
   # Database (Railway will provide this)
   DATABASE_URL=postgresql://username:password@host:port/database
   
   # OpenAI API
   OPENAI_API_KEY=your_openai_api_key_here
   
   # YouTube Data API
   YOUTUBE_API_KEY=your_youtube_api_key_here
   
   # JWT Secret (generate a strong random string)
   SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
   
   # Server Configuration
   PORT=8000
   DEBUG=False
   
   # CORS Configuration
   ALLOWED_ORIGINS=https://your-frontend-domain.railway.app
   
   # Vector Database
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   ```

### Step 4: Deploy Backend

1. **Railway will automatically detect and deploy your backend**
   - It will use the `railway.json` configuration
   - The backend will be available at: `https://your-backend-name.railway.app`

2. **Check Deployment**
   - Visit your backend URL + `/health` to verify it's working
   - Example: `https://your-backend-name.railway.app/health`

### Step 5: Deploy Frontend

1. **Create Frontend Service**
   - Click "New Service" → "GitHub Repo"
   - Select the same repository
   - Set the root directory to `frontend`

2. **Configure Frontend Build**
   - Add these environment variables to the frontend service:
   ```env
   VITE_API_URL=https://your-backend-name.railway.app
   ```

3. **Build Configuration**
   - Railway will automatically detect it's a Vite/React project
   - It will run `npm install` and `npm run build`
   - The frontend will be served from the `dist` folder

### Step 6: Connect Services

1. **Link Database to Backend**
   - In your backend service, go to "Variables"
   - Add the PostgreSQL connection URL from Step 2

2. **Link Frontend to Backend**
   - Make sure `VITE_API_URL` points to your backend URL

## 🔧 Configuration Files

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python backend/main.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Procfile
```
web: python backend/main.py
```

## 🌐 Custom Domains

1. **Add Custom Domain**
   - Go to your service settings
   - Click "Domains"
   - Add your custom domain

2. **Update CORS Settings**
   - Add your custom domain to `ALLOWED_ORIGINS` in backend variables

## 📊 Monitoring

1. **View Logs**
   - Click on any service to view real-time logs
   - Monitor for errors and performance

2. **Metrics**
   - Railway provides basic metrics for your services
   - Monitor CPU, memory, and network usage

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit sensitive data to Git
   - Use Railway's environment variables for all secrets

2. **Database Security**
   - Railway automatically secures your PostgreSQL database
   - Use strong passwords and limit access

3. **CORS Configuration**
   - Only allow necessary origins
   - Update `ALLOWED_ORIGINS` for production

## 🚨 Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check the build logs in Railway
   - Ensure all dependencies are in `requirements.txt` and `package.json`

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is correct
   - Check if the database service is running

3. **CORS Errors**
   - Update `ALLOWED_ORIGINS` to include your frontend domain
   - Check browser console for CORS errors

4. **Environment Variables**
   - Ensure all required variables are set
   - Check variable names match your code

### Useful Commands:

```bash
# Check Railway CLI (if installed)
railway status

# View logs
railway logs

# Open Railway dashboard
railway open
```

## 🎉 Success!

Once deployed, your Zyndle AI application will be available at:
- **Frontend**: `https://your-frontend-name.railway.app`
- **Backend API**: `https://your-backend-name.railway.app`
- **API Documentation**: `https://your-backend-name.railway.app/docs`

## 📞 Support

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: Report bugs in your repository

---

**Your Zyndle AI application is now live on Railway!** 🚀 