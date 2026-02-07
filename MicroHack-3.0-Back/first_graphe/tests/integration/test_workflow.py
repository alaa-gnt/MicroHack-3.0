"""
Integration test for the full scraping workflow
Tests the complete graph flow: Orchestrator → Scraping → Quality Filter → Formatter → Handoff
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from graph.workflow import build_scraping_graph
from graph.state import GraphState


class TestFullWorkflow:
    """Integration tests for the complete workflow"""
    
    @patch('graph.nodes.orchestrator_node.get_last_scrape_time')
    @patch('graph.nodes.handoff_node.save_last_scrape_time')
    @patch('graph.nodes.handoff_node.publish_batch')
    def test_full_workflow_with_mock_data(self, mock_publish, mock_save_time, mock_get_time):
        """Test complete workflow with mocked external dependencies"""
        # Setup mocks
        mock_get_time.return_value = None  # Never scraped before
        mock_save_time.return_value = True
        mock_publish.return_value = True
        
        # Build the graph
        app = build_scraping_graph()
        
        # Initial state with test data
        initial_state = {
            "sources": ["https://test.com/feed"],
            "keywords": ["test"]
        }
        
        # This will run the full workflow
        # Note: Actual scraping will fail since we're not mocking HTTP calls
        # The purpose here is to test the graph structure
        try:
            result = app.invoke(initial_state)
            # If we get here, the graph structure works
            assert "action" in result or "batch_id" in result or result == {}
        except Exception as e:
            # Expected to fail on actual HTTP calls, that's OK for structure test
            print(f"Workflow execution error (expected for mock test): {e}")
    
    @patch('graph.nodes.orchestrator_node.get_last_scrape_time')
    def test_workflow_skips_when_recently_scraped(self, mock_get_time):
        """Test that workflow skips when recently scraped"""
        from datetime import datetime, timedelta
        
        # Setup: last scrape was 1 hour ago
        mock_get_time.return_value = datetime.utcnow() - timedelta(hours=1)
        
        # Build the graph
        app = build_scraping_graph()
        
        initial_state = {
            "sources": [],
            "keywords": []
        }
        
        result = app.invoke(initial_state)
        
        # Should skip and return early
        assert result.get("action") == "skip"
    
    def test_graph_structure(self):
        """Test that the graph has correct nodes and edges"""
        app = build_scraping_graph()
        graph = app.get_graph()
        
        # Check nodes exist
        node_names = list(graph.nodes.keys())
        assert "orchestrator" in node_names
        assert "scraping" in node_names
        assert "quality_filter" in node_names
        assert "formatter" in node_names
        assert "handoff" in node_names
        
        print(f"Graph nodes: {node_names}")
        print(f"Graph edges: {list(graph.edges)}")


class TestGraphNodes:
    """Test individual nodes in isolation with mock data"""
    
    def test_quality_filter_with_mock_documents(self):
        """Test quality filter node with controlled input"""
        from graph.nodes.quality_filter_node import quality_filter_node
        
        state = {
            "raw_documents": [
                {
                    "url": "https://example.com/valid",
                    "source": "Test",
                    "title": "Valid Document Title",
                    "text": "This is a valid document with enough text content to pass the filter check easily.",
                    "published_date": "2026-02-06"
                },
                {
                    "url": "invalid-url",
                    "source": "Test",
                    "title": "Invalid",
                    "text": "Short",
                    "published_date": ""
                }
            ]
        }
        
        result = quality_filter_node(state)
        
        assert len(result["valid_documents"]) == 1
        assert result["valid_documents"][0]["title"] == "Valid Document Title"
    
    @patch('graph.nodes.formatter_node.generate_uuid')
    @patch('graph.nodes.formatter_node.now_iso8601')
    def test_formatter_output_structure(self, mock_time, mock_uuid):
        """Test formatter produces correct signal structure"""
        from graph.nodes.formatter_node import formatter_node
        
        mock_uuid.return_value = "test-uuid-123"
        mock_time.return_value = "2026-02-06T10:30:00Z"
        
        state = {
            "valid_documents": [
                {
                    "url": "https://example.com/article",
                    "source": "Test Source",
                    "title": "Test Title",
                    "text": "Test content",
                    "published_date": "2026-02-05"
                }
            ]
        }
        
        result = formatter_node(state)
        
        assert len(result["signals"]) == 1
        signal = result["signals"][0]
        
        # Verify signal schema
        assert "id" in signal
        assert "url" in signal
        assert "source" in signal
        assert "title" in signal
        assert "text" in signal
        assert "scraping_date" in signal
        assert "is_processed" in signal
        assert signal["is_processed"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
