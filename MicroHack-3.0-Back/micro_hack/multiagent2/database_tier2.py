import psycopg
import uuid
from state import Tier2State

# Updated to use the microhack database from .env
DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

def update_tier2_results(state: Tier2State):
    """Updates the record with the full Tier-2 analysis in the FeasibilityStudy table."""
    
    # query uses opportunity_id as the primary key for conflict logic
    # Note: if there's no unique constraint on opportunity_id, this ON CONFLICT will fail.
    # In that case, we'd need to check existence manually or use the id.
    query = """
    INSERT INTO feasibility_studies (
        id, 
        opportunity_id, 
        technical_assessment, 
        required_technology_stack, 
        market_analysis, 
        overall_feasibility, 
        final_recommendation
    ) VALUES (
        %(id)s, 
        %(opportunity_id)s, 
        %(technical_assessment)s, 
        %(required_technology_stack)s, 
        %(market_analysis)s, 
        %(overall_feasibility)s, 
        %(final_recommendation)s
    )
    ON CONFLICT (id) DO UPDATE SET 
        technical_assessment = EXCLUDED.technical_assessment,
        required_technology_stack = EXCLUDED.required_technology_stack,
        market_analysis = EXCLUDED.market_analysis,
        overall_feasibility = EXCLUDED.overall_feasibility,
        final_recommendation = EXCLUDED.final_recommendation;
    """
    
    # Prepare data
    score = state.get("feasibility_score", 0)
    status = "GO" if score > 0.7 else "MAYBE" if score > 0.4 else "NO GO"
    
    rec = state.get("final_recommendation", "")
    
    data = {
        "id": str(uuid.uuid4()), # We generate a new one, but for real persistence we might want to check if one exists
        "opportunity_id": state["opportunity_id"],
        "technical_assessment": state.get("technical_assessment", ""),
        "required_technology_stack": ", ".join(state.get("tech_stack", [])),
        "market_analysis": state.get("market_analysis", ""),
        "overall_feasibility": status,
        "final_recommendation": rec[:20] # Truncated to fit String(20)
    }
    
    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            with conn.cursor() as cur:
                # First try to find existing study for this opportunity
                cur.execute("SELECT id FROM feasibility_studies WHERE opportunity_id = %s", (state["opportunity_id"],))
                existing = cur.fetchone()
                if existing:
                    data["id"] = existing[0]
                
                cur.execute(query, data)
                print(f"💾 Feasibility Study saved for Opportunity: {state['opportunity_id']}")
    except Exception as e:
        print(f"❌ Error updating feasibility study: {e}")
