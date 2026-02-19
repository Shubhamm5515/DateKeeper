# Supabase Quick Start Guide

Get your DateKeeper app running with Supabase in 10 minutes!

## 1. Create Supabase Project (2 minutes)

1. Go to [https://supabase.com](https://supabase.com) and sign up
2. Click "New Project"
3. Enter:
   - **Name**: `datekeeper`
   - **Database Password**: Generate and save it!
   - **Region**: Choose closest to you
4. Click "Create new project"
5. Wait 2-3 minutes ☕

## 2. Get Connection String (1 minute)

1. In Supabase Dashboard, go to **Settings** → **Database**
2. Scroll to **Connection string** section
3. Select **URI** tab
4. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with your actual password

## 3. Update Backend Configuration (1 minute)

Edit `backend/.env`:

```bash
# Replace this line:
DATABASE_URL=sqlite:///./documents.db

# With your Supabase connection string:
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
```

## 4. Create Database Schema (2 minutes)

```bash
cd backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run migration script
python supabase_migrate.py
```

You should see:
```
✅ MIGRATION COMPLETED SUCCESSFULLY!
```

## 5. Test Connection (1 minute)

```bash
python test_supabase_connection.py
```

You should see:
```
✅ Connection successful!
✅ ALL CHECKS PASSED!
```

## 6. Start Backend (1 minute)

```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/health

You should see:
```json
{"status": "healthy"}
```

## 7. Test with Frontend (2 minutes)

```bash
# In a new terminal
cd frontend
npm run dev
```

Visit: http://localhost:5173

1. Register a new user
2. Create a document
3. Check Supabase Dashboard → **Table Editor** → `documents` table
4. You should see your document! 🎉

---

## Troubleshooting

### "Connection refused"
- Check if password is correct in DATABASE_URL
- Verify Supabase project is active (not paused)

### "SSL required"
Add `?sslmode=require` to your connection string:
```
postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres?sslmode=require
```

### "Table already exists"
That's fine! The migration script handles existing tables.

### "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

---

## Deploy to Render

1. Go to Render Dashboard → Your backend service
2. Go to **Environment** tab
3. Update `DATABASE_URL` with your Supabase connection string
4. Click "Save Changes"
5. Render will redeploy automatically

---

## Next Steps

- ✅ Enable automatic backups in Supabase
- ✅ Set up monitoring in Supabase Dashboard
- ✅ Consider using Supabase Auth for authentication
- ✅ Use Supabase Storage for document images
- ✅ Enable Row Level Security (RLS) for better security

---

## Need Help?

- Check `SUPABASE_MIGRATION_GUIDE.md` for detailed guide
- Supabase Docs: https://supabase.com/docs
- Supabase Discord: https://discord.supabase.com
