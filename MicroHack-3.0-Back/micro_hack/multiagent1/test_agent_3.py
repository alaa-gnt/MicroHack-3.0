"""Test for Agent 3: Impact Scoring"""
import os
from agents.agent_3_ImpactScoring import ImpactScoringAgent
from state import GraphState


def test_impact_scoring_agent():
    """Test the impact scoring agent"""
    
    test_state: GraphState = {
        "signal_id": 1,
        "signal_text": "Revolutionary quantum computing breakthrough achieves room temperature superconductivity, enabling widespread commercial applications.",
        "keyword": ["quantum", "breakthrough"],
        "domain": "Quantum Computing",
        "title": "Quantum Computing Revolution",
        "url": "https://example.com",
        "source": "Nature",
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
        "corrected_text": "Revolutionary quantum computing breakthrough achieves room temperature superconductivity, enabling widespread commercial applications.",
        "domain_confidence": 0.95,
        "extraction_confidence": None,
        "processing_errors": []
    }
    
    print("Testing Impact Scoring Agent...")
    print(f"Text: {test_state['signal_text']}")
    print(f"Domain: {test_state['domain']}")
    
    agent = ImpactScoringAgent()
    result = agent.process(test_state)
    
    print(f"\nImpact Score: {result.get('impact')}")
    print(f"Confidence: {result.get('impact_confidence')}")
    print("\n✅ Test completed!")
    
    assert "impact" in result
    assert "impact_confidence" in result
    assert 0 <= result["impact"] <= 1
    assert 0 <= result["impact_confidence"] <= 1


if __name__ == "__main__":
    test_impact_scoring_agent()