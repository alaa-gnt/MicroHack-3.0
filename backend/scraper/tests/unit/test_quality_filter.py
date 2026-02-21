"""
Tests for graph/nodes/quality_filter_node.py
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from graph.nodes.quality_filter_node import quality_filter_node
from graph.state import GraphState


class TestQualityFilterNode:
    """Tests for quality_filter_node function"""
    
    def test_valid_documents_pass_filter(self):
        """Valid documents should pass through the filter"""
        state = GraphState(
            raw_documents=[
                {
                    "url": "https://example.com/article1",
                    "source": "Test Source",
                    "title": "Valid Article Title",
                    "text": "This is a valid article text that is long enough to pass the quality filter validation.",
                    "published_date": "2026-02-06"
                }
            ]
        )
        
        result = quality_filter_node(state)
        
        assert len(result["valid_documents"]) == 1
        assert result["valid_documents"][0]["title"] == "Valid Article Title"
    
    def test_filters_out_missing_title(self):
        """Documents without title should be filtered out"""
        state = GraphState(
            raw_documents=[
                {
                    "url": "https://example.com/article1",
                    "source": "Test Source",
                    "title": "",  # Empty title
                    "text": "This is a valid article text that is long enough.",
                    "published_date": "2026-02-06"
                }
            ]
        )
        
        result = quality_filter_node(state)
        
        assert len(result["valid_documents"]) == 0
    
    def test_filters_out_short_text(self):
        """Documents with text < 50 chars should be filtered out"""
        state = GraphState(
            raw_documents=[
                {
                    "url": "https://example.com/article1",
                    "source": "Test Source",
                    "title": "Valid Title",
                    "text": "Too short",  # Less than 50 characters
                    "published_date": "2026-02-06"
                }
            ]
        )
        
        result = quality_filter_node(state)
        
        assert len(result["valid_documents"]) == 0
    
    def test_filters_out_invalid_url(self):
        """Documents with invalid URL should be filtered out"""
        state = GraphState(
            raw_documents=[
                {
                    "url": "not-a-valid-url",
                    "source": "Test Source",
                    "title": "Valid Title",
                    "text": "This is a valid article text that is long enough to pass the quality filter validation.",
                    "published_date": "2026-02-06"
                }
            ]
        )
        
        result = quality_filter_node(state)
        
        assert len(result["valid_documents"]) == 0
    
    def test_filters_out_missing_date(self):
        """Documents without published_date should be filtered out"""
        state = GraphState(
            raw_documents=[
                {
                    "url": "https://example.com/article1",
                    "source": "Test Source",
                    "title": "Valid Title",
                    "text": "This is a valid article text that is long enough to pass the quality filter validation.",
                    "published_date": ""  # Empty date
                }
            ]
        )
        
        result = quality_filter_node(state)
        
        assert len(result["valid_documents"]) == 0
    
    def test_multiple_documents_mixed(self):
        """Should filter multiple documents correctly"""
        state = GraphState(
            raw_documents=[
                {
                    "url": "https://example.com/valid",
                    "source": "Source 1",
                    "title": "Valid Document",
                    "text": "This is a valid document with enough text to pass the quality filter.",
                    "published_date": "2026-02-06"
                },
                {
                    "url": "https://example.com/invalid",
                    "source": "Source 2",
                    "title": "",  # Invalid - no title
                    "text": "Some text here",
                    "published_date": "2026-02-06"
                },
                {
                    "url": "https://example.com/another-valid",
                    "source": "Source 3",
                    "title": "Another Valid Document",
                    "text": "This is another valid document with sufficient text content to pass all checks.",
                    "published_date": "2026-02-05"
                }
            ]
        )
        
        result = quality_filter_node(state)
        
        assert len(result["valid_documents"]) == 2
        titles = [doc["title"] for doc in result["valid_documents"]]
        assert "Valid Document" in titles
        assert "Another Valid Document" in titles


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
