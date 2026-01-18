"""
Database Migration: Add Subscription Fields to Users Table

Adds:
- subscription_tier (free, pro, business, enterprise)
- subscription_status (active, cancelled, expired)
- razorpay_subscription_id
- document_limit (10 for free, -1 for unlimited)
"""

import sqlite3
import sys

def migrate_database():
    """Add subscription fields to users table"""
    
    try:
        # Connect to database
        conn = sqlite3.connect('documents.db')
        cursor = conn.cursor()
        
        print("🔄 Starting database migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add subscription_tier column
        if 'subscription_tier' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN subscription_tier VARCHAR(20) DEFAULT 'free'
            """)
            print("✅ Added subscription_tier column")
        else:
            print("⏭️  subscription_tier column already exists")
        
        # Add subscription_status column
        if 'subscription_status' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN subscription_status VARCHAR(20) DEFAULT 'active'
            """)
            print("✅ Added subscription_status column")
        else:
            print("⏭️  subscription_status column already exists")
        
        # Add razorpay_subscription_id column
        if 'razorpay_subscription_id' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN razorpay_subscription_id VARCHAR(255)
            """)
            print("✅ Added razorpay_subscription_id column")
        else:
            print("⏭️  razorpay_subscription_id column already exists")
        
        # Add document_limit column
        if 'document_limit' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN document_limit VARCHAR(10) DEFAULT '10'
            """)
            print("✅ Added document_limit column")
        else:
            print("⏭️  document_limit column already exists")
        
        # Commit changes
        conn.commit()
        
        # Verify migration
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print("\n📊 Current users table columns:")
        for col in columns:
            print(f"   - {col}")
        
        # Show current users
        cursor.execute("SELECT id, email, subscription_tier, subscription_status, document_limit FROM users")
        users = cursor.fetchall()
        
        if users:
            print(f"\n👥 Current users ({len(users)}):")
            for user in users:
                print(f"   - {user[1]}: {user[2]} tier, {user[3]} status, {user[4]} docs limit")
        else:
            print("\n👥 No users in database yet")
        
        conn.close()
        
        print("\n✅ Migration completed successfully!")
        print("\n📝 Next steps:")
        print("   1. Add Razorpay credentials to .env file")
        print("   2. Create plans in Razorpay Dashboard")
        print("   3. Update .env with plan IDs")
        print("   4. Install razorpay: pip install razorpay")
        print("   5. Restart backend server")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
