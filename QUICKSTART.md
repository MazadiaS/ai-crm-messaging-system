# Quick Start Guide

Get the AI CRM Messaging System running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Anthropic API key ([Get one free](https://console.anthropic.com/))

## Step-by-Step Setup

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd ai-crm-messaging-system
```

### 2. Configure Backend Environment
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit the file
nano backend/.env  # or use your preferred editor
```

**Required: Add your Anthropic API key:**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

The other default values are fine for local development.

### 3. Configure Frontend Environment (Optional)
```bash
cp frontend/.env.example frontend/.env
```

Default values work out of the box for local development.

### 4. Start All Services
```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Celery Workers
- Frontend (port 5173)

### 5. Seed Demo Data
```bash
# Wait ~30 seconds for services to be ready, then:
docker-compose exec backend python seed_data.py
```

This creates:
- 3 demo users (admin, manager, viewer)
- 11 sample contacts
- 7 sample messages
- 3 campaigns
- 5 templates

## Access the Application

### Frontend
Open: **http://localhost:5173**

### API Documentation
Open: **http://localhost:8000/api/docs** (Swagger UI)
Or: **http://localhost:8000/api/redoc** (ReDoc)

### Login Credentials

**Admin Account:**
- Email: `admin@crowe.uz`
- Password: `password123`

**Manager Account:**
- Email: `manager@crowe.uz`
- Password: `password123`

**Viewer Account:**
- Email: `viewer@crowe.uz`
- Password: `password123`

## Quick Test - Generate AI Message

### Using API Docs (Easiest)

1. Go to http://localhost:8000/api/docs
2. Click "Authorize" and login with admin credentials
3. Try `POST /api/messages/generate`:

```json
{
  "contact_id": "get-from-contacts-list",
  "occasion_type": "birthday",
  "custom_context": "celebrating 10 years partnership",
  "tone": "professional_friendly"
}
```

### Using curl

```bash
# First, login to get token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@crowe.uz","password":"password123"}' \
  | jq -r '.access_token')

# Get a contact ID
CONTACT_ID=$(curl http://localhost:8000/api/contacts?limit=1 \
  -H "Authorization: Bearer $TOKEN" \
  | jq -r '.items[0].id')

# Generate message
curl -X POST http://localhost:8000/api/messages/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"contact_id\": \"$CONTACT_ID\",
    \"occasion_type\": \"birthday\",
    \"tone\": \"professional_friendly\"
  }" | jq
```

## Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery-worker
```

### Restart Services
```bash
docker-compose restart

# Specific service
docker-compose restart backend
```

### Stop Everything
```bash
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

### Access Database
```bash
docker-compose exec postgres psql -U postgres -d ai_crm
```

### Run Backend Commands
```bash
# Python shell
docker-compose exec backend python

# Run migrations
docker-compose exec backend alembic upgrade head

# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## Development Without Docker

### Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations
alembic upgrade head

# Seed data
python seed_data.py

# Start server
uvicorn app.main:app --reload --port 8000
```

You'll need PostgreSQL and Redis running locally or update DATABASE_URL and REDIS_URL in .env.

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Set up .env file
cp .env.example .env

# Start dev server
npm run dev
```

## Troubleshooting

### "Connection refused" errors
Wait 30-60 seconds after `docker-compose up` for all services to initialize.

### API returns 401 Unauthorized
Your token may have expired. Login again to get a fresh token.

### Database errors
```bash
# Reset database
docker-compose down -v
docker-compose up -d
# Wait 30 seconds
docker-compose exec backend alembic upgrade head
docker-compose exec backend python seed_data.py
```

### Port already in use
Change ports in docker-compose.yml if 5432, 6379, 8000, or 5173 are taken:
```yaml
ports:
  - "8001:8000"  # Change left side to available port
```

### Anthropic API errors
Verify your API key in backend/.env. Get a new one at https://console.anthropic.com/

## Next Steps

1. **Explore the API** at http://localhost:8000/api/docs
2. **Try generating messages** for different occasions
3. **Create campaigns** for bulk messaging
4. **View analytics** dashboard
5. **Read full documentation** in README.md
6. **Deploy to production** using DEPLOYMENT.md

## Support

- Check logs: `docker-compose logs -f`
- Read README.md for detailed documentation
- Open an issue on GitHub

---

Happy messaging! 🚀
