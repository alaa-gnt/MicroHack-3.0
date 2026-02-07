import time
from dotenv import load_dotenv
import redis
import json
from workflow import app  # Imports the compiled LangGraph
from database_tier2 import update_tier2_results

load_dotenv()

def run_automation_loop():
    print("🤖 Multi-Agent 2 Watcher is ONLINE.")
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        print("✅ Connected to Redis.")
    except Exception as e:
        print(f"❌ Redis Connection Error: {e}")
        return

    while True:
        try:
            # 1. Listen for new messages (Blocking Pop)
            # This blocks until a message is available in 'signal_queue'
            queue_item = r.blpop("signal_queue", timeout=10)
            
            if queue_item:
                # payload is (key, value)
                msg_body = queue_item[1]
                data = json.loads(msg_body)
                
                opp_id = data.get('opportunity_id')
                sig_id = data.get('signal_id')
                text = data.get('corrected_text')
                
                if not opp_id:
                    print(f"⚠️ Warning: Received message without opportunity_id: {data}")
                    continue

                print(f"\n🚀 [EVENT] Redis Event for Opportunity: {opp_id}")
                print(f"📝 Input: {text[:100]}...")

                # 2. Prepare INITIAL state for Tier-2
                initial_state = {
                    "signal_id": sig_id,
                    "opportunity_id": opp_id,
                    "corrected_text": text,
                    "confidences": {},
                    "retry_counts": {},
                    "agent_thoughts": [f"Starting Tier-2 deep dive for Opportunity {opp_id}"]
                }

                # 3. Invoke
                config = {"configurable": {"thread_id": f"tier2_{opp_id}"}}
                print(f"🧠 Agents are thinking...")
                
                try:
                    final_state = app.invoke(initial_state, config=config)
                    
                    # 4. Save results to FeasibilityStudy table
                    update_tier2_results(final_state)
                    print(f"✅ Deep Dive Complete for {opp_id}. Feasibility Study saved.")
                except Exception as invoke_err:
                    print(f"❌ Error during agent execution: {invoke_err}")

            else:
                # Timeout happened
                pass


        except KeyboardInterrupt:
            print("\n🛑 Watcher stopped by user.")
            break
        except Exception as e:
            print(f"❌ Error in Watcher Loop: {e}")
            time.sleep(20)

if __name__ == "__main__":
    run_automation_loop()
