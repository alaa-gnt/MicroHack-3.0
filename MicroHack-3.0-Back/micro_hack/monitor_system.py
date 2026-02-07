import psycopg
import redis
import json
from psycopg.rows import dict_row

DB_URI = "postgresql://postgres:password123@localhost:5432/micro_hack_db"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

def check_redis():
    print("\n--- 🔴 Redis Status ---")
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
        queue_len = r.llen("signal_queue")
        print(f"Queue 'signal_queue' length: {queue_len}")
        if queue_len > 0:
            items = r.lrange("signal_queue", 0, -1)
            print("Items in queue:")
            for item in items:
                print(f"  - {item}")
        else:
            print("Queue is empty.")
    except Exception as e:
        print(f"❌ Redis Error: {e}")

def check_postgres():
    print("\n--- 🐘 Postgres Status ---")
    try:
        with psycopg.connect(DB_URI, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        signal_id, 
                        tier_2_status, 
                        tri, 
                        feasibility_score,
                        created_at
                    FROM signals_analysis 
                    ORDER BY created_at DESC;
                """)
                rows = cur.fetchall()
                print(f"Total signals found: {len(rows)}")
                for row in rows:
                    print(f"ID: {row['signal_id']} | T1 Tri: {row['tri']} | T2 Status: {row['tier_2_status']} | T2 Feasibility: {row['feasibility_score']}")
    except Exception as e:
        print(f"❌ Postgres Error: {e}")

if __name__ == "__main__":
    check_redis()
    check_postgres()
