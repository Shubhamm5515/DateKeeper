# 🚀 Start DateKeeper Backend

Port 8000 is used by Splunk, so we're using port 8001 instead.

## Quick Start

### Windows:
```bash
cd backend
start.bat
```

### Mac/Linux:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8001
```

## Access Points

- **Backend API**: http://localhost:8001
- **Health Check**: http://localhost:8001/health
- **API Docs**: http://localhost:8001/docs
- **Frontend**: http://localhost:5173 (after starting frontend)

## Start Frontend

In a new terminal:
```bash
cd frontend
npm run dev
```

## Troubleshooting

### Port Already in Use
If port 8001 is also in use, change it:
```bash
python -m uvicorn app.main:app --reload --port 8002
```

Then update `frontend/.env`:
```
VITE_API_URL=http://localhost:8002
```

### Backend Not Starting
1. Check if Python is installed: `python --version`
2. Check if dependencies are installed: `pip list`
3. Reinstall if needed: `pip install -r requirements.txt`

### Frontend Can't Connect
1. Make sure backend is running on port 8001
2. Check `frontend/.env` has correct VITE_API_URL
3. Restart frontend after changing .env

## Production Deployment

For Render deployment, the port is automatically set by Render via `$PORT` environment variable. No changes needed!

---

**Current Configuration:**
- Backend: Port 8001 (local)
- Frontend: Port 5173 (local)
- Production Backend: https://datekeeper-1.onrender.com
- Production Frontend: https://date-keeper-ivory.vercel.app
