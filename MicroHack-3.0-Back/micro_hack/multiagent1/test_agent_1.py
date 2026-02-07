"""Test for Agent 1: Text Improvement"""
import os
from agents.agent_1_TextImprove import TextImproveAgent
from state import GraphState


def test_text_improve_agent():
    """Test the text improvement agent"""
    
    # Test state with poor grammar
    test_state: GraphState = {
        "signal_id": 1,
        "signal_text": "AI technolgy is becomming more powerfull every day and its changing the way we work and live.",
        "keyword": ["AI", "technology"],
        "domain": "",
        "title": "AI Advancement",
        "url": "https://example.com",
        "source": "Test Source",
        "date": "2024-02-06",
        "impact_confidence": 0.0,
        "urgency_confidence": 0.0,
        "impact": 0.0,
        "urgency": 0.0,
        "tri": 0.0,
        "tri_confidence": 0.0,
        "companies": [],
        "technologies": [],
        "location": "",
        "corrected_text": None,
        "domain_confidence": None,
        "extraction_confidence": None,
        "processing_errors": []
    }
    
    print("Testing Text Improvement Agent...")
    print(f"Original text: {test_state['signal_text']}")
    
    agent = TextImproveAgent()
    result = agent.process(test_state)
    
    print(f"\nCorrected text: {result.get('corrected_text')}")
    print("\n✅ Test completed!")
    
    assert "corrected_text" in result
    assert len(result["corrected_text"]) > 0


if __name__ == "__main__":
    test_text_improve_agent()