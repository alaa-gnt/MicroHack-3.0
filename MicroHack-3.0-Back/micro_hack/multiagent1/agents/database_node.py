import psycopg
import uuid
import json
from state import GraphState

# Updated to use the microhack database from .env
DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def save_to_db_node(state: GraphState) -> GraphState:
    """Saves analysis results to signal_analysis_opportunity and updates signal status."""
    
    # Generate opportunity_id if not present
    if not state.get("opportunity_id"):
        state["opportunity_id"] = str(uuid.uuid4())

    opp_query = """
    INSERT INTO signal_analysis_opportunity (
        id, 
        signal_id, 
        primary_domain, 
        urgency_score, 
        impact_score, 
        estimated_trl, 
        companies_mentioned, 
        technologies_mentioned, 
        locations_mentioned,
        corrected_text
    ) VALUES (
        %(id)s, 
        %(signal_id)s, 
        %(primary_domain)s, 
        %(urgency_score)s, 
        %(impact_score)s, 
        %(estimated_trl)s, 
        %(companies_mentioned)s, 
        %(technologies_mentioned)s, 
        %(locations_mentioned)s,
        %(corrected_text)s
    )
    ON CONFLICT (id) DO UPDATE SET 
        primary_domain = EXCLUDED.primary_domain,
        urgency_score = EXCLUDED.urgency_score,
        impact_score = EXCLUDED.impact_score,
        estimated_trl = EXCLUDED.estimated_trl,
        companies_mentioned = EXCLUDED.companies_mentioned,
        technologies_mentioned = EXCLUDED.technologies_mentioned,
        locations_mentioned = EXCLUDED.locations_mentioned,
        corrected_text = EXCLUDED.corrected_text;
    """
    
    signal_query = """
    UPDATE signals SET is_processed = TRUE WHERE id = %s;
    """
    
    # Prepare data for opportunity
    opp_data = {
        "id": state["opportunity_id"],
        "signal_id": state["signal_id"],
        "primary_domain": state.get("domain", "Unknown"),
        "urgency_score": int(state.get("urgency", 0) * 10), 
        "impact_score": int(state.get("impact", 0) * 10),
        "estimated_trl": int(state.get("tri", 0) * 9), # Scaling TRI (0-1) to TRL (1-9)
        "companies_mentioned": ", ".join(state.get("companies", [])),
        "technologies_mentioned": ", ".join(state.get("technologies", [])),
        "locations_mentioned": state.get("location", ""),
        "corrected_text": state.get("corrected_text", "")
    }

    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            with conn.cursor() as cur:
                # 1. Save Opportunity
                cur.execute(opp_query, opp_data)
                
                # 2. Mark Signal as processed
                cur.execute(signal_query, (state["signal_id"],))
                
                print(f"💾 Opportunity created/updated: {state['opportunity_id']} for Signal: {state['signal_id']}")
    except Exception as e:
        print(f"❌ DB Node Save Error: {e}")
    
    return state

def redis_push_node(state: GraphState) -> GraphState:
    """Pushes the opportunity_id to Redis for Tier-2 processing."""
    try:
        import redis
        
        # Connect to Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        # Prepare payload
        payload = {
            "opportunity_id": state['opportunity_id'],
            "signal_id": state['signal_id'],
            "corrected_text": state.get('corrected_text', '')
        }
        
        # Push to the queue
        r.lpush("signal_queue", json.dumps(payload))
        print(f"🚀 Pushed to Redis Queue: Opportunity {state['opportunity_id']}")
        
    except Exception as e:
        print(f"⚠️ Redis Push Error: {e}")
        
    return state
