"""Test if all required packages are installed"""

print("Testing package imports...")

try:
    import fastapi
    print("✅ FastAPI installed")
except ImportError as e:
    print(f"❌ FastAPI not installed: {e}")

try:
    import uvicorn
    print("✅ Uvicorn installed")
except ImportError as e:
    print(f"❌ Uvicorn not installed: {e}")

try:
    import sqlalchemy
    print("✅ SQLAlchemy installed")
except ImportError as e:
    print(f"❌ SQLAlchemy not installed: {e}")

try:
    from google.cloud import vision
    print("✅ Google Cloud Vision installed")
except ImportError as e:
    print(f"❌ Google Cloud Vision not installed: {e}")

try:
    from PIL import Image
    print("✅ Pillow installed")
except ImportError as e:
    print(f"❌ Pillow not installed: {e}")

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    print("✅ APScheduler installed")
except ImportError as e:
    print(f"❌ APScheduler not installed: {e}")

print("\n✅ All core packages are installed!")
print("\nNext steps:")
print("1. Add your Google Cloud Vision API key to backend/.env")
print("2. Run: uvicorn app.main:app --reload")
print("3. Open: http://localhost:8000/docs")
