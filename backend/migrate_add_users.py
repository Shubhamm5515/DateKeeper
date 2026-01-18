"""
Database Migration - Add Users Table
Creates users table for authentication
"""

import sqlite3
import os

DB_PATH = "documents.db"

def migrate_add_users_table():
    """Create users table"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if users table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            print("⏭️  Users table already exists")
            conn.close()
            return True
        
        print("➕ Creating users table...")
        
        # Create users table
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
        
        # Verify table was created
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print(f"✅ Users table created with {len(columns)} columns")
        print(f"   Columns: {[col[1] for col in columns]}")
        
        conn.close()
        
        print("\n✅ Migration completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Restart backend")
        print("   2. Users can now register/login")
        print("   3. Documents will use user's email for notifications")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting database migration - Add Users Table...\n")
    migrate_add_users_table()
