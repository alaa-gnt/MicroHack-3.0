from graph.state import GraphState
from datetime import datetime
import uuid
import redis
import json

# Backend imports
from app.database.postgres import SessionLocal
from app.services.signal_service import SignalService
from app.schemas.signal import SignalCreate

def handoff_node(state: GraphState) -> GraphState:
    """
    Handoff node that saves processed signals to the PostgreSQL database.
    """
    batch_id = f"batch_{uuid.uuid4().hex}"

    # Initialize Redis for handoff
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
    except Exception as re:
        print(f"⚠️ Redis Connection Error in Handoff: {re}")
        r = None

    # Save to PostgreSQL
    db = SessionLocal()
    try:
        signals = state.get("signals", [])
        for signal_data in signals:
            try:
                signal_in = SignalCreate(
                    title=signal_data.get("title", "No Title"),
                    full_content=signal_data.get("text", ""),
                    source_url=signal_data.get("url", ""),
                    source_name=signal_data.get("source", "Unknown")
                )
                db_signal = SignalService.create_signal(db, signal_in)
                
                # Push to Redis for Agent 1 (Full Payload for matching Agent 1 -> Agent 2 pattern)
                if r:
                    try:
                        payload = {
                            "signal_id": db_signal.id,
                            "title": db_signal.title,
                            "full_content": db_signal.full_content
                        }
                        r.lpush("raw_signals_queue", json.dumps(payload))
                        print(f"🚀 Pushed Full Signal Data to Redis: {db_signal.id}")
                    except Exception as rp:
                        print(f"⚠️ Redis Push Error: {rp}")

            except Exception as e:
                print(f"Error saving signal to DB: {e}")
                continue
    finally:
        db.close()

    return {
        "batch_id": batch_id
    }
