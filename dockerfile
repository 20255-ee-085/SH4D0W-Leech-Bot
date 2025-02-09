# Base image
FROM python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create secure application user
RUN useradd -m -u 1001 -s /bin/sh shadowbot

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set ownership and permissions
RUN chown -R shadowbot:shadowbot /app \
    && chmod 755 /app \
    && chmod +x /app/start.sh

# Switch to non-root user
USER shadowbot

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DOWNLOAD_DIR=/app/downloads \
    TEMP_DIR=/app/temp \
    LOG_DIR=/app/logs

# Create volume for persistent storage
VOLUME ["/app/downloads", "/app/logs"]

# Entrypoint
ENTRYPOINT ["./start.sh"]