"""
Remove razorpay_subscription_id column from users table
"""

import sqlite3
import sys

def remove_razorpay_column():
    """Remove razorpay_subscription_id column"""
    
    try:
        conn = sqlite3.connect('documents.db')
        cursor = conn.cursor()
        
        print("🔄 Removing razorpay_subscription_id column...")
        
        # SQLite doesn't support DROP COLUMN directly
        # We need to recreate the table without that column
        
        # Get current table schema
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        # Check if razorpay_subscription_id exists
        has_razorpay = any(col[1] == 'razorpay_subscription_id' for col in columns)
        
        if not has_razorpay:
            print("⏭️  razorpay_subscription_id column doesn't exist")
            conn.close()
            return True
        
        # Create new table without razorpay_subscription_id
        cursor.execute("""
            CREATE TABLE users_new (
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                alternate_email TEXT,
                reminder_intervals TEXT,
                subscription_tier TEXT DEFAULT 'free',
                subscription_status TEXT DEFAULT 'active',
                document_limit TEXT DEFAULT '10'
            )
        """)
        
        # Copy data (excluding razorpay_subscription_id)
        cursor.execute("""
            INSERT INTO users_new 
            SELECT id, email, hashed_password, full_name, phone, 
                   notify_email, notify_sms, is_active, is_verified,
                   created_at, updated_at, alternate_email, reminder_intervals,
                   subscription_tier, subscription_status, document_limit
            FROM users
        """)
        
        # Drop old table
        cursor.execute("DROP TABLE users")
        
        # Rename new table
        cursor.execute("ALTER TABLE users_new RENAME TO users")
        
        # Recreate index
        cursor.execute("CREATE INDEX idx_users_email ON users(email)")
        
        conn.commit()
        
        print("✅ Removed razorpay_subscription_id column")
        
        # Verify
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"\n📊 Updated columns: {len(columns)}")
        for col in columns:
            print(f"   - {col}")
        
        conn.close()
        
        print("\n✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = remove_razorpay_column()
    sys.exit(0 if success else 1)
