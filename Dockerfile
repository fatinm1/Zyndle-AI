# Use Python base image
FROM python:3.11-slim

# Install Node.js and npm for frontend build
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package.json files first for better caching
COPY package.json ./
COPY frontend/package.json ./frontend/

# Install Node.js dependencies (without running postinstall scripts)
RUN npm install --ignore-scripts
RUN cd frontend && npm install --ignore-scripts

# Copy the frontend source code
COPY frontend/ ./frontend/

# Build the frontend
RUN cd frontend && npm run build

# Copy requirements and install Python dependencies
COPY backend/requirements-deploy.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ ./backend/

# Set working directory to backend
WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Start the application
CMD ["python", "start.py"] 