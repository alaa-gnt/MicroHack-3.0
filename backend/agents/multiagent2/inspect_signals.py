import psycopg
from psycopg.rows import dict_row
import sys

# Flush stdout to ensure logs appear immediately
def log(msg):
    print(msg)
    sys.stdout.flush()

DB_URI = "postgresql://postgres:password123@127.0.0.1:5432/micro_hack_db"

def inspect_signals():
    log("Starting inspection...")
    try:
        log(f"Connecting to {DB_URI}...")
        with psycopg.connect(DB_URI, row_factory=dict_row) as conn:
            log("Connected.")
            with conn.cursor() as cur:
                log("Executing query...")
                cur.execute("SELECT signal_id, tier_2_status FROM signals_analysis;")
                rows = cur.fetchall()
                log(f"Found {len(rows)} rows.")
                print("Signal Statuses:")
                for row in rows:
                    print(row)
                    sys.stdout.flush()
    except Exception as e:
        log(f"Error: {e}")

if __name__ == "__main__":
    inspect_signals()
