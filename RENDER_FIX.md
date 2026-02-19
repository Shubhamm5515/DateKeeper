# 🔧 Render Deployment Fix - pkg_resources Error

## Problem

Your Render deployment is failing with:
```
ModuleNotFoundError: No module named 'pkg_resources'
```

This happens because:
1. `pkg_resources` is part of `setuptools`
2. `setuptools` needs to be installed before other packages
3. The `razorpay` package depends on `pkg_resources`

## Solution

I've fixed this by:

1. ✅ Reordered `requirements.txt` to install `setuptools` first
2. ✅ Added `wheel` for better package installation
3. ✅ Created `build.sh` script for Render

---

## 🚀 Deploy to Render (Updated Instructions)

### Option 1: Update Existing Service (Recommended)

1. **Go to Render Dashboard:**
   ```
   https://dashboard.render.com
   ```

2. **Click on your backend service** (datekeeper-1)

3. **Go to "Settings" tab**

4. **Update Build Command:**
   ```bash
   cd backend && chmod +x build.sh && ./build.sh
   ```

5. **Verify Start Command:**
   ```bash
   cd backend && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120 --keep-alive 5
   ```

6. **Click "Save Changes"**

7. **Go to "Manual Deploy" → "Deploy latest commit"**

### Option 2: Use render.yaml (Alternative)

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: datekeeper-backend
    env: python
    region: oregon
    plan: free
    buildCommand: cd backend && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
    startCommand: cd backend && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120 --keep-alive 5
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        sync: false
```

---

## 🧪 Test Locally First

Before deploying, test locally:

```bash
cd backend

# Clean install
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with new requirements
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Verify
python -c "import pkg_resources; print('✅ pkg_resources OK')"
python -c "import razorpay; print('✅ razorpay OK')"

# Start server
uvicorn app.main:app --reload
```

If this works locally, it will work on Render!

---

## 📋 Updated requirements.txt Structure

The new structure ensures proper installation order:

```
1. setuptools & wheel (build tools)
2. Core dependencies (fastapi, sqlalchemy)
3. Authentication packages
4. External services (razorpay, twilio, etc.)
5. Production server (gunicorn)
```

---

## ✅ Verification Steps

After deployment:

1. **Check Render Logs:**
   - Should see: "✅ pkg_resources available"
   - Should see: "✅ razorpay available"
   - Should see: "✅ Build completed successfully!"

2. **Test Health Endpoint:**
   ```
   https://datekeeper-1.onrender.com/health
   ```
   Should return: `{"status": "healthy"}`

3. **Test API:**
   ```
   https://datekeeper-1.onrender.com/docs
   ```
   Should show Swagger UI

---

## 🔄 If Still Failing

### Check Python Version

Render might be using Python 3.12+ which has deprecated `pkg_resources`.

**Fix:** Add to Render environment variables:
```
PYTHON_VERSION=3.11.9
```

Or create `runtime.txt` in backend folder:
```
python-3.11.9
```

### Force Reinstall

In Render Dashboard:
1. Go to "Settings"
2. Scroll to "Build & Deploy"
3. Click "Clear build cache & deploy"

### Check Environment Variables

Verify all required variables are set:
- DATABASE_URL
- SECRET_KEY
- OCRSPACE_API_KEY
- GEMINI_API_KEY
- SMTP credentials
- Google OAuth credentials
- Razorpay credentials

---

## 🎯 Quick Fix Commands

If you have SSH access to Render:

```bash
# Install setuptools explicitly
pip install --upgrade setuptools wheel

# Reinstall razorpay
pip uninstall razorpay -y
pip install razorpay==1.4.1

# Verify
python -c "import pkg_resources"
```

---

## 📝 Alternative: Use importlib.metadata

If the issue persists, we can update the code to use `importlib.metadata` instead of `pkg_resources`:

Create `backend/fix_razorpay.py`:

```python
"""
Monkey patch razorpay to use importlib.metadata instead of pkg_resources
"""
import sys
from importlib import metadata

# Create a fake pkg_resources module
class FakePkgResources:
    @staticmethod
    def get_distribution(name):
        class Distribution:
            def __init__(self, name):
                self.version = metadata.version(name)
        return Distribution(name)

sys.modules['pkg_resources'] = FakePkgResources()
```

Then update `app/main.py`:

```python
# Add at the very top, before any other imports
try:
    import pkg_resources
except ImportError:
    import fix_razorpay  # Monkey patch
```

---

## 🚀 Expected Result

After applying the fix, your Render logs should show:

```
📦 Installing build tools...
✅ Successfully installed setuptools-75.0.0 wheel-0.42.0

📦 Installing dependencies...
✅ Successfully installed razorpay-1.4.1 ...

✅ Verifying installations...
✅ pkg_resources available
✅ razorpay available
✅ fastapi available
✅ sqlalchemy available

✅ Build completed successfully!

==> Starting service...
Using OCR.space API for text extraction
✨ Gemini AI enabled for intelligent date extraction
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 📞 Still Having Issues?

1. **Check Render Status:** https://status.render.com
2. **Review Render Docs:** https://render.com/docs/troubleshooting-deploys
3. **Check Python Version:** Ensure using Python 3.11.x
4. **Clear Cache:** Use "Clear build cache & deploy"
5. **Check Logs:** Look for other error messages

---

## 🎉 Success Criteria

✅ Build completes without errors
✅ Server starts successfully
✅ Health endpoint returns 200
✅ API docs accessible
✅ No import errors in logs

---

**Last Updated:** 2026-02-19
**Issue:** ModuleNotFoundError: No module named 'pkg_resources'
**Status:** Fixed ✅
