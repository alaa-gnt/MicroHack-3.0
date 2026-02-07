from graph.state import GraphState
from utils.uuid_generator import generate_uuid
from utils.timestamp import now_iso8601


def formatter_node(state: GraphState) -> GraphState:
    signals = []

    for doc in state["valid_documents"]:
        signals.append({
            "id": generate_uuid(),
            "url": doc["url"],
            "source": doc["source"],
            "title": doc["title"],
            "text": doc["text"],
            "scraping_date": now_iso8601(),
            "is_processed": False
        })

    return {
        "signals": signals
    }
