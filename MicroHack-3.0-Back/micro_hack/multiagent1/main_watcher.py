import time
from dotenv import load_dotenv
import psycopg
import redis
import json
from psycopg.rows import dict_row
from workflow import app

load_dotenv()

# Database Connection URI
DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def run_watcher():
    print("🤖 Multi-Agent 1 Watcher is ONLINE (Pure Redis Event Mode).")
    
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        print("✅ Connected to Redis.")
    except Exception as re:
        print(f"❌ Redis Connection Error: {re}")
        return

    while True:
        try:
            # Listening for new signals from the scraper (Exactly same as Agent 2)
            queue_item = r.blpop("raw_signals_queue", timeout=10)
            
            if not queue_item:
                continue

            # payload is (key, value)
            msg_body = queue_item[1]
            data = json.loads(msg_body)
            
            sig_id = data.get('signal_id')
            content = data.get('full_content') or data.get('title')

            if not sig_id or not content:
                print(f"⚠️ Warning: Received incomplete message from Redis: {data}")
                continue

            print(f"\n🚀 [EVENT] Redis Event for Signal: {sig_id}")
            print(f"📝 Input: {content[:100]}...")
            
            # Initializing the state
            initial_state = {
                "signal_id": sig_id,
                "signal_text": content,
                "corrected_text": "", 
                "domain": "",
                "impact": 0.0,
                "urgency": 0.0,
                "tri": 0.0,
                "technologies": [],
                "companies": [],
                "location": "",
                "retry_count": 0,
                "processing_errors": [],
                "agent_thoughts": []
            }
            
            config = {"configurable": {"thread_id": f"tier1_{sig_id}"}}
            
            try:
                print(f"🧠 Agents are analyzing signal {sig_id}...")
                app.invoke(initial_state, config=config)
                print(f"✅ Signal {sig_id} processed successfully.")
            except Exception as invoke_err:
                print(f"❌ Error during agent execution: {invoke_err}")

        except KeyboardInterrupt:
            print("\n🛑 Watcher stopped by user.")
            break
        except Exception as e:
            print(f"❌ Error in Watcher Loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_watcher()
