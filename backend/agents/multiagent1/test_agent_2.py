"""Test for Agent 2: Domain Classification"""
import os
from agents.agent_2_ClassifyDomain import ClassifyDomainAgent
from state import GraphState


def test_classify_domain_agent():
    """Test the domain classification agent"""
    
    test_state: GraphState = {
        "signal_id": 1,
        "signal_text": "Blockchain technology is being used to create decentralized applications for financial transactions.",
        "keyword": ["blockchain", "DeFi", "crypto"],
        "domain": "",
        "title": "Blockchain in Finance",
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
        "corrected_text": "Blockchain technology is being used to create decentralized applications for financial transactions.",
        "domain_confidence": None,
        "extraction_confidence": None,
        "processing_errors": []
    }
    
    print("Testing Domain Classification Agent...")
    print(f"Text: {test_state['signal_text']}")
    print(f"Keywords: {test_state['keyword']}")
    
    agent = ClassifyDomainAgent()
    result = agent.process(test_state)
    
    print(f"\nClassified Domain: {result.get('domain')}")
    print(f"Confidence: {result.get('domain_confidence')}")
    print("\n✅ Test completed!")
    
    assert "domain" in result
    assert "domain_confidence" in result
    assert 0 <= result["domain_confidence"] <= 1


if __name__ == "__main__":
    test_classify_domain_agent()