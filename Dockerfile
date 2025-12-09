# ============================
# Stage 1: Build Frontend
# ============================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build the React app
RUN npm run build

# ============================
# Stage 2: Python Backend
# ============================
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/backend/static ./backend/static

# Set working directory to backend
WORKDIR /app/backend

# Environment variables
ENV FLASK_PORT=5000
ENV FLASK_DEBUG=False

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
