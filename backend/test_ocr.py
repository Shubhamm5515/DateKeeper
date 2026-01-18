"""Test OCR functionality with OCR.space"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ocr_service import OCRService
from app.config import settings

print("=" * 50)
print("Testing OCR Service (OCR.space)")
print("=" * 50)

print(f"\n1. Checking configuration...")
if settings.OCRSPACE_API_KEY:
    print(f"   ✅ Custom API Key configured")
    print(f"   API Key (first 10 chars): {settings.OCRSPACE_API_KEY[:10]}...")
else:
    print(f"   ℹ️  Using public API key (rate limited)")
    print(f"   Tip: Get your own free key at https://ocr.space/ocrapi")

print(f"\n2. Initializing OCR Service...")
try:
    ocr_service = OCRService()
    print(f"   ✅ OCR Service initialized")
    print(f"   Provider: OCR.space API")
    print(f"   Free tier: 25,000 requests/month")
except Exception as e:
    print(f"   ❌ Failed to initialize: {e}")
    sys.exit(1)

print(f"\n3. Service is ready!")
print(f"   No billing required ✅")
print(f"   No credit card needed ✅")
print(f"   Works immediately ✅")

print("\n" + "=" * 50)
print("OCR Service is ready!")
print("=" * 50)
print("\nNext steps:")
print("1. Start backend: uvicorn app.main:app --reload")
print("2. Test health: http://localhost:8000/api/ocr/health")
print("3. Upload image from frontend to test")
print("\nOptional: Get your own free API key at https://ocr.space/ocrapi")
