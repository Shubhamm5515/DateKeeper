# GitHub Actions Setup Guide

## ✅ Configuration Complete!

Your GitHub Actions workflow is configured to keep your Render backend alive by pinging it every 10 minutes.

**Backend URL**: `https://datekeeper-1.onrender.com`

## How to Deploy

### Step 1: Commit and Push
```bash
git add .
git commit -m "Add GitHub Actions to keep backend alive"
git push origin main
```

### Step 2: Enable GitHub Actions
1. Go to your GitHub repository
2. Click on **"Actions"** tab
3. If prompted, click **"I understand my workflows, go ahead and enable them"**

### Step 3: Verify It's Working
1. Go to **Actions** tab in your GitHub repo
2. Click on **"Keep Backend Alive"** workflow
3. You should see it running every 10 minutes
4. Click on a run to see the logs

### Step 4: Manual Test (Optional)
1. Go to **Actions** tab
2. Click **"Keep Backend Alive"** workflow
3. Click **"Run workflow"** dropdown
4. Click **"Run workflow"** button
5. Watch it ping your backend in real-time!

## What It Does

The workflow:
- ✅ Runs every 10 minutes automatically
- ✅ Pings `/health` endpoint to wake up backend
- ✅ Checks `/api/scheduler/health` to verify scheduler
- ✅ Handles cold starts (waits 30s if needed)
- ✅ Shows clear status messages in logs
- ✅ Can be triggered manually anytime

## Expected Results

### Before GitHub Actions
- Backend spins down after 15 minutes
- First request takes 30-60 seconds
- Settings page is slow

### After GitHub Actions
- Backend stays warm 24/7
- All requests respond in <2 seconds
- Settings page loads instantly

## Monitoring

### Check Workflow Status
```bash
# View recent workflow runs
gh run list --workflow=keep-backend-alive.yml

# View logs of latest run
gh run view --log
```

### Check Backend Status
```bash
# Test health endpoint
curl https://datekeeper-1.onrender.com/health

# Test scheduler endpoint
curl https://datekeeper-1.onrender.com/api/scheduler/health
```

### View in Browser
- Health: https://datekeeper-1.onrender.com/health
- Scheduler: https://datekeeper-1.onrender.com/api/scheduler/health

## Troubleshooting

### Workflow Not Running?
1. Check if Actions are enabled in repo settings
2. Verify you pushed to `main` branch (not `master`)
3. Check Actions tab for error messages
4. Manually trigger workflow to test

### Backend Still Slow?
1. Wait 10-15 minutes after enabling Actions
2. Check workflow logs to verify it's pinging
3. Test backend URL directly in browser
4. Check Render dashboard for spin-down events

### Workflow Failing?
1. Check if backend URL is correct
2. Verify backend is deployed on Render
3. Check Render logs for errors
4. Try manual workflow trigger

## Cost

**GitHub Actions Free Tier:**
- 2,000 minutes/month for private repos
- Unlimited for public repos
- This workflow uses ~1 minute/day
- **Total cost: $0** ✅

## Alternative: Disable Workflow

If you want to stop the keep-alive:

```bash
# Delete the workflow file
rm .github/workflows/keep-backend-alive.yml
git add .
git commit -m "Remove keep-alive workflow"
git push
```

Or disable it in GitHub:
1. Go to Actions tab
2. Click "Keep Backend Alive"
3. Click "..." menu
4. Click "Disable workflow"

## Next Steps

1. ✅ Push changes to GitHub
2. ✅ Enable Actions in repo
3. ✅ Wait 10 minutes
4. ✅ Test Settings page - should be fast!
5. ✅ Monitor workflow runs in Actions tab

## Support

If you encounter issues:
1. Check workflow logs in Actions tab
2. Test backend URL directly
3. Review Render deployment logs
4. Check PERFORMANCE_OPTIMIZATION.md for alternatives
