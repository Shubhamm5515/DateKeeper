"""
Database Migration Script
Adds email and SMS notification fields to documents table
"""

import sqlite3
import os

DB_PATH = "documents.db"

def migrate_database():
    """Add notification fields to documents table"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(documents)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"📊 Current columns: {columns}")
        
        # Add email column if not exists
        if 'email' not in columns:
            print("➕ Adding 'email' column...")
            cursor.execute("ALTER TABLE documents ADD COLUMN email VARCHAR(255)")
            print("✅ Added 'email' column")
        else:
            print("⏭️  'email' column already exists")
        
        # Add phone column if not exists
        if 'phone' not in columns:
            print("➕ Adding 'phone' column...")
            cursor.execute("ALTER TABLE documents ADD COLUMN phone VARCHAR(20)")
            print("✅ Added 'phone' column")
        else:
            print("⏭️  'phone' column already exists")
        
        # Add notify_email column if not exists
        if 'notify_email' not in columns:
            print("➕ Adding 'notify_email' column...")
            cursor.execute("ALTER TABLE documents ADD COLUMN notify_email CHAR(1) DEFAULT 'Y'")
            print("✅ Added 'notify_email' column")
        else:
            print("⏭️  'notify_email' column already exists")
        
        # Add notify_sms column if not exists
        if 'notify_sms' not in columns:
            print("➕ Adding 'notify_sms' column...")
            cursor.execute("ALTER TABLE documents ADD COLUMN notify_sms CHAR(1) DEFAULT 'N'")
            print("✅ Added 'notify_sms' column")
        else:
            print("⏭️  'notify_sms' column already exists")
        
        conn.commit()
        
        # Verify changes
        cursor.execute("PRAGMA table_info(documents)")
        new_columns = [col[1] for col in cursor.fetchall()]
        print(f"\n📊 Updated columns: {new_columns}")
        
        conn.close()
        
        print("\n✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting database migration...\n")
    migrate_database()
