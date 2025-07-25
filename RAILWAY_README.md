# Zyndle AI - Railway Deployment

This is a full-stack application with:
- **Backend**: FastAPI (Python) in `/backend` directory
- **Frontend**: React (Node.js) in `/frontend` directory

## Railway Deployment

### Backend Service
- **Root Directory**: `/backend`
- **Start Command**: `python main.py`
- **Port**: `8000` (set via `PORT` environment variable)

### Frontend Service (Separate Deployment)
- **Root Directory**: `/frontend`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm run preview` or serve `dist` folder

## Environment Variables

### Backend Required Variables:
```env
DATABASE_URL=postgresql://username:password@host:port/database
OPENAI_API_KEY=your_openai_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
PORT=8000
DEBUG=False
ALLOWED_ORIGINS=https://your-frontend-domain.railway.app
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### Frontend Required Variables:
```env
VITE_API_URL=https://your-backend-name.railway.app
```

## Project Structure
```
/
├── backend/           # FastAPI backend
│   ├── main.py       # Main application
│   ├── requirements.txt
│   └── ...
├── frontend/          # React frontend
│   ├── package.json
│   ├── src/
│   └── ...
├── railway.json       # Railway configuration
├── nixpacks.toml      # Nixpacks configuration
└── Procfile          # Process definition
``` 