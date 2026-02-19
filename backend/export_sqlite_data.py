"""
Export SQLite Data to SQL File
Use this to export your existing SQLite data before migrating to Supabase
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = "documents.db"
OUTPUT_FILE = f"sqlite_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

def export_sqlite_data():
    """Export SQLite database to SQL file"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        print("💡 No data to export. You can start fresh with Supabase!")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            print("⚠️  No tables found in database")
            conn.close()
            return False
        
        print(f"📊 Found tables: {tables}")
        
        # Open output file
        with open(OUTPUT_FILE, 'w') as f:
            f.write("-- SQLite Data Export\n")
            f.write(f"-- Generated: {datetime.now().isoformat()}\n")
            f.write("-- Database: documents.db\n\n")
            
            # Export each table
            for table in tables:
                if table.startswith('sqlite_'):
                    continue
                
                print(f"\n📋 Exporting table: {table}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   Rows: {count}")
                
                if count == 0:
                    continue
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]
                
                # Write table header
                f.write(f"\n-- Table: {table} ({count} rows)\n")
                f.write(f"-- Columns: {', '.join(columns)}\n\n")
                
                # Get all rows
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                # Write INSERT statements
                for row in rows:
                    # Format values
                    values = []
                    for val in row:
                        if val is None:
                            values.append('NULL')
                        elif isinstance(val, str):
                            # Escape single quotes
                            escaped = val.replace("'", "''")
                            values.append(f"'{escaped}'")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        else:
                            values.append(f"'{val}'")
                    
                    insert_sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
                    f.write(insert_sql)
                
                f.write("\n")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ EXPORT COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📄 Output file: {OUTPUT_FILE}")
        print(f"   Size: {os.path.getsize(OUTPUT_FILE)} bytes")
        
        print("\n📝 Next steps:")
        print("   1. Review the exported SQL file")
        print("   2. Set up Supabase database")
        print("   3. Run: python supabase_migrate.py")
        print("   4. Import data using Supabase SQL Editor:")
        print(f"      - Open {OUTPUT_FILE}")
        print("      - Copy and paste into SQL Editor")
        print("      - Click 'Run'")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Export failed: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("SQLITE DATA EXPORT")
    print("="*60)
    print()
    
    export_sqlite_data()
