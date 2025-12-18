# Deployment Guide

This guide covers deploying the AI CRM Messaging System to production environments.

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Railway Deployment](#railway-deployment)
3. [Digital Ocean Deployment](#digital-ocean-deployment)
4. [Render Deployment](#render-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Setup](#database-setup)
7. [SSL/HTTPS Configuration](#sslhttps-configuration)
8. [Monitoring and Logging](#monitoring-and-logging)
9. [Backup Strategy](#backup-strategy)
10. [Scaling Considerations](#scaling-considerations)

## Pre-Deployment Checklist

- [ ] Anthropic API key obtained
- [ ] Production database provisioned (PostgreSQL 14+)
- [ ] Redis instance available
- [ ] Domain name configured (optional)
- [ ] SSL certificate ready (for custom domains)
- [ ] Environment variables prepared
- [ ] Database migrations tested
- [ ] Backup strategy planned

## Railway Deployment

Railway offers the easiest deployment with PostgreSQL and Redis included.

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
railway login
```

### Step 2: Initialize Project
```bash
cd ai-crm-messaging-system
railway init
```

### Step 3: Add Services

**Add PostgreSQL:**
```bash
railway add postgresql
```

**Add Redis:**
```bash
railway add redis
```

### Step 4: Set Environment Variables
```bash
railway variables set ANTHROPIC_API_KEY=your-api-key
railway variables set SECRET_KEY=your-secret-key-32-chars-min
railway variables set ENVIRONMENT=production
railway variables set DEBUG=False
```

### Step 5: Deploy Backend
```bash
cd backend
railway up
```

### Step 6: Run Migrations
```bash
railway run alembic upgrade head
```

### Step 7: Deploy Frontend
```bash
cd ../frontend
railway up
```

### Step 8: Configure Custom Domain (Optional)
Go to Railway dashboard → Settings → Custom Domain

**Railway Button:**
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

## Digital Ocean Deployment

### Option 1: App Platform (Easiest)

1. **Create App**
   - Go to Digital Ocean → App Platform → Create App
   - Connect GitHub repository

2. **Configure Services**

**Backend Service:**
```yaml
name: backend
dockerfile_path: backend/Dockerfile
http_port: 8000
instance_count: 1
instance_size_slug: basic-xs
envs:
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}
  - key: REDIS_URL
    value: ${redis.REDIS_URL}
  - key: ANTHROPIC_API_KEY
    value: your-api-key
    type: SECRET
```

**Frontend Service:**
```yaml
name: frontend
dockerfile_path: frontend/Dockerfile
http_port: 5173
instance_count: 1
instance_size_slug: basic-xs
```

**Database:**
- Add Managed PostgreSQL database (Production)
- Add Managed Redis (Production)

3. **Deploy**
   - Click "Create Resources"
   - Wait for deployment
   - Run migrations via console

### Option 2: Droplet (Manual)

1. **Create Droplet**
   - Ubuntu 22.04 LTS
   - 2GB RAM minimum
   - Enable monitoring

2. **Initial Setup**
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y
```

3. **Clone Repository**
```bash
git clone https://github.com/yourusername/ai-crm-messaging-system.git
cd ai-crm-messaging-system
```

4. **Set Environment Variables**
```bash
cp backend/.env.example backend/.env
nano backend/.env
# Edit with production values
```

5. **Deploy with Docker Compose**
```bash
docker-compose up -d
```

6. **Set Up Nginx Reverse Proxy**
```bash
apt install nginx -y

cat > /etc/nginx/sites-available/ai-crm << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/ai-crm /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

7. **Install SSL with Let's Encrypt**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

## Render Deployment

1. **Create New Web Service**
   - Connect GitHub repository
   - Select Docker deployment

2. **Backend Configuration**
```yaml
Name: ai-crm-backend
Region: Oregon (or closest to you)
Branch: main
Root Directory: backend
Environment: Docker
Instance Type: Starter ($7/month)

Environment Variables:
DATABASE_URL: (from Render PostgreSQL)
REDIS_URL: (from Render Redis)
ANTHROPIC_API_KEY: <secret>
SECRET_KEY: <secret>
```

3. **Add PostgreSQL**
   - Create PostgreSQL database
   - Copy connection string to DATABASE_URL

4. **Add Redis**
   - Create Redis instance
   - Copy connection string to REDIS_URL

5. **Frontend Configuration**
```yaml
Name: ai-crm-frontend
Region: Oregon
Branch: main
Root Directory: frontend
Environment: Docker
Instance Type: Starter

Environment Variables:
VITE_API_URL: https://ai-crm-backend.onrender.com/api
```

## Environment Configuration

### Production Environment Variables

**Backend:**
```env
# Required - NO DEFAULTS in production
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379/0
ANTHROPIC_API_KEY=sk-ant-xxxxx
SECRET_KEY=<generate-secure-random-32-char-string>

# Application
ENVIRONMENT=production
DEBUG=False
APP_NAME=AI CRM Messaging System

# Security
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS (comma-separated)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# AI Settings
DEFAULT_AI_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=1000
AI_TEMPERATURE=0.7

# Optional - Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@yourdomain.com
```

**Frontend:**
```env
VITE_API_URL=https://api.yourdomain.com/api
```

### Generate Secure SECRET_KEY
```python
import secrets
print(secrets.token_urlsafe(32))
```

Or:
```bash
openssl rand -base64 32
```

## Database Setup

### Run Migrations
```bash
# In production
docker-compose exec backend alembic upgrade head

# Or on Railway
railway run alembic upgrade head

# Or on Render
# Use shell access in dashboard
```

### Create Admin User
```python
# Via Python shell
from app.models.user import User
from app.utils.auth import get_password_hash
from app.config.database import SyncSessionLocal

db = SyncSessionLocal()
admin = User(
    email="admin@yourdomain.com",
    full_name="Admin User",
    role="admin",
    hashed_password=get_password_hash("secure-password-here")
)
db.add(admin)
db.commit()
```

### Backup PostgreSQL
```bash
# Manual backup
pg_dump -h hostname -U username -d dbname > backup.sql

# Restore
psql -h hostname -U username -d dbname < backup.sql

# Automated daily backups (cron)
0 2 * * * pg_dump -h localhost -U postgres ai_crm > /backups/ai_crm_$(date +\%Y\%m\%d).sql
```

## SSL/HTTPS Configuration

### Let's Encrypt (Certbot)
```bash
# Install Certbot
apt install certbot python3-certbot-nginx

# Obtain certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
certbot renew --dry-run
```

### Cloudflare (Recommended)
1. Add domain to Cloudflare
2. Update DNS to Cloudflare nameservers
3. Enable "Full (strict)" SSL mode
4. Enable "Always Use HTTPS"
5. Configure page rules for caching

## Monitoring and Logging

### Application Monitoring

**Sentry Integration:**
```bash
pip install sentry-sdk[fastapi]
```

```python
# In app/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment=settings.ENVIRONMENT,
    traces_sample_rate=1.0,
)
```

### Log Aggregation

**Docker Compose Logging:**
```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

**View Logs:**
```bash
docker-compose logs -f backend
docker-compose logs -f celery-worker
```

### Health Checks

**Add to docker-compose.yml:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Backup Strategy

### Database Backups

**Automated Backups:**
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="ai_crm"

# Create backup
docker-compose exec -T postgres pg_dump -U postgres $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Compress
gzip $BACKUP_DIR/backup_$DATE.sql

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz s3://your-bucket/backups/
```

**Schedule with Cron:**
```bash
0 2 * * * /path/to/backup.sh >> /var/log/backup.log 2>&1
```

### Application Data Backups
- Contact exports (CSV)
- Message templates
- Campaign configurations
- User data

## Scaling Considerations

### Horizontal Scaling

**Load Balancer Setup:**
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location /api {
        proxy_pass http://backend;
    }
}
```

### Database Scaling
- Read replicas for analytics queries
- Connection pooling (PgBouncer)
- Query optimization and indexing

### Celery Workers
```bash
# Scale workers
docker-compose up -d --scale celery-worker=3
```

### Redis Caching
- Cache frequently accessed data
- Session storage
- Rate limiting

### CDN for Frontend
- Cloudflare
- AWS CloudFront
- Vercel Edge Network

## Performance Tuning

### Database Optimization
```sql
-- Add indexes
CREATE INDEX idx_messages_status ON messages(status);
CREATE INDEX idx_messages_contact_id ON messages(contact_id);
CREATE INDEX idx_contacts_segment ON contacts(segment);
CREATE INDEX idx_contacts_birthday ON contacts(birthday);
```

### Application Tuning
```python
# In settings.py
POOL_SIZE = 20  # Database connection pool
MAX_OVERFLOW = 40
POOL_PRE_PING = True
```

## Troubleshooting

### Common Issues

**Database Connection Refused:**
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check firewall rules

**Redis Connection Error:**
- Verify REDIS_URL
- Check Redis service status
- Ensure network connectivity

**API 500 Errors:**
- Check application logs
- Verify environment variables
- Check database migrations

**CORS Errors:**
- Update CORS_ORIGINS
- Check frontend API_URL
- Verify protocol (http vs https)

## Security Best Practices

1. **Never commit .env files**
2. **Use strong SECRET_KEY (32+ chars)**
3. **Enable HTTPS only in production**
4. **Regular dependency updates**
5. **Database encryption at rest**
6. **API rate limiting**
7. **Regular security audits**
8. **Monitor for suspicious activity**

## Post-Deployment Checklist

- [ ] Application accessible via HTTPS
- [ ] Database migrations applied
- [ ] Admin user created
- [ ] Health check endpoint responding
- [ ] Logs being collected
- [ ] Backups configured
- [ ] Monitoring alerts set up
- [ ] SSL certificate auto-renewal tested
- [ ] CORS configured correctly
- [ ] Environment variables verified
- [ ] API documentation accessible
- [ ] Error tracking (Sentry) working

## Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Test database connection
4. Review health check status

---

**Deployment Guide** - AI CRM Messaging System
