# Deployment Checklist

## ✅ GitHub Actions Keep-Alive Setup

### 1. Commit Changes
```bash
git add .
git commit -m "Add GitHub Actions keep-alive and performance optimizations"
git push origin main
```

### 2. Enable GitHub Actions
- Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
- Click "I understand my workflows, go ahead and enable them" (if needed)
- Workflow will start automatically

### 3. Test Manually (Optional)
- Go to Actions tab
- Click "Keep Backend Alive"
- Click "Run workflow" → "Run workflow"
- Watch the logs to verify it works

### 4. Verify Backend
```bash
# Test health endpoint
curl https://datekeeper-1.onrender.com/health

# Should return:
# {"status":"healthy","environment":"production"}
```

### 5. Deploy Backend Changes
Your backend has these optimizations:
- ✅ 2 workers instead of 1 (better performance)
- ✅ Increased timeout to 120s
- ✅ Keep-alive connections enabled
- ✅ Response caching on settings endpoint

**Deploy to Render:**
- Render auto-deploys from GitHub
- Or manually trigger in Render dashboard
- Wait 2-3 minutes for deployment

### 6. Update Frontend Environment
If deploying to production, update Vercel environment variables:

**Vercel Dashboard → Settings → Environment Variables:**
```
VITE_API_URL=https://datekeeper-1.onrender.com
```

Then redeploy frontend:
```bash
# Vercel will auto-deploy from GitHub
# Or trigger manually in Vercel dashboard
```

### 7. Test Settings Page
1. Login to your app
2. Go to Settings page
3. Should load in <2 seconds (after GitHub Actions starts)
4. First load might still be slow (wait 10 minutes for Actions to kick in)

## Timeline

| Time | What Happens |
|------|--------------|
| 0 min | Push to GitHub |
| 1 min | GitHub Actions workflow created |
| 2 min | Backend deploys on Render |
| 10 min | First keep-alive ping runs |
| 20 min | Second keep-alive ping runs |
| 30 min | Backend stays warm consistently |

## Verification

### Check GitHub Actions
```bash
# View workflow runs
gh run list --workflow=keep-backend-alive.yml

# Or visit:
# https://github.com/YOUR_USERNAME/YOUR_REPO/actions
```

### Check Backend Status
```bash
# Health check
curl https://datekeeper-1.onrender.com/health

# Scheduler check
curl https://datekeeper-1.onrender.com/api/scheduler/health
```

### Monitor Render
- Go to Render dashboard
- Check "Events" tab
- Should see regular requests every 10 minutes
- No more "Spinning down" events

## Expected Performance

### Before Optimization
- ❌ Settings page: 30-60 seconds (cold start)
- ❌ Backend spins down after 15 minutes
- ❌ Poor user experience

### After Optimization
- ✅ Settings page: <2 seconds
- ✅ Backend stays warm 24/7
- ✅ Great user experience

## Troubleshooting

### Settings Still Slow?
1. Wait 15-20 minutes after enabling Actions
2. Check Actions tab - verify workflow is running
3. Check Render logs - verify requests are coming in
4. Test backend URL directly in browser

### GitHub Actions Not Running?
1. Verify Actions are enabled in repo settings
2. Check if you're on `main` branch (not `master`)
3. Manually trigger workflow to test
4. Check workflow file syntax

### Backend Errors?
1. Check Render deployment logs
2. Verify environment variables are set
3. Check database connection
4. Review recent code changes

## Rollback Plan

If something breaks:

```bash
# Revert changes
git revert HEAD
git push origin main

# Or disable workflow
# Go to Actions → Keep Backend Alive → ... → Disable workflow
```

## Cost Summary

| Service | Plan | Cost |
|---------|------|------|
| GitHub Actions | Free | $0 |
| Render Backend | Free | $0 |
| Vercel Frontend | Free | $0 |
| **Total** | | **$0/month** |

## Next Steps

1. ✅ Push changes to GitHub
2. ✅ Enable Actions
3. ✅ Wait 10-15 minutes
4. ✅ Test Settings page
5. ✅ Monitor for 24 hours
6. ✅ Celebrate faster app! 🎉

## Future Improvements

When ready to scale:
- Upgrade Render to paid plan ($7/month) for guaranteed uptime
- Add Redis caching for even faster responses
- Implement service workers for offline support
- Add performance monitoring (Sentry, LogRocket)
