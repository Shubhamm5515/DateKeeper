"""
Database Migration: Add reminder settings to users table

Adds:
- alternate_email: Optional alternate email for reminders
- reminder_intervals: JSON field for enabled reminder intervals
"""

import sqlite3
import json

# Connect to database
conn = sqlite3.connect('documents.db')
cursor = conn.cursor()

print("=" * 60)
print("DATABASE MIGRATION: Add Reminder Settings")
print("=" * 60)

try:
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add alternate_email column if it doesn't exist
    if 'alternate_email' not in columns:
        print("\n✅ Adding 'alternate_email' column...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN alternate_email TEXT
        """)
        print("   Column 'alternate_email' added successfully")
    else:
        print("\n⏭️  Column 'alternate_email' already exists")
    
    # Add reminder_intervals column if it doesn't exist
    if 'reminder_intervals' not in columns:
        print("\n✅ Adding 'reminder_intervals' column...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN reminder_intervals TEXT
        """)
        print("   Column 'reminder_intervals' added successfully")
        
        # Set default values for existing users
        default_intervals = json.dumps({
            "6_months": True,
            "3_months": True,
            "1_month": True,
            "7_days": True
        })
        
        cursor.execute("""
            UPDATE users 
            SET reminder_intervals = ? 
            WHERE reminder_intervals IS NULL
        """, (default_intervals,))
        
        print(f"   Set default reminder intervals for {cursor.rowcount} users")
    else:
        print("\n⏭️  Column 'reminder_intervals' already exists")
    
    # Commit changes
    conn.commit()
    
    # Verify migration
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    
    print("\nUsers table columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Show sample data
    cursor.execute("SELECT id, email, alternate_email, reminder_intervals FROM users LIMIT 3")
    users = cursor.fetchall()
    
    if users:
        print("\nSample user data:")
        for user in users:
            print(f"\n  User: {user[1]}")
            print(f"  Alternate Email: {user[2] or 'Not set'}")
            print(f"  Reminder Intervals: {user[3] or 'Not set'}")
    
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
except sqlite3.Error as e:
    print(f"\n❌ Migration failed: {e}")
    conn.rollback()
finally:
    conn.close()

print("\nYou can now:")
print("1. Restart the backend server")
print("2. Use the Settings page to configure reminders")
print("3. Set alternate email for notifications")
