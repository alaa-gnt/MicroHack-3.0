
import psycopg
from datetime import datetime, timedelta, timezone
from psycopg.rows import dict_row

DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def verify_recent_signals():
    print("🔍 Verifying if scraper ran on startup (Direct SQL)...")
    try:
        with psycopg.connect(DB_URI, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                # Check for signals created in the last 15 minutes (UTC)
                fifteen_mins_ago = datetime.now(timezone.utc) - timedelta(minutes=15)
                
                query = "SELECT id, title, source_name, date FROM signals WHERE date >= %s ORDER BY date DESC"
                cur.execute(query, (fifteen_mins_ago,))
                recent_signals = cur.fetchall()
                
                if recent_signals:
                    print(f"✅ SUCCESS: Found {len(recent_signals)} signals created in the last 15 minutes.")
                    for s in recent_signals[:5]:
                        print(f"   - [{s['date']}] {s['source_name']} | {s['title'][:50]}...")
                else:
                    print("⚠️ WARNING: No signals found from the last 15 minutes.")
                    print("   This might mean the scraper hasn't finished its first run yet.")
                    
                    cur.execute("SELECT count(*) FROM signals")
                    total = cur.fetchone()['count']
                    print(f"   Total signals in DB: {total}")
                    
                    cur.execute("SELECT date FROM signals ORDER BY date DESC LIMIT 1")
                    last = cur.fetchone()
                    if last:
                        print(f"   Last signal was created at: {last['date']}")

    except Exception as e:
        print(f"❌ Error verifying signals: {e}")

if __name__ == "__main__":
    verify_recent_signals()
