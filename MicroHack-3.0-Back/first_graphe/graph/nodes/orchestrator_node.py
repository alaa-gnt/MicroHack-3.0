from graph.state import GraphState
from storage.redis_client import get_last_scrape_time
from config.settings import SCRAPE_INTERVAL_MINUTES
from datetime import datetime, timedelta


def orchestrator_node(state: GraphState) -> GraphState:
    last_scrape = get_last_scrape_time()

    if last_scrape:
        delta = datetime.utcnow() - last_scrape
        if delta < timedelta(minutes=SCRAPE_INTERVAL_MINUTES):
            return {
                "action": "skip"
            }

    return {
        "action": "proceed",
        "sources": state.get("sources", []),
        "keywords": state.get("keywords", [])
    }
