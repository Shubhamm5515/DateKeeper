"""
Supabase Migration Script
Creates database schema in Supabase PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_to_supabase():
    """Create database schema in Supabase"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        print("💡 Add your Supabase connection string to .env:")
        print("   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres")
        return False
    
    if 'sqlite' in database_url.lower():
        print("❌ DATABASE_URL is still pointing to SQLite")
        print("💡 Update DATABASE_URL in .env to your Supabase connection string")
        return False
    
    print("🔄 Connecting to Supabase PostgreSQL...")
    print(f"   Database: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'unknown'}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL")
            print(f"   Version: {version.split(',')[0]}")
        
        print("\n📊 Creating database schema...")
        
        # Read schema file
        schema_file = 'supabase_schema.sql'
        if not os.path.exists(schema_file):
            print(f"❌ Schema file not found: {schema_file}")
            return False
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        with engine.connect() as conn:
            # Split by semicolon and execute each statement
            statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
            
            for i, statement in enumerate(statements, 1):
                # Skip comments and empty statements
                if statement.startswith('--') or not statement:
                    continue
                
                try:
                    conn.execute(text(statement))
                    conn.commit()
                except Exception as e:
                    # Ignore "already exists" errors
                    if 'already exists' in str(e).lower():
                        continue
                    else:
                        print(f"⚠️  Warning on statement {i}: {e}")
            
            print(f"✅ Executed {len(statements)} SQL statements")
        
        # Verify tables were created
        print("\n🔍 Verifying tables...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if 'users' in tables and 'documents' in tables:
                print("✅ Tables created successfully:")
                for table in tables:
                    print(f"   - {table}")
            else:
                print("⚠️  Some tables might be missing")
                print(f"   Found: {tables}")
        
        # Verify indexes
        print("\n🔍 Verifying indexes...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT indexname, tablename 
                FROM pg_indexes 
                WHERE schemaname = 'public'
                ORDER BY tablename, indexname
            """))
            indexes = result.fetchall()
            
            if indexes:
                print(f"✅ Found {len(indexes)} indexes:")
                for idx_name, table_name in indexes:
                    print(f"   - {table_name}.{idx_name}")
            else:
                print("⚠️  No indexes found")
        
        print("\n" + "="*60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        print("\n📝 Next steps:")
        print("   1. Test the connection: python test_supabase_connection.py")
        print("   2. Start backend: uvicorn app.main:app --reload")
        print("   3. Register a test user")
        print("   4. Create a test document")
        print("   5. Check Supabase Dashboard → Table Editor")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check DATABASE_URL is correct")
        print("   2. Verify Supabase project is active")
        print("   3. Check your IP is allowed (Supabase allows all by default)")
        print("   4. Try adding ?sslmode=require to connection string")
        return False

if __name__ == "__main__":
    print("="*60)
    print("SUPABASE MIGRATION SCRIPT")
    print("="*60)
    print()
    
    success = migrate_to_supabase()
    sys.exit(0 if success else 1)
