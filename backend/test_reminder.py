"""Test reminder system manually"""
from app.scheduler import check_expiring_documents
from app.config import settings
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 60)
print("TESTING REMINDER SYSTEM")
print("=" * 60)

print("\n📧 Email Configuration:")
print(f"SMTP Host: {settings.SMTP_HOST}")
print(f"SMTP Port: {settings.SMTP_PORT}")
print(f"SMTP User: {settings.SMTP_USER}")
print(f"SMTP Password: {'*' * len(settings.SMTP_PASSWORD) if settings.SMTP_PASSWORD else 'NOT SET'}")

print("\n🔔 Running reminder check...")
print("-" * 60)

try:
    check_expiring_documents()
    print("\n✅ Reminder check completed!")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Check your email inbox!")
print("=" * 60)
