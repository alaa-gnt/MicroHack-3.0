"""Test for Agent 6: Information Extraction"""
import os
from agents.agent_6_Extracter import ExtractorAgent
from state import GraphState


def test_extractor_agent():
    """Test the information extraction agent"""
    
    test_state: GraphState = {
        "signal_id": 1,
        "signal_text": "Tesla and SpaceX are collaborating on a new satellite internet project using Starlink technology in California. The project will leverage advanced AI algorithms and quantum encryption protocols.",
        "keyword": ["satellite", "internet"],
        "domain": "Space Technology",
        "title": "Tesla-SpaceX Satellite Collaboration",
        "url": "https://example.com/tesla-spacex",
        "source": "Tech News",
        "date": "2024-02-06",
        "impact_confidence": 0.80,
        "urgency_confidence": 0.70,
        "impact": 0.75,
        "urgency": 0.65,
        "tri": 8.5,
        "tri_confidence": 0.85,
        "companies": [],
        "technologies": [],
        "location": "",
        "corrected_text": "Tesla and SpaceX are collaborating on a new satellite internet project using Starlink technology in California. The project will leverage advanced AI algorithms and quantum encryption protocols.",
        "domain_confidence": 0.90,
        "extraction_confidence": None,
        "processing_errors": []
    }
    
    print("Testing Information Extraction Agent...")
    print(f"Text: {test_state['signal_text']}")
    
    agent = ExtractorAgent()
    result = agent.process(test_state)
    
    print(f"\nExtracted Companies: {result.get('companies')}")
    print(f"Extracted Technologies: {result.get('technologies')}")
    print(f"Extracted Location: {result.get('location')}")
    print(f"Confidence: {result.get('extraction_confidence')}")
    print("\n✅ Test completed!")
    
    assert "companies" in result
    assert "technologies" in result
    assert "location" in result
    assert isinstance(result["companies"], list)
    assert isinstance(result["technologies"], list)


if __name__ == "__main__":
    test_extractor_agent()