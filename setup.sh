#!/bin/bash

# AI CRM Messaging System - Quick Setup Script

set -e

echo "====================================="
echo "AI CRM Messaging System - Setup"
echo "====================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose found"
echo ""

# Check for API key
if [ ! -f "backend/.env" ]; then
    echo "Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo ""
    echo "⚠️  IMPORTANT: You need to add your Anthropic API key!"
    echo "   Edit backend/.env and set ANTHROPIC_API_KEY"
    echo "   Get your key at: https://console.anthropic.com/"
    echo ""
    read -p "Press Enter after you've added your API key..."
fi

if [ ! -f "frontend/.env" ]; then
    echo "Creating frontend/.env from template..."
    cp frontend/.env.example frontend/.env
fi

echo ""
echo "Starting services with Docker Compose..."
docker-compose up -d

echo ""
echo "Waiting for services to initialize (30 seconds)..."
sleep 30

echo ""
echo "Running database migrations..."
docker-compose exec -T backend alembic upgrade head

echo ""
echo "Seeding database with demo data..."
docker-compose exec -T backend python seed_data.py

echo ""
echo "====================================="
echo "✅ Setup Complete!"
echo "====================================="
echo ""
echo "Access the application:"
echo "  Frontend:  http://localhost:5173"
echo "  API Docs:  http://localhost:8000/api/docs"
echo "  ReDoc:     http://localhost:8000/api/redoc"
echo ""
echo "Login credentials:"
echo "  Admin:   admin@crowe.uz / password123"
echo "  Manager: manager@crowe.uz / password123"
echo "  Viewer:  viewer@crowe.uz / password123"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop services:    docker-compose down"
echo "  Restart services: docker-compose restart"
echo ""
echo "Happy coding! 🚀"
