"""Test for Agent 5: TRI Scoring"""
import os
from agents.agent_5_Tri import TriAgent
from state import GraphState


def test_tri_agent():
    """Test the TRI scoring agent"""
    
    test_state: GraphState = {
        "signal_id": 1,
        "signal_text": "5G network deployment accelerating globally with major telecom providers launching commercial services in urban areas.",
        "keyword": ["5G", "network", "telecom"],
        "domain": "5G/Networking",
        "title": "5G Rollout Gains Momentum",
        "url": "https://example.com",
        "source": "Telecom News",
        "date": "2024-02-06",
        "impact_confidence": 0.85,
        "urgency_confidence": 0.75,
        "impact": 0.75,
        "urgency": 0.70,
        "tri": 0.0,
        "tri_confidence": 0.0,
        "companies": [],
        "technologies": [],
        "location": "",
        "corrected_text": "5G network deployment accelerating globally with major telecom providers launching commercial services in urban areas.",
        "domain_confidence": 0.90,
        "extraction_confidence": None,
        "processing_errors": []
    }
    
    print("Testing TRI Agent...")
    print(f"Text: {test_state['signal_text']}")
    print(f"Domain: {test_state['domain']}")
    print(f"Impact: {test_state['impact']} (conf: {test_state['impact_confidence']})")
    print(f"Urgency: {test_state['urgency']} (conf: {test_state['urgency_confidence']})")
    
    agent = TriAgent()
    result = agent.process(test_state)
    
    print(f"\nTRI Score: {result.get('tri')}/10")
    print(f"Confidence: {result.get('tri_confidence')}")
    print("\n✅ Test completed!")
    
    assert "tri" in result
    assert "tri_confidence" in result
    assert 0 <= result["tri"] <= 10
    assert 0 <= result["tri_confidence"] <= 1


if __name__ == "__main__":
    test_tri_agent()