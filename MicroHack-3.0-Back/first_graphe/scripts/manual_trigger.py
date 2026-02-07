"""
Manually trigger scraping for testing
"""
import sys
import os

# Add the project root and first_graphe to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph.workflow import build_scraping_graph
from graph.state import GraphState
from utils.uuid_generator import generate_uuid
from utils.timestamp import get_iso8601_timestamp

def main():
    print("🚀 Manually triggering scraping workflow (REAL EXECUTION)...")
    
    initial_state = GraphState(
        batch_id=generate_uuid(),  # Using batch_id as per state definition
        # trigger_time was removed from state? Let's check state.py. 
        # State has action, sources, keywords, raw_documents, valid_documents, signals, batch_id
        action="scrape", # Directly force action to scrape
        signals=[]
    )
    
    print("Building workflow...")
    workflow = build_scraping_graph()
    print("Invoking workflow...")
    result = workflow.invoke(initial_state)
    
    print(f" Complete! Collected {result.get('signals_count', 0)} signals")
    print(f"Batch ID: {result.get('batch_id')}")

if __name__ == "__main__":
    main()