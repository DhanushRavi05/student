# Production Dockerfile for EduBehavior AI Academic Portal
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose web port
EXPOSE 5000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Start server using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "app:app"]
