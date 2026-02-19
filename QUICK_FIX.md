# ⚡ Quick Fix - Render Deployment Error

## Problem
```
ModuleNotFoundError: No module named 'pkg_resources'
```

## Solution (2 minutes)

### Step 1: Update Render Build Command

1. Go to: https://dashboard.render.com
2. Click your backend service
3. Go to **Settings** tab
4. Find **Build Command** and change it to:
   ```bash
   cd backend && chmod +x build.sh && ./build.sh
   ```
5. Click **Save Changes**

### Step 2: Redeploy

1. Go to **Manual Deploy** section
2. Click **Deploy latest commit**
3. Wait 2-3 minutes

### Step 3: Verify

Visit: https://datekeeper-1.onrender.com/health

Should see: `{"status": "healthy"}`

---

## What Changed?

I fixed `requirements.txt` to install `setuptools` first, which provides `pkg_resources` needed by `razorpay`.

---

## Still Failing?

See detailed guide: [`RENDER_FIX.md`](RENDER_FIX.md)

---

**That's it! Your backend should now deploy successfully.** ✅
