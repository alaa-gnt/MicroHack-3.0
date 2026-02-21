import psycopg

DB_URI = "postgresql://postgres:password123@localhost:5432/micro_hack_db"

def inspect_db():
    try:
        with psycopg.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                print("Checking tables...")
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cur.fetchall()
                print("Tables:", tables)

                for table in tables:
                    t_name = table[0]
                    cur.execute(f"SELECT COUNT(*) FROM {t_name}")
                    count = cur.fetchone()[0]
                    print(f"Table '{t_name}' row count: {count}")
                    
                    # If it's a checkpoint table, maybe check size
                    if "checkpoint" in t_name:
                         # Truncate?
                         pass

                # Assuming standard langgraph tables: checkpoints, checkpoint_blobs, checkpoint_writes
                # checkpoints has column 'metadata', 'checkpoint' (bytea or jsonb)
                
    except Exception as e:
        print("Error inspecting DB:", e)

def truncate_checkpoints():
    print("\nTrucating checkpoint tables...")
    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            with conn.cursor() as cur:
                # Common tables created by PostgresSaver
                cur.execute("TRUNCATE TABLE checkpoints, checkpoint_blobs, checkpoint_writes RESTART IDENTITY CASCADE;")
                print("✅ Checkpoint tables truncated.")
    except Exception as e:
         # It might fail if tables don't exist or have different names, but let's try.
         print(f"❌ Error truncating: {e}")
         # Attempt to drop them if truncate fails?
         try:
            with psycopg.connect(DB_URI, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute("DROP TABLE IF EXISTS checkpoints, checkpoint_blobs, checkpoint_writes CASCADE;")
                    print("✅ Checkpoint tables dropped.")
         except Exception as e2:
             print(f"❌ Error dropping: {e2}")

if __name__ == "__main__":
    inspect_db()
    truncate_checkpoints()
