# ⚡ DateKeeper - Quick Deploy (30 Minutes)

## 🚀 Super Fast Deployment Guide

---

## Step 1: Push to GitHub (5 min)

```bash
cd document-reminder-system
git init
git add .
git commit -m "DateKeeper - Ready to deploy"

# Create repo at: https://github.com/new (name: datekeeper)
git remote add origin https://github.com/YOUR_USERNAME/datekeeper.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend (10 min)

### A. Create Database
1. Go to: https://render.com/signup
2. New + → PostgreSQL
3. Name: `datekeeper-db`, Plan: **Free**
4. Click "Create Database"
5. **Wait 2-3 minutes** for database to be ready
6. **Copy Internal Database URL**:
   - Look for "Connections" section
   - Find "Internal Database URL" (NOT External)
   - It looks like: `postgresql://datekeeper_user:xxxxx@dpg-xxxxx/datekeeper`
   - Click the copy icon 📋
   - **Save this URL** - you'll need it in next step!
   postgresql://datekeeper_db_r23a_user:HzdIYtI4Kx6wl8HF4HAvMiETfe8Wi5Rx@dpg-d5mf5f3e5dus73efm55g-a/datekeeper_db_r23a

### B. Deploy Backend
1. Click "New +" → "Web Service"
2. **Connect Repository**:
   - Click "Connect account" if first time
   - Select your GitHub repository: `datekeeper`
   - Click "Connect"

3. **Configure Service** (Fill in these fields):
   
   **Basic Settings:**
   - **Name**: `datekeeper-api` (this will be your URL)
   - **Region**: Same as database (e.g., Singapore)
   - **Branch**: `main`
   - **Root Directory**: `backend` ← Important!
   
   **Build Settings:**
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: 
     ```
     gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```
   
   **Plan:**
   - Select: **Free** (512 MB RAM, 0.1 CPU)
   - Note: Service will sleep after 15 min inactivity

4. **Environment Variables** (Click "Advanced" → "Add Environment Variable"):
   
   Add these one by one (click "+ Add Environment Variable" for each):

```env
DATABASE_URL=<paste-internal-database-url-from-step-A>
SECRET_KEY=change-this-secret-key-12345
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
```

5. Click "Create Web Service" (blue button at bottom)
6. **Wait 5-10 minutes** for deployment (watch the logs)
7. Once you see "Your service is live 🎉":
   - **Copy your backend URL**: `https://datekeeper-api.onrender.com`
   - Click on the URL to test (should see: `{"message":"Document Expiry Reminder API"...}`)

**What the Render Dashboard Looks Like:**
```
┌────────────────────────────────────────────────────┐
│ Create a new Web Service                          │
├────────────────────────────────────────────────────┤
│                                                    │
│ Name *                                             │
│ [datekeeper-api                              ]     │
│                                                    │
│ Region *                                           │
│ [Singapore (Southeast Asia)                  ▼]   │
│                                                    │
│ Branch *                                           │
│ [main                                        ▼]   │
│                                                    │
│ Root Directory                                     │
│ [backend                                     ]     │ ← Important!
│                                                    │
│ Runtime *                                          │
│ [Python 3                                    ▼]   │
│                                                    │
│ Build Command *                                    │
│ [pip install -r requirements.txt            ]     │
│                                                    │
│ Start Command *                                    │
│ [gunicorn app.main:app --workers 1 ...     ]     │
│                                                    │
│ Plan *                                             │
│ ○ Starter ($7/month)                              │
│ ● Free ($0/month) ← Select this                   │
│                                                    │
│ [Advanced ▼]                                       │
│   Environment Variables                            │
│   [+ Add Environment Variable]                     │
│                                                    │
│              [Create Web Service]                  │
└────────────────────────────────────────────────────┘
```

**Troubleshooting:**
- ❌ Build failed? Check `requirements.txt` exists in `backend/` folder
- ❌ Start failed? Check `Procfile` or start command is correct
- ❌ Service unhealthy? Check environment variables are set correctly

---

## Step 3: Deploy Frontend (10 min)

1. Go to: https://vercel.com/signup
2. New Project → Import `datekeeper`
3. Settings:
   - Framework: Vite
   - Root: `frontend`
   - Build: `npm run build`
   - Output: `dist`

4. Environment Variables:
```env
VITE_API_URL=https://datekeeper-api.onrender.com
VITE_GOOGLE_CLIENT_ID=your-google-client-id
VITE_RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxx
VITE_RAZORPAY_PLAN_PRO=plan_xxxxxxxxxxxxx
VITE_RAZORPAY_PLAN_BUSINESS=plan_xxxxxxxxxxxxx
```

5. Click "Deploy" → Wait 3 min
6. **Your app is LIVE!** 🎉

---

## Step 4: Run Migrations (5 min)

1. Go to Render → Your backend → Shell tab
2. Run:
```bash
python migrate_add_users.py
python migrate_add_settings.py
python migrate_add_subscription.py
```

---

## Step 5: Keep Backend Awake (2 min)

1. Go to: https://cron-job.org/en/signup
2. Create job:
   - URL: `https://datekeeper-api.onrender.com/health`
   - Every: 14 minutes

---

## ✅ Done!

**Your App**: https://datekeeper.vercel.app
**API**: https://datekeeper-api.onrender.com

**Cost**: ₹0/month forever! 🎉

---

## 🔧 Quick Fixes

**Backend sleeping?**
→ Wait 30 seconds, it will wake up

**CORS error?**
→ Update `FRONTEND_URL` in Render backend env vars

**Can't login?**
→ Update Google OAuth redirect URIs:
- Add: `https://datekeeper.vercel.app/auth/google/callback`

---

**Full Guide**: See `FREE_DEPLOYMENT_GUIDE.md`
