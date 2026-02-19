# Supabase PostgreSQL Migration Guide

Complete guide to migrate from Render PostgreSQL to Supabase PostgreSQL.

## Why Supabase?

- **Free Tier**: 500MB database, 2GB bandwidth, 50MB file storage
- **Better Performance**: No cold starts like Render free tier
- **Built-in Features**: Auth, Storage, Realtime, Edge Functions
- **Easy Backups**: Automatic daily backups
- **Better Dashboard**: SQL editor, table viewer, API docs

---

## Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Name**: datekeeper (or your choice)
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free
5. Click "Create new project"
6. Wait 2-3 minutes for provisioning

---

## Step 2: Get Supabase Connection Details

1. In your Supabase project dashboard, go to **Settings** → **Database**
2. Scroll to **Connection string** section
3. Copy the **Connection string** (URI format)
4. It looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
   ```

---

## Step 3: Update Backend Configuration

### Update `.env` file:

```bash
# Replace your current DATABASE_URL with Supabase connection string
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres

# Add connection pooling for better performance (optional but recommended)
# Get this from Supabase Settings → Database → Connection Pooling
DATABASE_URL_POOLER=postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
```

### Update `backend/app/database.py`:

No changes needed! Your current code already supports PostgreSQL.

---

## Step 4: Create Database Schema in Supabase

### Option A: Using SQL Editor (Recommended)

1. Go to Supabase Dashboard → **SQL Editor**
2. Click "New query"
3. Copy and paste the schema from `backend/supabase_schema.sql` (created below)
4. Click "Run"

### Option B: Using Migration Script

Run the Python migration script:
```bash
cd backend
python supabase_migrate.py
```

---

## Step 5: Export Data from Render (If you have existing data)

### Export from Render:

```bash
# Connect to Render PostgreSQL
pg_dump [YOUR_RENDER_DATABASE_URL] > render_backup.sql

# Or use Render dashboard to download backup
```

### Import to Supabase:

```bash
# Using psql
psql [YOUR_SUPABASE_DATABASE_URL] < render_backup.sql

# Or use Supabase SQL Editor to paste and run the SQL
```

---

## Step 6: Test the Connection

```bash
cd backend

# Test database connection
python test_supabase_connection.py

# If successful, start the backend
uvicorn app.main:app --reload
```

---

## Step 7: Update Render Deployment

1. Go to Render Dashboard → Your backend service
2. Go to **Environment** tab
3. Update `DATABASE_URL` with your Supabase connection string
4. Click "Save Changes"
5. Render will automatically redeploy

---

## Step 8: Verify Migration

1. Open your frontend: `http://localhost:5173`
2. Register a new user
3. Create a document
4. Check Supabase Dashboard → **Table Editor** → `users` and `documents` tables
5. Verify data is being saved

---

## Performance Optimization

### Enable Connection Pooling:

Update `backend/app/database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)
```

### Use Supabase Connection Pooler:

For production, use the pooler URL instead of direct connection:
```
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
```

---

## Supabase Features You Can Use

### 1. Row Level Security (RLS)

Protect your data at the database level:

```sql
-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Users can only see their own documents
CREATE POLICY "Users can view own documents"
ON documents FOR SELECT
USING (auth.uid()::text = user_id);

-- Users can only insert their own documents
CREATE POLICY "Users can insert own documents"
ON documents FOR INSERT
WITH CHECK (auth.uid()::text = user_id);
```

### 2. Realtime Subscriptions

Get live updates when documents change:

```javascript
// Frontend code
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

supabase
  .channel('documents')
  .on('postgres_changes', 
    { event: '*', schema: 'public', table: 'documents' },
    (payload) => {
      console.log('Document changed:', payload)
      // Update UI
    }
  )
  .subscribe()
```

### 3. Storage for Document Images

Store uploaded document images in Supabase Storage:

```javascript
// Upload image
const { data, error } = await supabase.storage
  .from('documents')
  .upload(`${userId}/${filename}`, file)
```

### 4. Edge Functions

Run serverless functions for OCR processing:

```bash
supabase functions new ocr-processor
```

---

## Troubleshooting

### Connection Refused:
- Check if your IP is allowed in Supabase (Settings → Database → Connection Pooling)
- Supabase allows all IPs by default, but verify

### SSL Certificate Error:
Add `?sslmode=require` to your connection string:
```
postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres?sslmode=require
```

### Slow Queries:
- Enable connection pooling
- Add indexes on frequently queried columns
- Use Supabase Dashboard → Database → Query Performance

### Migration Errors:
- Check Supabase logs: Dashboard → Logs
- Verify schema matches your models
- Check for data type mismatches

---

## Cost Comparison

| Feature | Render Free | Supabase Free |
|---------|-------------|---------------|
| Database | 90 days then deleted | Permanent |
| Storage | 1GB | 500MB |
| Bandwidth | - | 2GB |
| Cold Starts | Yes (15 min) | No |
| Backups | No | Daily automatic |
| Dashboard | Basic | Advanced |

---

## Next Steps After Migration

1. ✅ Remove SQLite fallback code
2. ✅ Enable Supabase RLS for security
3. ✅ Set up automatic backups
4. ✅ Monitor query performance
5. ✅ Consider using Supabase Auth instead of custom JWT
6. ✅ Use Supabase Storage for document images
7. ✅ Enable Realtime for live updates

---

## Support

- Supabase Docs: https://supabase.com/docs
- Supabase Discord: https://discord.supabase.com
- GitHub Issues: https://github.com/supabase/supabase/issues
