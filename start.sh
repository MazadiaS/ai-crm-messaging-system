#!/bin/sh
set -e

echo "=== START SCRIPT RUNNING ==="
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la
echo "PORT environment variable: ${PORT}"

# Use PORT from environment, default to 8000 if not set
PORT=${PORT:-8000}

echo "Starting uvicorn on port $PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
