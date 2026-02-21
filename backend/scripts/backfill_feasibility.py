import psycopg
import redis
import json
from psycopg.rows import dict_row

DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def backfill():
    print("🔄 Starting Feasibility Study Backfill...")
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        with psycopg.connect(DB_URI, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Find opportunities without a feasibility study
                cur.execute("""
                    SELECT sao.id, sao.signal_id, sao.corrected_text, sig.full_content
                    FROM signal_analysis_opportunity sao
                    JOIN signals sig ON sao.signal_id = sig.id
                    LEFT JOIN feasibility_studies fs ON sao.id = fs.opportunity_id
                    WHERE fs.id IS NULL
                """)
                missing = cur.fetchall()
                
                print(f"📊 Found {len(missing)} opportunities missing a feasibility study.")
                
                count = 0
                for row in missing:
                    # Use corrected_text if available, else fallback to full_content
                    text = row['corrected_text'] or row['full_content']
                    
                    payload = {
                        "opportunity_id": row['id'],
                        "signal_id": row['signal_id'],
                        "corrected_text": text
                    }
                    
                    r.lpush("signal_queue", json.dumps(payload))
                    count += 1
                
                print(f"🚀 Successfully pushed {count} opportunities to the processing queue.")
                print("💡 Make sure 'python main_watcher.py' is running in the multiagent2 folder!")

    except Exception as e:
        print(f"❌ Backfill failed: {e}")

if __name__ == "__main__":
    backfill()
