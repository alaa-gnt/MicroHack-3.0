"""
Test script to run the full workflow and display output at each step
This script tests the graph nodes individually and shows signals at the end
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import json
from datetime import datetime


from graph.workflow import build_scraping_graph
from graph.state import GraphState
from config.loader import get_scraping_config
import uuid

def test_live_workflow():
    """
    Test the complete workflow with LIVE data
    """
    print("=" * 60)
    print("LIVE SCRAPING WORKFLOW TEST")
    print("=" * 60)
    print(f"Start time: {datetime.now().isoformat()}")
    
    # Initialization
    config = get_scraping_config()
    initial_state: GraphState = {
        "batch_id": f"batch_{uuid.uuid4().hex[:8]}",
        "keywords": config.get('keywords', [])[:3], # Small subset for testing
        "sources": config.get('rss_feeds', [])
    }
    
    print(f"Keywords: {initial_state['keywords']}")
    print(f"RSS Feeds: {len(initial_state['sources'])}")
    print("-" * 60)

    # Compile and run graph
    app = build_scraping_graph()
    
    print("Executing Graph (with Orchestrator skip bypass)...")
    # Bypass orchestrator skip by mocking the last scrape time check
    from unittest.mock import patch
    with patch('graph.nodes.orchestrator_node.get_last_scrape_time') as mock_scrape_time:
        mock_scrape_time.return_value = None
        final_state = app.invoke(initial_state)
    
    print("-" * 60)
    print("WORKFLOW COMPLETE")
    print("-" * 60)
    
    # Result Summary
    raw_count = len(final_state.get("raw_documents", []))
    valid_count = len(final_state.get("valid_documents", []))
    signal_count = len(final_state.get("signals", []))
    
    print(f"Raw Documents found: {raw_count}")
    print(f"Documents after Quality Filter: {valid_count}")
    print(f"Final Formatted Signals: {signal_count}")
    print("-" * 60)
    
    # Save summary to file
    summary = {
        "timestamp": datetime.now().isoformat(),
        "keywords": initial_state['keywords'],
        "raw_count": raw_count,
        "valid_count": valid_count,
        "signal_count": signal_count,
        "sample_signal": final_state["signals"][0] if signal_count > 0 else None
    }
    
    summary_path = os.path.join(project_root, "logs", "test_workflow_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to: {summary_path}")

    if signal_count > 0:
        print("\nSAMPLE SIGNAL:")
        print(json.dumps(final_state["signals"][0], indent=2))
    
    print("\n" + "=" * 60)
    print(f"End time: {datetime.now().isoformat()}")
    
    return final_state

if __name__ == "__main__":
    try:
        test_live_workflow()
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
