"""
Tests for graph/router.py
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from graph.router import route_on_action
from graph.state import GraphState


class TestRouteOnAction:
    """Tests for route_on_action function"""
    
    def test_routes_to_scrape_on_proceed(self):
        """Should return 'scrape' when action is 'proceed'"""
        state = GraphState(action="proceed")
        
        result = route_on_action(state)
        
        assert result == "scrape"
    
    def test_routes_to_end_on_skip(self):
        """Should return 'end' when action is 'skip'"""
        state = GraphState(action="skip")
        
        result = route_on_action(state)
        
        assert result == "end"
    
    def test_routes_to_end_on_unknown(self):
        """Should return 'end' for any unknown action"""
        state = GraphState(action="unknown_action")
        
        result = route_on_action(state)
        
        assert result == "end"
    
    def test_routes_to_end_on_empty(self):
        """Should return 'end' when action is empty"""
        state = GraphState(action="")
        
        result = route_on_action(state)
        
        assert result == "end"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
