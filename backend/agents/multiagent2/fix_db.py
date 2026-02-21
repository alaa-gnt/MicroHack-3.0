import psycopg
import sys

# Flush stdout
def log(msg):
    print(msg)
    sys.stdout.flush()

DB_URI = "postgresql://postgres:password123@127.0.0.1:5432/micro_hack_db"

def fix_signals():
    log("Starting DB Fix...")
    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            with conn.cursor() as cur:
                log("Executing UPDATE...")
                cur.execute("UPDATE signals_analysis SET tier_2_status = 'pending';")
                log(f"Updated {cur.rowcount} rows.")
    except Exception as e:
        log(f"Error: {e}")

if __name__ == "__main__":
    fix_signals()
