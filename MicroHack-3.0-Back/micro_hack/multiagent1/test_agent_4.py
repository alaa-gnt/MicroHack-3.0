"""Test for Agent 4: Urgency Scoring"""
import os
from agents.agent_4_UrgencyScoring import UrgencyScoringAgent
from state import GraphState


def test_urgency_scoring_agent():
    """Test the urgency scoring agent"""
    
    test_state: GraphState = {
        "signal_id": 1,
        "signal_text": "Major cybersecurity vulnerability discovered in widely-used enterprise software, affecting millions of users worldwide. Patch must be deployed immediately.",
        "keyword": ["cybersecurity", "vulnerability"],
        "domain": "Cybersecurity",
        "title": "Critical Security Flaw Discovered",
        "url": "https://example.com",
        "source": "Security Weekly",
        "date": "2024-02-06",
        "impact_confidence": 0.9,
        "urgency_confidence": 0.0,
        "impact": 0.85,
        "urgency": 0.0,
        "tri": 0.0,
        "tri_confidence": 0.0,
        "companies": [],
        "technologies": [],
        "location": "",
        "corrected_text": "Major cybersecurity vulnerability discovered in widely-used enterprise software, affecting millions of users worldwide. Patch must be deployed immediately.",
        "domain_confidence": 0.95,
        "extraction_confidence": None,
        "processing_errors": []
    }
    
    print("Testing Urgency Scoring Agent...")
    print(f"Text: {test_state['signal_text']}")
    print(f"Domain: {test_state['domain']}")
    
    agent = UrgencyScoringAgent()
    result = agent.process(test_state)
    
    print(f"\nUrgency Score: {result.get('urgency')}")
    print(f"Confidence: {result.get('urgency_confidence')}")
    print("\n✅ Test completed!")
    
    assert "urgency" in result
    assert "urgency_confidence" in result
    assert 0 <= result["urgency"] <= 1
    assert 0 <= result["urgency_confidence"] <= 1


if __name__ == "__main__":
    test_urgency_scoring_agent()