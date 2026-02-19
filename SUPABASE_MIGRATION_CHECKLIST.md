# Supabase Migration Checklist

Complete checklist for migrating from Render PostgreSQL to Supabase.

## Pre-Migration

- [ ] **Backup existing data** (if you have any)
  ```bash
  cd backend
  python export_sqlite_data.py
  ```
  - This creates a SQL backup file with timestamp
  - Save this file in a safe location

- [ ] **Review current database**
  ```bash
  python check_data.py
  ```
  - Note how many users and documents you have
  - Take screenshots if needed

## Supabase Setup

- [ ] **Create Supabase account**
  - Go to https://supabase.com
  - Sign up with email or GitHub

- [ ] **Create new project**
  - Project name: `datekeeper` (or your choice)
  - Database password: Generate strong password
  - Region: Choose closest to your users
  - Plan: Free tier (500MB database)
  - Wait 2-3 minutes for provisioning

- [ ] **Get connection details**
  - Dashboard → Settings → Database
  - Copy "Connection string" (URI format)
  - Save password securely (you'll need it!)

## Backend Configuration

- [ ] **Update .env file**
  ```bash
  # Edit backend/.env
  DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
  ```
  - Replace `[PASSWORD]` with your actual password
  - Keep the rest of the connection string as-is

- [ ] **Test connection**
  ```bash
  cd backend
  python test_supabase_connection.py
  ```
  - Should see: ✅ Connection successful!

- [ ] **Run migration**
  ```bash
  python supabase_migrate.py
  ```
  - Creates users and documents tables
  - Sets up indexes and triggers
  - Should see: ✅ MIGRATION COMPLETED SUCCESSFULLY!

- [ ] **Verify schema**
  - Go to Supabase Dashboard → Table Editor
  - Check `users` table exists
  - Check `documents` table exists
  - Verify columns match your models

## Data Migration (If you have existing data)

- [ ] **Import data to Supabase**
  - Option A: Using SQL Editor
    - Dashboard → SQL Editor → New query
    - Paste contents of your backup SQL file
    - Click "Run"
  
  - Option B: Using psql
    ```bash
    psql [SUPABASE_CONNECTION_STRING] < sqlite_export_*.sql
    ```

- [ ] **Verify data imported**
  - Dashboard → Table Editor → users
  - Check row count matches
  - Dashboard → Table Editor → documents
  - Check row count matches

## Testing

- [ ] **Test backend locally**
  ```bash
  cd backend
  uvicorn app.main:app --reload
  ```
  - Visit: http://localhost:8000/health
  - Should see: `{"status": "healthy"}`

- [ ] **Test user registration**
  - Start frontend: `cd frontend && npm run dev`
  - Register a new test user
  - Check Supabase Dashboard → Table Editor → users
  - Verify user was created

- [ ] **Test document creation**
  - Create a test document
  - Check Supabase Dashboard → Table Editor → documents
  - Verify document was created

- [ ] **Test authentication**
  - Logout and login again
  - Verify JWT tokens work
  - Check documents are user-scoped

- [ ] **Test OCR functionality**
  - Upload a document image
  - Verify OCR extracts expiry date
  - Check document is saved to Supabase

- [ ] **Test notifications**
  ```bash
  python test_reminder.py
  ```
  - Verify email notifications work
  - Check scheduler can access database

## Production Deployment

- [ ] **Update Render environment variables**
  - Go to Render Dashboard → Your backend service
  - Environment tab
  - Update `DATABASE_URL` with Supabase connection string
  - Click "Save Changes"
  - Wait for automatic redeploy

- [ ] **Test production backend**
  - Visit: https://your-backend.onrender.com/health
  - Should see: `{"status": "healthy"}`

- [ ] **Test production frontend**
  - Visit your Vercel frontend URL
  - Register a new user
  - Create a document
  - Verify everything works

- [ ] **Monitor for errors**
  - Check Render logs for any database errors
  - Check Supabase Dashboard → Logs
  - Monitor for 24 hours

## Post-Migration

- [ ] **Enable Supabase features**
  - [ ] Set up automatic backups
    - Dashboard → Database → Backups
    - Enable daily backups
  
  - [ ] Enable Row Level Security (optional)
    - Dashboard → Authentication → Policies
    - See `supabase_schema.sql` for RLS policies
  
  - [ ] Set up monitoring
    - Dashboard → Reports
    - Monitor query performance
    - Set up alerts

- [ ] **Optimize performance**
  - [ ] Enable connection pooling
    - Update DATABASE_URL to use pooler URL
    - Get from: Settings → Database → Connection Pooling
  
  - [ ] Add additional indexes if needed
    - Monitor slow queries in Dashboard → Database → Query Performance
    - Add indexes for frequently queried columns

- [ ] **Update documentation**
  - [ ] Update README.md with Supabase setup
  - [ ] Update deployment docs
  - [ ] Document connection string format

- [ ] **Clean up old database**
  - [ ] Verify Supabase is working for 1 week
  - [ ] Delete Render PostgreSQL database (if applicable)
  - [ ] Delete local SQLite file (keep backup!)
  - [ ] Remove old database credentials from .env

## Rollback Plan (If something goes wrong)

- [ ] **Keep old database running** for 1 week
- [ ] **Keep backup SQL file** safe
- [ ] **Document any issues** encountered
- [ ] **To rollback:**
  ```bash
  # Restore old DATABASE_URL in .env
  DATABASE_URL=sqlite:///./documents.db  # or old Render URL
  
  # Restart backend
  uvicorn app.main:app --reload
  ```

## Success Criteria

✅ All tests passing
✅ Users can register and login
✅ Documents can be created and viewed
✅ OCR functionality works
✅ Notifications work
✅ Production deployment successful
✅ No errors in logs for 24 hours
✅ Performance is good (no slow queries)

## Estimated Time

- Supabase setup: 5 minutes
- Backend configuration: 5 minutes
- Schema migration: 2 minutes
- Data migration: 5-30 minutes (depends on data size)
- Testing: 15 minutes
- Production deployment: 10 minutes
- Monitoring: 24 hours

**Total active time: ~45 minutes**

## Support Resources

- **Quick Start**: See `backend/SUPABASE_QUICKSTART.md`
- **Detailed Guide**: See `SUPABASE_MIGRATION_GUIDE.md`
- **Supabase Docs**: https://supabase.com/docs
- **Supabase Discord**: https://discord.supabase.com
- **GitHub Issues**: https://github.com/supabase/supabase/issues

## Notes

- Supabase free tier includes:
  - 500MB database storage
  - 2GB bandwidth
  - 50MB file storage
  - Unlimited API requests
  - Daily automatic backups

- No credit card required for free tier
- Can upgrade to Pro ($25/month) if needed
- Much better than Render free tier (no cold starts!)

---

**Last Updated**: 2026-02-19
