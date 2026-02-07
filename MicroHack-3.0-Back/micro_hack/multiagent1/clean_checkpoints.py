#!/usr/bin/env python3
"""Clean corrupted checkpoint data from PostgreSQL"""
import psycopg

DB_URI = "postgresql://postgres:password123@127.0.0.1:5432/micro_hack_db"

def clean_checkpoints():
    print("Connecting to database...")
    with psycopg.connect(DB_URI, autocommit=True) as conn:
        with conn.cursor() as cur:
            # List all tables
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = [row[0] for row in cur.fetchall()]
            print(f'Tables found: {tables}')
            
            # Find and clean checkpoint tables
            cleaned = 0
            for t in tables:
                if 'checkpoint' in t.lower():
                    print(f'Truncating {t}...')
                    cur.execute(f'TRUNCATE TABLE {t} CASCADE;')
                    cleaned += 1
                    print(f'  ✓ Done.')
            
            if cleaned == 0:
                print("No checkpoint tables found to clean.")
            else:
                print(f"\n✅ Cleaned {cleaned} checkpoint table(s)!")

if __name__ == "__main__":
    clean_checkpoints()
