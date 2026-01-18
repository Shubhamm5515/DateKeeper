"""Create test documents that will trigger reminders"""
from app.database import SessionLocal
from app.models.document import Document
from app.models.user import User
from datetime import datetime, timedelta
import uuid

db = SessionLocal()

# Get first user
user = db.query(User).first()
if not user:
    print("❌ No users found! Please register first.")
    exit(1)

print(f"Creating test documents for user: {user.email}")
print("=" * 60)

# Calculate dates that will trigger reminders
today = datetime.now().date()
test_dates = [
    (today + timedelta(days=7), "7 days", "7_days"),
    (today + timedelta(days=30), "1 month", "1_month"),
    (today + timedelta(days=90), "3 months", "3_months"),
    (today + timedelta(days=180), "6 months", "6_months"),
]

for expiry_date, label, reminder_type in test_dates:
    doc = Document(
        id=str(uuid.uuid4()),
        user_id=user.id,
        document_name=f"Test Document ({label})",
        document_type="passport",
        expiry_date=expiry_date,
        status="valid",
        email=user.email,
        phone=user.phone,
        notify_email="Y",
        notify_sms="N",
        reminder_sent={}
    )
    db.add(doc)
    print(f"✅ Created: {doc.document_name} - Expires: {expiry_date}")

db.commit()
db.close()

print("\n" + "=" * 60)
print("Test documents created!")
print("Now run: python test_reminder.py")
print("=" * 60)
