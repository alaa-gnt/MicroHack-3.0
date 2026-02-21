"""
Tests for graph/nodes/orchestrator_node.py
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from graph.nodes.orchestrator_node import orchestrator_node
from graph.state import GraphState


class TestOrchestratorNode:
    """Tests for orchestrator_node function"""
    
    @patch('graph.nodes.orchestrator_node.get_last_scrape_time')
    def test_proceed_when_no_last_scrape(self, mock_get_last_scrape):
        """Should proceed if never scraped before"""
        mock_get_last_scrape.return_value = None
        
        state = GraphState(
            sources=["https://example.com/feed"],
            keywords=["IoT", "smart port"]
        )
        
        result = orchestrator_node(state)
        
        assert result["action"] == "proceed"
        assert result["sources"] == ["https://example.com/feed"]
        assert result["keywords"] == ["IoT", "smart port"]
    
    @patch('graph.nodes.orchestrator_node.get_last_scrape_time')
    @patch('graph.nodes.orchestrator_node.SCRAPE_INTERVAL_MINUTES', 300)
    def test_skip_when_recently_scraped(self, mock_get_last_scrape):
        """Should skip if scraped within interval"""
        # Last scrape was 1 hour ago (within 5 hour interval)
        mock_get_last_scrape.return_value = datetime.utcnow() - timedelta(hours=1)
        
        state = GraphState(
            sources=["https://example.com/feed"],
            keywords=["IoT"]
        )
        
        result = orchestrator_node(state)
        
        assert result["action"] == "skip"
    
    @patch('graph.nodes.orchestrator_node.get_last_scrape_time')
    @patch('graph.nodes.orchestrator_node.SCRAPE_INTERVAL_MINUTES', 300)
    def test_proceed_when_interval_passed(self, mock_get_last_scrape):
        """Should proceed if interval has passed"""
        # Last scrape was 6 hours ago (beyond 5 hour interval)
        mock_get_last_scrape.return_value = datetime.utcnow() - timedelta(hours=6)
        
        state = GraphState(
            sources=["https://example.com/feed"],
            keywords=["IoT"]
        )
        
        result = orchestrator_node(state)
        
        assert result["action"] == "proceed"
    
    @patch('graph.nodes.orchestrator_node.get_last_scrape_time')
    def test_uses_default_empty_lists(self, mock_get_last_scrape):
        """Should use empty lists for sources/keywords if not in state"""
        mock_get_last_scrape.return_value = None
        
        state = GraphState()  # Empty state
        
        result = orchestrator_node(state)
        
        assert result["action"] == "proceed"
        assert result["sources"] == []
        assert result["keywords"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
