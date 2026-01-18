"""
Database Migration Script - Create Users Table
"""

import sqlite3
import os

DB_PATH = "documents.db"

def create_users_table():
    """Create users table for authentication"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            print("⏭️  'users' table already exists")
            conn.close()
            return True
        
        # Create users table
        print("➕ Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                full_name TEXT,
                phone TEXT,
                notify_email TEXT DEFAULT 'Y',
                notify_sms TEXT DEFAULT 'N',
                is_active BOOLEAN DEFAULT 1,
                is_verified BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on email
        cursor.execute("CREATE INDEX idx_users_email ON users(email)")
        
        conn.commit()
        print("✅ Created 'users' table")
        
        # Verify
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"📊 Users table columns: {columns}")
        
        conn.close()
        
        print("\n✅ Users table migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting users table migration...\n")
    create_users_table()
