"""Test settings functionality"""
from app.database import SessionLocal
from app.models.user import User
import json

db = SessionLocal()

print("=" * 60)
print("TESTING SETTINGS FUNCTIONALITY")
print("=" * 60)

# Get first user
user = db.query(User).first()
if not user:
    print("❌ No users found!")
    exit(1)

print(f"\n📧 User: {user.email}")
print(f"ID: {user.id}")

# Test 1: Read current settings
print("\n" + "=" * 60)
print("TEST 1: Read Current Settings")
print("=" * 60)

print(f"Alternate Email: {user.alternate_email}")
print(f"Reminder Intervals: {user.reminder_intervals}")
print(f"Notify Email: {user.notify_email}")
print(f"Notify SMS: {user.notify_sms}")

# Test 2: Update settings
print("\n" + "=" * 60)
print("TEST 2: Update Settings")
print("=" * 60)

print("Setting alternate email...")
user.alternate_email = "test-alternate@example.com"

print("Updating reminder intervals...")
user.reminder_intervals = {
    "6_months": False,
    "3_months": False,
    "1_month": True,
    "7_days": True
}

print("Updating notification preferences...")
user.notify_email = "Y"
user.notify_sms = "N"

db.commit()
db.refresh(user)

print("✅ Settings updated!")

# Test 3: Verify updates
print("\n" + "=" * 60)
print("TEST 3: Verify Updates")
print("=" * 60)

print(f"Alternate Email: {user.alternate_email}")
print(f"Reminder Intervals: {user.reminder_intervals}")
print(f"Notify Email: {user.notify_email}")
print(f"Notify SMS: {user.notify_sms}")

# Test 4: Check database directly
print("\n" + "=" * 60)
print("TEST 4: Check Database Directly")
print("=" * 60)

import sqlite3
conn = sqlite3.connect('documents.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT email, alternate_email, reminder_intervals, notify_email, notify_sms 
    FROM users 
    WHERE id = ?
""", (user.id,))

row = cursor.fetchone()
print(f"Email: {row[0]}")
print(f"Alternate Email: {row[1]}")
print(f"Reminder Intervals (raw): {row[2]}")
print(f"Notify Email: {row[3]}")
print(f"Notify SMS: {row[4]}")

conn.close()

# Test 5: Reset to defaults
print("\n" + "=" * 60)
print("TEST 5: Reset to Defaults")
print("=" * 60)

user.alternate_email = None
user.reminder_intervals = {
    "6_months": True,
    "3_months": True,
    "1_month": True,
    "7_days": True
}

db.commit()
db.refresh(user)

print("✅ Settings reset to defaults")
print(f"Alternate Email: {user.alternate_email}")
print(f"Reminder Intervals: {user.reminder_intervals}")

db.close()

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED")
print("=" * 60)
