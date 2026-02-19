# Document Expiry Reminder - Backend

FastAPI backend with AI-powered OCR for document expiry date extraction.

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up database (Choose one):**

### Option A: Supabase PostgreSQL (Recommended)
```bash
# See SUPABASE_QUICKSTART.md for detailed guide
cp .env.example .env
# Add your Supabase connection string to .env
python supabase_migrate.py
python test_supabase_connection.py
```

### Option B: SQLite (Development only)
```bash
cp .env.example .env
# DATABASE_URL=sqlite:///./documents.db (default)
```

3. **Configure environment variables:**
Edit `.env` and add your API keys (see `.env.example` for details)

4. **Run the server:**
```bash
uvicorn app.main:app --reload
```

Server will run on: http://localhost:8000

## Database Setup

### Supabase PostgreSQL (Recommended for Production)

**Why Supabase?**
- ✅ Free tier: 500MB database, 2GB bandwidth
- ✅ No cold starts (unlike Render free tier)
- ✅ Automatic daily backups
- ✅ Better performance and scalability
- ✅ Built-in dashboard and monitoring

**Quick Setup (10 minutes):**

1. Create Supabase project at [https://supabase.com](https://supabase.com)
2. Get connection string from Settings → Database
3. Update `.env`:
   ```bash
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
4. Run migration:
   ```bash
   python supabase_migrate.py
   ```

**Detailed guides:**
- Quick Start: `SUPABASE_QUICKSTART.md`
- Full Guide: `../SUPABASE_MIGRATION_GUIDE.md`
- Checklist: `../SUPABASE_MIGRATION_CHECKLIST.md`

### SQLite (Development Only)

SQLite is included by default for local development but is NOT recommended for production:
- ❌ Not suitable for multi-user applications
- ❌ No automatic backups
- ❌ Limited scalability
- ❌ File-based (can be lost easily)

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### OCR
- `POST /api/ocr/extract-expiry` - Extract expiry date from document image
- `GET /api/ocr/health` - Check OCR service status

### Documents
- `POST /api/documents/` - Create new document
- `GET /api/documents/` - Get all documents
- `GET /api/documents/{id}` - Get specific document
- `PUT /api/documents/{id}` - Update document
- `DELETE /api/documents/{id}` - Delete document
- `GET /api/documents/stats/summary` - Get statistics

## Deployment

### Deploy to Render with Supabase

1. **Set up Supabase database** (see above)

2. **Push code to GitHub**

3. **Create Web Service on Render:**
   - Connect your GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120 --keep-alive 5`

4. **Add environment variables in Render:**
   ```bash
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
   SECRET_KEY=your-secret-key
   OCRSPACE_API_KEY=your-key
   GEMINI_API_KEY=your-key
   # ... other API keys
   ```

5. **Deploy!**

**Benefits of Supabase + Render:**
- ✅ Database never sleeps (no cold starts)
- ✅ Backend can sleep, database stays fast
- ✅ Automatic backups
- ✅ Better performance

### Testing

```bash
# Test database connection
python test_supabase_connection.py

# Test OCR
python test_ocr.py

# Test email notifications
python test_email.py

# Test reminders
python test_reminder.py

# Test authentication
python test_auth.py
```

## Useful Scripts

| Script | Purpose |
|--------|---------|
| `supabase_migrate.py` | Create database schema in Supabase |
| `test_supabase_connection.py` | Test Supabase connection |
| `export_sqlite_data.py` | Export SQLite data to SQL file |
| `check_data.py` | View current database contents |
| `test_*.py` | Various test scripts |

## Troubleshooting

### Database Connection Issues

**"Connection refused":**
- Check DATABASE_URL is correct
- Verify Supabase project is active
- Check password is correct

**"SSL required":**
Add `?sslmode=require` to connection string:
```
DATABASE_URL=postgresql://...?sslmode=require
```

**"No module named 'psycopg2'":**
```bash
pip install psycopg2-binary
```

### OCR Issues

**"OCR.space API Error":**
- Check OCRSPACE_API_KEY in .env
- Free tier: 25,000 requests/month
- Get key at: https://ocr.space/ocrapi

**"Gemini API Error":**
- Check GEMINI_API_KEY in .env
- Get key at: https://makersuite.google.com/app/apikey

### Notification Issues

**Email not sending:**
- Check SMTP credentials in .env
- For Gmail: Enable 2FA and generate App Password
- Check SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

**SMS not sending:**
- Check Twilio credentials in .env
- Verify phone number format: +1234567890 (E.164)
- Check Twilio account balance

## Performance Optimization

### Connection Pooling

Already configured in `app/database.py`:
- Pool size: 5 connections
- Max overflow: 10 connections
- Pre-ping: Verify connections before use
- Recycle: Recycle connections after 1 hour

### Caching

Settings endpoint cached for 5 minutes (see `app/routers/auth.py`)

### Monitoring

- Supabase Dashboard → Database → Query Performance
- Render Dashboard → Metrics
- Check logs for slow queries
