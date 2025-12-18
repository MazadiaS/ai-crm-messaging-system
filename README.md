# AI-Powered CRM Messaging System

A production-ready full-stack application that uses Claude AI to generate personalized messages for CRM contacts, with human approval workflows, background job processing, and real-time analytics.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)

## Features

### Core Functionality
- **AI-Powered Message Generation**: Uses Claude Sonnet 4.5 to create personalized, context-aware messages
- **Human Approval Workflow**: All AI-generated messages require human review before sending
- **Multi-Language Support**: Russian, English, and Uzbek message generation
- **Contact Management**: Complete CRM for managing contacts with segments, tags, and custom fields
- **Campaign Management**: Create bulk messaging campaigns with scheduling and recurrence
- **Background Job Processing**: Celery + Redis for async message generation and sending
- **Real-Time Analytics**: Dashboard with charts, statistics, and AI usage tracking

### Technical Highlights
- **FastAPI Backend**: Modern async Python framework with automatic API documentation
- **React + TypeScript Frontend**: Type-safe UI with shadcn/ui components and TailwindCSS
- **PostgreSQL Database**: Robust data persistence with SQLAlchemy ORM
- **JWT Authentication**: Secure token-based auth with role-based access control
- **Docker Compose**: One-command deployment for development and production
- **Alembic Migrations**: Database versioning and migration management

## Tech Stack

### Backend
- **Framework**: FastAPI 0.109 with async/await
- **Database**: PostgreSQL 16 with SQLAlchemy 2.0
- **Task Queue**: Celery 5.3 + Redis 7
- **AI Integration**: Anthropic Claude API
- **Authentication**: JWT with python-jose
- **Validation**: Pydantic v2

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 5
- **State Management**: Zustand + TanStack Query
- **UI Components**: shadcn/ui + Radix UI
- **Styling**: TailwindCSS 3.4
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts 2

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database**: PostgreSQL 16
- **Cache/Queue**: Redis 7
- **Web Server**: Uvicorn (ASGI)

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Anthropic API key ([get one here](https://console.anthropic.com/))

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-crm-messaging-system.git
cd ai-crm-messaging-system
```

### 2. Set Up Environment Variables
```bash
# Copy backend environment file
cp backend/.env.example backend/.env

# Edit backend/.env and add your Anthropic API key
# ANTHROPIC_API_KEY=your-api-key-here

# Copy frontend environment file
cp frontend/.env.example frontend/.env
```

### 3. Start All Services
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis on port 6379
- Backend API on port 8000
- Celery worker and beat scheduler
- Frontend on port 5173

### 4. Access the Application
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### 5. Create Your First Admin User
Register at http://localhost:5173/register with role "admin"

## Project Structure

```
ai-crm-messaging-system/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── config/       # Settings and database config
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic (AI generator)
│   │   ├── tasks/        # Celery tasks
│   │   └── utils/        # Helpers and prompts
│   ├── alembic/          # Database migrations
│   ├── tests/            # Test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── lib/          # API client and utilities
│   │   ├── hooks/        # Custom React hooks
│   │   ├── stores/       # Zustand state stores
│   │   └── types/        # TypeScript types
│   └── package.json
└── docker-compose.yml
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user

### Contacts
- `GET /api/contacts` - List contacts (with filters)
- `POST /api/contacts` - Create contact
- `GET /api/contacts/{id}` - Get contact
- `PUT /api/contacts/{id}` - Update contact
- `DELETE /api/contacts/{id}` - Delete contact

### Messages
- `POST /api/messages/generate` - Generate AI message
- `GET /api/messages` - List messages (with filters)
- `GET /api/messages/{id}` - Get message
- `PATCH /api/messages/{id}` - Update message
- `POST /api/messages/{id}/approve` - Approve message
- `POST /api/messages/{id}/reject` - Reject message
- `POST /api/messages/{id}/send` - Send message
- `GET /api/messages/{id}/history` - Get audit trail

### Campaigns
- `GET /api/campaigns` - List campaigns
- `POST /api/campaigns` - Create campaign
- `GET /api/campaigns/{id}` - Get campaign
- `PUT /api/campaigns/{id}` - Update campaign
- `POST /api/campaigns/{id}/execute` - Execute campaign
- `POST /api/campaigns/{id}/pause` - Pause campaign

### Analytics
- `GET /api/analytics/dashboard` - Dashboard stats
- `GET /api/analytics/messages-by-status` - Message counts by status
- `GET /api/analytics/messages-by-occasion` - Message counts by occasion
- `GET /api/analytics/ai-usage-stats` - AI token and cost stats
- `GET /api/analytics/campaign-performance` - Campaign metrics

Full API documentation available at `/api/docs` when running.

## Development

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Run development server
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

## Database Migrations

### Create a New Migration
```bash
cd backend
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

## Environment Variables

### Backend (.env)
```env
# Required
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_crm
REDIS_URL=redis://localhost:6379/0
ANTHROPIC_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-min-32-chars

# Optional
DEBUG=True
ENVIRONMENT=development
DEFAULT_AI_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=1000
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

## Key Features Explained

### AI Message Generation
The system uses Claude Sonnet 4.5 with carefully crafted prompts to generate:
- Personalized messages based on contact details
- Context-aware content for different occasions
- Multi-language support (RU, EN, UZ)
- Different tones (professional, friendly, formal, warm)

### Human Approval Workflow
1. AI generates message → Status: `PENDING_APPROVAL`
2. Human reviews and can edit the message
3. Human approves → Status: `APPROVED`
4. System sends message → Status: `SENT`

All changes are tracked in the message history for audit purposes.

### Background Jobs
Celery handles:
- Bulk message generation for campaigns
- Scheduled message sending
- Daily birthday checks
- Email/SMS sending (mock implementation for demo)

### Analytics Dashboard
Real-time insights including:
- Total contacts and messages
- Messages by status and occasion type
- AI usage statistics (tokens, cost)
- Campaign performance metrics
- Timeline charts

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions including:
- Railway deployment
- Digital Ocean deployment
- SSL/HTTPS configuration
- Environment setup
- Monitoring and logging
- Backup strategies

## Security Considerations

- JWT tokens with expiration
- Password hashing with bcrypt
- SQL injection prevention via ORM
- CORS configuration
- Input validation with Pydantic
- Role-based access control (Admin, Manager, Viewer)

## Performance Optimization

- Database indexes on frequently queried fields
- Async/await for I/O operations
- Redis caching for session management
- Pagination for large datasets
- Connection pooling for database

## Future Enhancements

- WebSocket support for real-time updates
- Email template builder
- A/B testing for message variations
- Image generation with DALL-E
- SMS integration with Twilio
- Slack/Telegram notifications
- Advanced analytics with charts
- Multi-tenant support
- API rate limiting

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Email: your-email@example.com

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- AI powered by [Anthropic Claude](https://www.anthropic.com/)

---

**Built for the CROWE interview - showcasing production-ready full-stack development skills.**
