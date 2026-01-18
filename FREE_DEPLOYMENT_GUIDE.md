# 🚀 DateKeeper - Free Deployment Guide

## Complete guide to deploy your app for FREE (₹0/month)

---

## 📋 Overview

We'll deploy:
- **Frontend** → Vercel (Free)
- **Backend** → Render (Free)
- **Database** → Render PostgreSQL (Free)
- **Total Cost**: ₹0/month forever!

---

## 🎯 Step-by-Step Deployment

### PART 1: Prepare Your Code (10 minutes)

#### 1.1 Create GitHub Repository

```bash
# Initialize git (if not already done)
cd document-reminder-system
git init

# Create .gitignore
echo "node_modules/
.env
__pycache__/
*.pyc
.DS_Store
documents.db
uploads/*
!uploads/README.md" > .gitignore

# Commit your code
git add .
git commit -m "Initial commit - DateKeeper app"

# Create GitHub repo and push
# Go to: https://github.com/new
# Create repository named: datekeeper
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/datekeeper.git
git branch -M main
git push -u origin main
```

#### 1.2 Update Backend for Production

Create `document-reminder-system/backend/runtime.txt`:
```txt
python-3.11.0
```

Update `document-reminder-system/backend/requirements.txt` (add if missing):
```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.36
python-dotenv==1.0.1
pydantic==2.10.3
pydantic-settings==2.6.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.17
apscheduler==3.10.4
alembic==1.14.0
Pillow==11.0.0
python-dateutil==2.9.0
requests==2.32.3
sendgrid==6.11.0
twilio==9.0.0
google-auth==2.36.0
google-auth-oauthlib==1.2.1
google-auth-httplib2==0.2.0
google-generativeai==0.8.3
razorpay==1.4.1
authlib==1.3.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

Create `document-reminder-system/backend/Procfile`:
```
web: gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

#### 1.3 Update Frontend for Production

Update `document-reminder-system/frontend/package.json` (add build script if missing):
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

---

### PART 2: Deploy Backend to Render (15 minutes)

#### 2.1 Sign Up for Render

1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub account
4. Authorize Render to access your repositories

#### 2.2 Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. **Name**: `datekeeper-db`
3. **Database**: `datekeeper`
4. **User**: `datekeeper_user`
5. **Region**: Choose closest to you (e.g., Singapore)
6. **Plan**: **Free** (0 GB RAM, expires after 90 days - we'll handle this)
7. Click "Create Database"
8. **Wait 2-3 minutes** for database to initialize
9. **Find the Internal Database URL**:
   - On the database dashboard, scroll down to "Connections" section
   - You'll see two URLs:
     - **External Database URL** (starts with `postgres://`)
     - **Internal Database URL** (starts with `postgresql://`)
   - **Copy the INTERNAL Database URL** (click the 📋 copy icon)
   - It looks like: `postgresql://datekeeper_user:xxxxx@dpg-xxxxx-internal/datekeeper`
   - **Important**: Use INTERNAL, not External!
   - Save this URL - you'll paste it in the next step

**Visual Guide - What to Look For:**
```
┌─────────────────────────────────────────────────┐
│ Connections                                     │
├─────────────────────────────────────────────────┤
│                                                 │
│ External Database URL                           │
│ postgres://datekeeper_user:xxx@dpg-xxx/db  📋  │ ← DON'T use this
│                                                 │
│ Internal Database URL                           │
│ postgresql://datekeeper_user:xxx@dpg-xxx-      │
│ internal/datekeeper                         📋  │ ← USE THIS ONE!
│                                                 │
│ PSQL Command                                    │
│ psql -h dpg-xxx -U datekeeper_user datekeeper   │
└─────────────────────────────────────────────────┘
```

#### 2.3 Deploy Backend Web Service

1. Click "New +" → "Web Service"

2. **Connect Your Repository**:
   - If first time: Click "Connect account" → Authorize GitHub
   - Select your repository: `datekeeper`
   - Click "Connect"

3. **Configure Service Settings**:

   **Basic Information:**
   - **Name**: `datekeeper-api`
     - This becomes your URL: `https://datekeeper-api.onrender.com`
   - **Region**: Same as your database (e.g., Singapore)
   - **Branch**: `main`
   - **Root Directory**: `backend` ⚠️ **IMPORTANT!**
     - This tells Render to look in the backend folder

   **Runtime & Build:**
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```

   **Instance Type:**
   - **Plan**: Select **Free** 
     - 512 MB RAM
     - 0.1 CPU
     - Sleeps after 15 min inactivity
     - 750 hours/month (enough for 24/7 with wake-up pings)

#### 2.4 Add Environment Variables

Click "Environment" → "Add Environment Variable" and add:

```env
DATABASE_URL=<paste-internal-database-url-from-step-2.2>
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
OCRSPACE_API_KEY=K81615831188957
GEMINI_API_KEY=AIzaSyCmZ3sUtJC2r6hkqFzFMKmyrHFUkR0MqqY
FRONTEND_URL=https://datekeeper.vercel.app
ENVIRONMENT=production
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxx
RAZORPAY_PLAN_PRO=plan_xxxxxxxxxxxxx
RAZORPAY_PLAN_BUSINESS=plan_xxxxxxxxxxxxx
```

11. Click "Create Web Service"
12. Wait 5-10 minutes for deployment
13. **Copy your backend URL**: `https://datekeeper-api.onrender.com`

---

### PART 3: Deploy Frontend to Vercel (10 minutes)

#### 3.1 Sign Up for Vercel

1. Go to: https://vercel.com
2. Click "Sign Up"
3. Sign up with GitHub account
4. Authorize Vercel

#### 3.2 Deploy Frontend

1. Click "Add New..." → "Project"
2. Import your GitHub repository: `datekeeper`
3. **Framework Preset**: Vite
4. **Root Directory**: `frontend`
5. **Build Command**: `npm run build`
6. **Output Directory**: `dist`

#### 3.3 Add Environment Variables

Click "Environment Variables" and add:

```env
VITE_API_URL=https://datekeeper-api.onrender.com
VITE_GOOGLE_CLIENT_ID=your-google-client-id
VITE_RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxx
VITE_RAZORPAY_PLAN_PRO=plan_xxxxxxxxxxxxx
VITE_RAZORPAY_PLAN_BUSINESS=plan_xxxxxxxxxxxxx
```

7. Click "Deploy"
8. Wait 2-3 minutes
9. **Your app is live!** 🎉
10. **Copy your URL**: `https://datekeeper.vercel.app`

---

### PART 4: Update CORS & URLs (5 minutes)

#### 4.1 Update Backend CORS

Go to Render dashboard → Your backend service → Environment

Update `FRONTEND_URL`:
```env
FRONTEND_URL=https://datekeeper.vercel.app
```

Click "Save Changes" (will auto-redeploy)

#### 4.2 Update Google OAuth Redirect URIs

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click your OAuth 2.0 Client ID
3. Add to "Authorized JavaScript origins":
   - `https://datekeeper.vercel.app`
4. Add to "Authorized redirect URIs":
   - `https://datekeeper.vercel.app/auth/google/callback`
5. Click "Save"

#### 4.3 Update Razorpay Webhook (if using)

1. Go to: https://dashboard.razorpay.com/app/webhooks
2. Update webhook URL to:
   - `https://datekeeper-api.onrender.com/api/razorpay/webhook`

---

## 🎉 Your App is Live!

**Frontend**: https://datekeeper.vercel.app
**Backend**: https://datekeeper-api.onrender.com

---

## 🔧 Post-Deployment Setup

### 1. Run Database Migrations

```bash
# Install Render CLI
npm install -g @render-com/cli

# Login to Render
render login

# Connect to your service
render shell datekeeper-api

# Run migrations
python migrate_add_users.py
python migrate_add_settings.py
python migrate_add_subscription.py
```

**OR** use Render Dashboard:
1. Go to your backend service
2. Click "Shell" tab
3. Run migration commands

### 2. Test Your App

1. Visit: https://datekeeper.vercel.app
2. Register a new account
3. Upload a document
4. Check email notifications
5. Test reminders

---

## 💰 Free Tier Limits

### Vercel (Frontend)
- ✅ **Bandwidth**: 100 GB/month
- ✅ **Builds**: 6,000 minutes/month
- ✅ **Deployments**: Unlimited
- ✅ **Custom domain**: Free
- ✅ **SSL**: Free
- ⚠️ **Limit**: 100 GB bandwidth (enough for 10,000+ users)

### Render (Backend)
- ✅ **RAM**: 512 MB
- ✅ **CPU**: Shared
- ✅ **Bandwidth**: 100 GB/month
- ✅ **Build minutes**: 500/month
- ⚠️ **Sleeps after 15 min inactivity** (wakes up in ~30 seconds)
- ⚠️ **Limit**: Sleeps when inactive

### Render PostgreSQL (Database)
- ✅ **Storage**: 1 GB
- ✅ **Connections**: 97
- ⚠️ **Expires after 90 days** (need to create new one)
- ⚠️ **Limit**: 1 GB storage (~10,000 documents)

---

## 🚨 Important Notes

### 1. Backend Sleep Issue (Free Tier)

**Problem**: Render free tier sleeps after 15 minutes of inactivity.

**Solutions**:

**Option A: Use Cron Job (Free)**
```bash
# Use cron-job.org to ping your backend every 14 minutes
# URL to ping: https://datekeeper-api.onrender.com/health
```

1. Go to: https://cron-job.org
2. Sign up (free)
3. Create new cron job:
   - **URL**: `https://datekeeper-api.onrender.com/health`
   - **Schedule**: Every 14 minutes
   - **Method**: GET

**Option B: UptimeRobot (Free)**
1. Go to: https://uptimerobot.com
2. Sign up (free)
3. Add new monitor:
   - **Type**: HTTP(s)
   - **URL**: `https://datekeeper-api.onrender.com/health`
   - **Interval**: 5 minutes

### 2. Database Expiry (90 Days)

**Problem**: Free PostgreSQL expires after 90 days.

**Solution**: Backup and migrate

```bash
# Backup before expiry (day 85)
pg_dump $DATABASE_URL > backup.sql

# Create new database on Render
# Restore backup
psql $NEW_DATABASE_URL < backup.sql

# Update DATABASE_URL in backend environment variables
```

### 3. Custom Domain (Optional - Free)

**Vercel**:
1. Go to your project → Settings → Domains
2. Add your domain: `datekeeper.com`
3. Update DNS records (provided by Vercel)
4. SSL automatically configured

**Render**:
1. Go to your service → Settings → Custom Domain
2. Add: `api.datekeeper.com`
3. Update DNS records
4. SSL automatically configured

---

## 📊 Monitoring & Logs

### Vercel Logs
1. Go to: https://vercel.com/dashboard
2. Click your project
3. Click "Deployments" → Latest deployment → "View Function Logs"

### Render Logs
1. Go to: https://dashboard.render.com
2. Click your service
3. Click "Logs" tab
4. Real-time logs appear here

---

## 🔄 Continuous Deployment

**Automatic Deployment** is already set up!

Every time you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

- ✅ Vercel auto-deploys frontend (2-3 min)
- ✅ Render auto-deploys backend (5-10 min)

---

## 🐛 Troubleshooting

### Frontend not loading?
```bash
# Check build logs in Vercel dashboard
# Common issue: Environment variables not set
```

### Backend not responding?
```bash
# Check if service is sleeping (Render free tier)
# Visit: https://datekeeper-api.onrender.com/health
# Wait 30 seconds for wake up
```

### Database connection error?
```bash
# Check DATABASE_URL in Render environment variables
# Ensure it's the Internal Database URL
```

### CORS error?
```bash
# Update FRONTEND_URL in backend environment variables
# Should be: https://datekeeper.vercel.app
```

---

## 💡 Upgrade Options (When You Grow)

### When to Upgrade?

**Vercel** ($20/month):
- When you exceed 100 GB bandwidth
- When you need faster builds
- When you need team collaboration

**Render** ($7/month):
- When you need 24/7 uptime (no sleep)
- When you need more RAM (1 GB)
- When you need faster response times

**Database** ($7/month):
- When you exceed 1 GB storage
- When you need more than 90 days
- When you need backups

---

## 🎯 Cost Comparison

### Free Tier (Current)
```
Vercel: $0
Render Backend: $0
Render Database: $0
Total: $0/month
```

### Paid Tier (When Needed)
```
Vercel Pro: $20/month
Render Starter: $7/month
Render PostgreSQL: $7/month
Total: $34/month (~₹2,800/month)
```

### Break-even Point
```
Need ~4 Pro users ($9/month each) to cover costs
= $36/month revenue
- $34/month costs
= $2/month profit
```

---

## 📚 Additional Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **React Deployment**: https://vitejs.dev/guide/static-deploy.html

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Render
- [ ] Database created on Render
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set (both)
- [ ] CORS updated
- [ ] Google OAuth redirect URIs updated
- [ ] Database migrations run
- [ ] Test registration
- [ ] Test document upload
- [ ] Test email notifications
- [ ] Set up uptime monitoring (cron-job.org)
- [ ] Bookmark deployment URLs

---

## 🎉 Congratulations!

Your DateKeeper app is now live and accessible worldwide for FREE!

**Share your app**:
- Frontend: https://datekeeper.vercel.app
- API: https://datekeeper-api.onrender.com

**Next Steps**:
1. Share with friends and family
2. Collect feedback
3. Add features
4. Grow your user base
5. Monetize when ready!

---

**Need Help?** Check the troubleshooting section or deployment logs!

**Last Updated**: January 18, 2026
