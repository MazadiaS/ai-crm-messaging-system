FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from backend directory
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from backend directory
COPY backend/ .

# Copy startup script
COPY start.sh .
RUN chmod +x start.sh

# Expose port (Railway uses $PORT env var)
EXPOSE 8000

# Start the application using the startup script
CMD ["./start.sh"]
