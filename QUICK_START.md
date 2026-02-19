# 🚀 DateKeeper - Quick Start Guide

## Start Backend (Port 8001)

**Windows:**
```bash
cd backend
start.bat
```

**Mac/Linux:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8001
```

Backend will be at: **http://localhost:8001**

## Start Frontend (Port 5173)

**In a new terminal:**
```bash
cd frontend
npm run dev
```

Frontend will be at: **http://localhost:5173**

## Test Your Setup

1. **Backend Health**: http://localhost:8001/health
2. **API Docs**: http://localhost:8001/docs
3. **Frontend**: http://localhost:5173

## Common Issues

### Port 8000 Already in Use
✅ **Fixed!** We're using port 8001 now (Splunk uses 8000)

### Backend Won't Start
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend Can't Connect
1. Make sure backend is running on port 8001
2. Check `frontend/.env` has: `VITE_API_URL=http://localhost:8001`
3. Restart frontend after changing .env

## Deploy to Production

### Backend (Render)
1. Push to GitHub
2. Render auto-deploys
3. No port changes needed (Render uses $PORT)

### Frontend (Vercel)
1. Change `frontend/.env`:
   ```
   VITE_API_URL=https://datekeeper-1.onrender.com
   ```
2. Push to GitHub
3. Vercel auto-deploys

## What's Working

✅ User authentication (JWT + Google OAuth)
✅ Document management
✅ OCR functionality  
✅ Email/SMS notifications
✅ Reminder scheduler
✅ Subscription tiers
❌ Payment processing (removed Razorpay)

## Next Steps

1. ✅ Test locally
2. ✅ Deploy to production
3. 📚 Migrate to Supabase (optional): See `backend/SUPABASE_QUICKSTART.md`

---

**Need Help?**
- Backend issues: Check `START_BACKEND.md`
- Deployment: Check `RENDER_FIX.md`
- Database: Check `SUPABASE_QUICKSTART.md`
