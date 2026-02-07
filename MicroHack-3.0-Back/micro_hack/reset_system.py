import psycopg
import redis

DB_URI = "postgresql://postgres:password123@127.0.0.1:5432/micro_hack_db"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

def reset_all():
    print("🧹 Resetting system for clean test...")
    
    # 1. Clear Redis
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        r.delete("signal_queue")
        print("✅ Redis queue 'signal_queue' cleared.")
    except Exception as e:
        print(f"❌ Redis Reset Error: {e}")

    # 2. Reset Postgres (Signals)
    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE signals_analysis SET tier_2_status = 'pending', feasibility_score = NULL, tech_assessment = NULL, tech_stack = NULL, market_analysis = NULL, recommendation = NULL;")
                print(f"✅ Postgres signals reset ({cur.rowcount} rows).")
                
                # Also truncate checkpoints to be safe
                cur.execute("TRUNCATE checkpoints, checkpoint_blobs, checkpoint_writes;")
                print("✅ Postgres checkpoints truncated.")
    except Exception as e:
        print(f"❌ Postgres Reset Error: {e}")

if __name__ == "__main__":
    reset_all()
