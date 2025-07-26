# Use Python base image
FROM python:3.11-slim

# Install Node.js and npm in a single layer to reduce size
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements-deploy.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json and install Node.js dependencies
COPY package.json .
COPY frontend/package.json ./frontend/

# Install Node.js dependencies
RUN npm install
RUN cd frontend && npm install

# Copy the rest of the application
COPY . .

# Build frontend
RUN cd frontend && npm run build

# Expose port
EXPOSE 8000

# Start the application
CMD ["python", "backend/start.py"] 