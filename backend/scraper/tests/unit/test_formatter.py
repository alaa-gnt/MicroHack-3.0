"""
Tests for graph/nodes/formatter_node.py
"""
import pytest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from graph.nodes.formatter_node import formatter_node
from graph.state import GraphState


class TestFormatterNode:
    """Tests for formatter_node function"""
    
    @patch('graph.nodes.formatter_node.generate_uuid')
    @patch('graph.nodes.formatter_node.now_iso8601')
    def test_formats_documents_to_signals(self, mock_timestamp, mock_uuid):
        """Should convert valid_documents to signals format"""
        mock_uuid.return_value = "test-uuid-12345"
        mock_timestamp.return_value = "2026-02-06T10:30:00Z"
        
        state = GraphState(
            valid_documents=[
                {
                    "url": "https://example.com/article",
                    "source": "Test Source",
                    "title": "Test Article Title",
                    "text": "This is the article content.",
                    "published_date": "2026-02-05"
                }
            ]
        )
        
        result = formatter_node(state)
        
        assert len(result["signals"]) == 1
        signal = result["signals"][0]
        
        assert signal["id"] == "test-uuid-12345"
        assert signal["url"] == "https://example.com/article"
        assert signal["source"] == "Test Source"
        assert signal["title"] == "Test Article Title"
        assert signal["text"] == "This is the article content."
        assert signal["scraping_date"] == "2026-02-06T10:30:00Z"
        assert signal["is_processed"] is False
    
    @patch('graph.nodes.formatter_node.generate_uuid')
    @patch('graph.nodes.formatter_node.now_iso8601')
    def test_multiple_documents(self, mock_timestamp, mock_uuid):
        """Should format multiple documents"""
        mock_uuid.side_effect = ["uuid-1", "uuid-2", "uuid-3"]
        mock_timestamp.return_value = "2026-02-06T10:30:00Z"
        
        state = GraphState(
            valid_documents=[
                {"url": "https://a.com", "source": "A", "title": "Title A", "text": "Text A", "published_date": "2026-02-01"},
                {"url": "https://b.com", "source": "B", "title": "Title B", "text": "Text B", "published_date": "2026-02-02"},
                {"url": "https://c.com", "source": "C", "title": "Title C", "text": "Text C", "published_date": "2026-02-03"},
            ]
        )
        
        result = formatter_node(state)
        
        assert len(result["signals"]) == 3
        assert result["signals"][0]["id"] == "uuid-1"
        assert result["signals"][1]["id"] == "uuid-2"
        assert result["signals"][2]["id"] == "uuid-3"
    
    @patch('graph.nodes.formatter_node.generate_uuid')
    @patch('graph.nodes.formatter_node.now_iso8601')
    def test_empty_documents(self, mock_timestamp, mock_uuid):
        """Should return empty signals list for empty input"""
        state = GraphState(valid_documents=[])
        
        result = formatter_node(state)
        
        assert result["signals"] == []
    
    @patch('graph.nodes.formatter_node.generate_uuid')
    @patch('graph.nodes.formatter_node.now_iso8601')
    def test_is_processed_always_false(self, mock_timestamp, mock_uuid):
        """All signals should have is_processed=False initially"""
        mock_uuid.return_value = "test-uuid"
        mock_timestamp.return_value = "2026-02-06T10:30:00Z"
        
        state = GraphState(
            valid_documents=[
                {"url": "https://example.com", "source": "S", "title": "T", "text": "Text", "published_date": "2026-02-01"},
            ]
        )
        
        result = formatter_node(state)
        
        for signal in result["signals"]:
            assert signal["is_processed"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
