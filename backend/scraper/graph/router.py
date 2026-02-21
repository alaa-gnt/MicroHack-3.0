from graph.state import GraphState


def route_on_action(state: GraphState) -> str:
    """
    Routes based on orchestrator decision
    
    If action == "proceed" → go to scraping
    If action == "skip" → end graph
    """


    if state["action"] == "proceed":
        return "scrape"
    return "end"
