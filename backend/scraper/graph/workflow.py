from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes.orchestrator_node import orchestrator_node
from graph.nodes.scraping_node import scraping_node
from graph.nodes.quality_filter_node import quality_filter_node
from graph.nodes.formatter_node import formatter_node
from graph.nodes.handoff_node import handoff_node
from graph.router import route_on_action


def build_scraping_graph():
    """
    Creates and returns compiled LangGraph workflow
    
    Flow:
    START → Orchestrator → [Scraping | END]
    Scraping → Quality Filter → Formatter → Handoff → END
    """

    graph = StateGraph(GraphState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("scraping", scraping_node)
    graph.add_node("quality_filter", quality_filter_node)
    graph.add_node("formatter", formatter_node)
    graph.add_node("handoff", handoff_node)

    graph.set_entry_point("orchestrator")

    graph.add_conditional_edges(
        "orchestrator",
        route_on_action,
        {
            "scrape": "scraping",
            "end": END
        }
    )

    graph.add_edge("scraping", "quality_filter")
    graph.add_edge("quality_filter", "formatter")
    graph.add_edge("formatter", "handoff")
    graph.add_edge("handoff", END)

    return graph.compile()
