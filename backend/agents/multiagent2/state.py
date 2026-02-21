from typing import Annotated, List, TypedDict, Dict
import operator

# Helper function to merge dictionaries
def merge_dicts(existing: Dict, new: Dict) -> Dict:
    combined = existing.copy()
    combined.update(new)
    return combined

class Tier2State(TypedDict):
    signal_id: str
    opportunity_id: str  # Added for integration
    corrected_text: str
    
    # Outputs
    technical_assessment: str
    tech_stack: List[str]
    market_analysis: str
    feasibility_score: float
    final_recommendation: str
    
    # Updated Annotated fields using our helper and standard operator
    confidences: Annotated[Dict[str, float], merge_dicts] 
    retry_counts: Annotated[Dict[str, int], merge_dicts]
    agent_thoughts: Annotated[List[str], operator.add]