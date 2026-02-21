import sys
import os
import logging

# Setup path
base_dir = os.getcwd()
agent_dir = os.path.join(base_dir, "first_graphe")
sys.path.insert(0, base_dir)
sys.path.insert(0, agent_dir)

from first_graphe.graph.nodes.scraping_node import scraping_node
from first_graphe.graph.state import GraphState

logging.basicConfig(level=logging.INFO)

def test_scraping_node():
    print("Testing Scraping Node...")
    state = {
        "keywords": ["maritime"],
        "sources": ["https://www.porttechnology.org/feed/"]
    }
    
    result = scraping_node(state)
    docs = result.get("raw_documents", [])
    print(f"\nFound {len(docs)} raw documents.")
    
    if docs:
        for i, doc in enumerate(docs[:3]):
            print(f"\nDocument {i+1}:")
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print(f"Pub Date: {doc.get('published_date')}")
            print(f"Text Snippet: {doc.get('text', '')[:100]}...")

if __name__ == "__main__":
    test_scraping_node()
