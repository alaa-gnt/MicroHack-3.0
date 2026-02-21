from graph.state import GraphState
from utils.validators import is_valid_url


def quality_filter_node(state: GraphState) -> GraphState:
    valid_docs = []

    for doc in state["raw_documents"]:
        if not doc.get("title"):
            continue
        if not doc.get("text") or len(doc["text"]) < 50:
            continue
        if not is_valid_url(doc.get("url")):
            continue
        if not doc.get("published_date"):
            continue

        valid_docs.append(doc)

    return {
        "valid_documents": valid_docs
    }
