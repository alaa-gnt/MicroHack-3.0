"""
Graph Visualization Script

Generates and saves a visual representation of the scraping workflow graph.
Outputs: graph_visualization.png in the scripts folder
"""

import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from graph.workflow import build_scraping_graph


def visualize_graph():
    """Build and visualize the scraping graph, saving it as a PNG image."""
    
    # Build the graph
    app = build_scraping_graph()
    
    # Get the output path (same folder as this script)
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "graph_visualization.png")
    
    try:
        # Try using draw_mermaid_png (preferred for LangGraph)
        graph_image = app.get_graph().draw_mermaid_png()
        with open(output_path, "wb") as f:
            f.write(graph_image)
        print(f" Graph saved successfully to: {output_path}")
        
    except Exception as e:
        print(f"Mermaid PNG failed: {e}")
        try:
            # Fallback to draw_png (requires graphviz)
            graph_image = app.get_graph().draw_png()
            with open(output_path, "wb") as f:
                f.write(graph_image)
            print(f" Graph saved successfully to: {output_path}")
            
        except Exception as e2:
            print(f" Could not generate graph image: {e2}")
            print("\nTo fix this, try one of the following:")
            print("1. Install graphviz: pip install graphviz pygraphviz")
            print("2. Or install mermaid support for langgraph")
            
            # Fallback: print ASCII representation
            print("\n Graph Structure (ASCII):")
            print("=" * 50)
            graph = app.get_graph()
            print(f"Nodes: {list(graph.nodes.keys())}")
            print(f"\nEdges:")
            for edge in graph.edges:
                print(f"  {edge}")
            return False
    
    return True


if __name__ == "__main__":
    visualize_graph()
