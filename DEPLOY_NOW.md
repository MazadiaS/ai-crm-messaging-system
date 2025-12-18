# 🚀 Deploy to Railway - Step by Step

Get your AI CRM system live in **5 minutes**!

---

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Your OpenAI API key (keep this secret!)

---

## 🎯 Option 1: Railway (Recommended - Easiest)

### **Step 1: Push to GitHub** (2 minutes)

```bash
cd /Users/muje/ai-crm-messaging-system

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit - AI CRM with OpenAI"

# Create repo on GitHub and push
# Go to: https://github.com/new
# Name it: ai-crm-messaging-system
# Then:
git remote add origin https://github.com/YOUR_USERNAME/ai-crm-messaging-system.git
git branch -M main
git push -u origin main
```

### **Step 2: Deploy to Railway** (3 minutes)

1. **Go to Railway:**
   - Visit: https://railway.app/new
   - Click "Login with GitHub"

2. **Create New Project:**
   - Click "Deploy from GitHub repo"
   - Select your repo: `ai-crm-messaging-system`

3. **Add PostgreSQL:**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will create it automatically

4. **Add Redis:**
   - Click "New" → "Database" → "Redis"
   - Railway will create it automatically

5. **Configure Backend Service:**
   - Click on your backend service
   - Go to "Settings" → "Service"
   - Root Directory: `backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. **Set Environment Variables:**
   Click "Variables" and add:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   SECRET_KEY=railway-super-secret-key-for-production-change-later
   DEBUG=False
   ENVIRONMENT=production
   CORS_ORIGINS=*
   ```

7. **Deploy:**
   - Railway will automatically build and deploy
   - Wait 2-3 minutes

8. **Run Migrations:**
   - Go to service → "Deployments"
   - Click on the running deployment
   - Click "View Logs"
   - Once deployed, go to "Settings" → "Service Settings"
   - Add Build Command: `alembic upgrade head`
   - Redeploy

9. **Get Your URL:**
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - You'll get: `https://your-app.railway.app`

10. **Access Your API:**
    ```
    https://your-app.railway.app/api/docs
    ```

### **Step 3: Seed Demo Data** (1 minute)

Railway doesn't have easy shell access, but you can:

**Option A:** Use the API directly to create data via Swagger UI

**Option B:** Add a seed endpoint temporarily:

Create `backend/app/api/admin.py`:
```python
from fastapi import APIRouter, Depends
from app.api.deps import AdminUser
from app.config.database import get_sync_db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/seed")
async def seed_data(current_user: AdminUser):
    """Seed database with demo data"""
    from seed_data import seed_database
    seed_database()
    return {"message": "Database seeded successfully"}
```

Then call: `POST /api/admin/seed` after creating admin user.

---

## 🎯 Option 2: Render (Alternative)

### **Step 1: Push to GitHub** (same as above)

### **Step 2: Deploy to Render**

1. **Go to Render:**
   - Visit: https://render.com
   - Sign up with GitHub

2. **Create PostgreSQL:**
   - New → PostgreSQL
   - Name: `ai-crm-db`
   - Plan: Free
   - Create Database
   - Copy the "Internal Database URL"

3. **Create Redis:**
   - New → Redis
   - Name: `ai-crm-redis`
   - Plan: Free
   - Copy the "Internal Redis URL"

4. **Create Web Service:**
   - New → Web Service
   - Connect your GitHub repo
   - Settings:
     ```
     Name: ai-crm-backend
     Root Directory: backend
     Environment: Docker
     Plan: Free
     ```

5. **Environment Variables:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=<paste-internal-db-url>
   REDIS_URL=<paste-internal-redis-url>
   SECRET_KEY=render-production-secret-key
   DEBUG=False
   ENVIRONMENT=production
   ```

6. **Build Command:**
   ```
   pip install -r requirements.txt && alembic upgrade head
   ```

7. **Start Command:**
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

8. **Deploy:**
   - Click "Create Web Service"
   - Wait 5-10 minutes
   - Get URL: `https://ai-crm-backend.onrender.com`

---

## 🎯 Option 3: Vercel + Neon (Fastest for Backend)

### **Step 1: Deploy Database to Neon**

1. Go to: https://neon.tech
2. Create free account
3. Create new project: "ai-crm"
4. Copy connection string

### **Step 2: Deploy to Vercel**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /Users/muje/ai-crm-messaging-system/backend
vercel

# Set environment variables
vercel env add OPENAI_API_KEY
vercel env add DATABASE_URL
vercel env add REDIS_URL
# ... etc

# Deploy to production
vercel --prod
```

---

## ✅ After Deployment

### **Test Your Live API:**

1. **Health Check:**
   ```
   https://your-app.railway.app/health
   ```

2. **API Documentation:**
   ```
   https://your-app.railway.app/api/docs
   ```

3. **Create Admin User:**
   ```
   POST /api/auth/register
   {
     "email": "admin@demo.com",
     "password": "SecurePassword123!",
     "full_name": "Demo Admin",
     "role": "admin"
   }
   ```

4. **Login:**
   ```
   POST /api/auth/login
   {
     "email": "admin@demo.com",
     "password": "SecurePassword123!"
   }
   ```

5. **Create Contact:**
   ```
   POST /api/contacts
   {
     "name": "John Smith",
     "email": "john@example.com",
     "segment": "VIP",
     "language": "en"
   }
   ```

6. **Generate AI Message:**
   ```
   POST /api/messages/generate
   {
     "contact_id": "<contact-id-from-step-5>",
     "occasion_type": "birthday",
     "tone": "professional_friendly"
   }
   ```

---

## 🎓 For Your Interview

### **Share These URLs:**

```
Live API: https://your-app.railway.app/api/docs
GitHub Repo: https://github.com/YOUR_USERNAME/ai-crm-messaging-system
Documentation: https://github.com/YOUR_USERNAME/ai-crm-messaging-system#readme
```

### **Demo Flow:**

1. **Show the live API docs**
2. **Register a user**
3. **Create a contact**
4. **Generate AI message** ← This is the wow moment!
5. **Show approval workflow**
6. **Display analytics**

---

## 🚀 Quick Railway Deploy (Fastest)

**If you just want it deployed NOW:**

1. Visit: https://railway.app/new
2. Login with GitHub
3. "Deploy from GitHub repo"
4. Add PostgreSQL + Redis
5. Set OPENAI_API_KEY environment variable
6. Wait 3 minutes
7. Get live URL!

**That's it!** 🎉

---

## 🔧 Troubleshooting

### **Build Fails:**
- Check logs in Railway dashboard
- Ensure `requirements.txt` is correct
- Verify Python version (3.11+)

### **Database Connection Error:**
- Make sure `DATABASE_URL` is set correctly
- Check PostgreSQL is added to project
- Verify migrations ran: `alembic upgrade head`

### **API Returns 500:**
- Check environment variables are set
- View logs in Railway dashboard
- Ensure OPENAI_API_KEY is valid

### **CORS Issues:**
- Set `CORS_ORIGINS=*` for testing
- Or specify your frontend domain

---

## 📊 Cost Breakdown

### **Railway (Free Tier):**
- ✅ PostgreSQL: Free (500MB)
- ✅ Redis: Free (100MB)
- ✅ Web Service: Free ($5 credit/month)
- ✅ Total: **FREE**

### **OpenAI Usage:**
- Each message: ~$0.0006
- 1000 messages: ~$0.60
- Demo/Testing: < $1

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] PostgreSQL database added
- [ ] Redis database added
- [ ] Environment variables set
- [ ] Service deployed
- [ ] Migrations ran
- [ ] Health check working
- [ ] API docs accessible
- [ ] Test user created
- [ ] AI message generated
- [ ] Live URL obtained

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ Health endpoint returns 200: `/health`
✅ API docs load: `/api/docs`
✅ Can register user: `POST /api/auth/register`
✅ Can login: `POST /api/auth/login`
✅ Can generate AI message: `POST /api/messages/generate`

---

## 🚀 Ready to Deploy?

**Fastest Path:**
1. Push to GitHub
2. Railway.app → Deploy from GitHub
3. Add PostgreSQL + Redis
4. Set OPENAI_API_KEY
5. Done!

**Get your live demo URL in 5 minutes!** ✨

---

**Need help? Check Railway logs or ask me!**
