"""
Test Supabase PostgreSQL Connection
Verifies database connection and schema
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test Supabase database connection"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    if 'sqlite' in database_url.lower():
        print("⚠️  DATABASE_URL is pointing to SQLite, not Supabase")
        return False
    
    print("🔄 Testing Supabase connection...")
    print(f"   Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'unknown'}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            # Get PostgreSQL version
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"\n✅ Connection successful!")
            print(f"   PostgreSQL Version: {version.split(',')[0]}")
            
            # Check if tables exist
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            
            print(f"\n📊 Tables found: {len(tables)}")
            for table in tables:
                # Count rows in each table
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = count_result.fetchone()[0]
                print(f"   - {table}: {count} rows")
            
            # Check required tables
            required_tables = ['users', 'documents']
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                print(f"\n⚠️  Missing tables: {missing_tables}")
                print("   Run: python supabase_migrate.py")
                return False
            
            # Check indexes
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM pg_indexes 
                WHERE schemaname = 'public'
            """))
            index_count = result.fetchone()[0]
            print(f"\n🔍 Indexes: {index_count}")
            
            # Check triggers
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.triggers 
                WHERE trigger_schema = 'public'
            """))
            trigger_count = result.fetchone()[0]
            print(f"⚡ Triggers: {trigger_count}")
            
            print("\n" + "="*60)
            print("✅ ALL CHECKS PASSED!")
            print("="*60)
            print("\n💡 Your Supabase database is ready to use!")
            print("   Start backend: uvicorn app.main:app --reload")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check DATABASE_URL in .env file")
        print("   2. Verify Supabase project is active")
        print("   3. Check password is correct")
        print("   4. Try adding ?sslmode=require to connection string")
        print("   5. Check Supabase Dashboard → Settings → Database")
        return False

if __name__ == "__main__":
    print("="*60)
    print("SUPABASE CONNECTION TEST")
    print("="*60)
    print()
    
    success = test_connection()
    sys.exit(0 if success else 1)
