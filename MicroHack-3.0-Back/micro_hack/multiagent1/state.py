from typing import Annotated, List, TypedDict
import operator

class GraphState(TypedDict):
    # Core Data
    signal_id: str
    opportunity_id: str  # Added for integration
    signal_text: str
    corrected_text: str
    keyword: List[str]
    title: str
    url: str
    source: str
    date: str
    
    # Classification & Scoring
    domain: str
    domain_confidence: float
    impact: float
    impact_confidence: float
    urgency: float
    urgency_confidence: float
    tri: float
    tri_confidence: float
    
    # Extraction Results
    companies: List[str]
    technologies: List[str]
    location: str
    extraction_confidence: float
    
    # ReAct / Metadata
    retry_count: Annotated[int, operator.add] 
    processing_errors: Annotated[List[str], operator.add]
    agent_thoughts: Annotated[List[str], operator.add]