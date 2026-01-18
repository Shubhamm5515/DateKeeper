"""Check database data for debugging"""
from app.database import SessionLocal
from app.models.document import Document
from app.models.user import User

db = SessionLocal()

print("=" * 60)
print("USERS IN DATABASE")
print("=" * 60)
users = db.query(User).all()
for u in users:
    print(f"ID: {u.id}")
    print(f"Email: {u.email}")
    print(f"Name: {u.full_name}")
    print(f"Notify Email: {u.notify_email}")
    print(f"Notify SMS: {u.notify_sms}")
    print("-" * 60)

print("\n" + "=" * 60)
print("DOCUMENTS IN DATABASE")
print("=" * 60)
docs = db.query(Document).all()
for d in docs:
    print(f"ID: {d.id}")
    print(f"Name: {d.document_name}")
    print(f"Type: {d.document_type}")
    print(f"Expiry: {d.expiry_date}")
    print(f"Email: {d.email}")
    print(f"Phone: {d.phone}")
    print(f"Notify Email: {d.notify_email}")
    print(f"Notify SMS: {d.notify_sms}")
    print(f"User ID: {d.user_id}")
    print(f"Status: {d.status}")
    print("-" * 60)

db.close()

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total Users: {len(users)}")
print(f"Total Documents: {len(docs)}")
print(f"Documents with email: {sum(1 for d in docs if d.email)}")
print(f"Documents with notify_email='Y': {sum(1 for d in docs if d.notify_email == 'Y')}")
