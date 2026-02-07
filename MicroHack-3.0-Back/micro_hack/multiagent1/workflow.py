from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from state import GraphState
from agents.database_node import save_to_db_node, redis_push_node, DB_URI

# Import your agent nodes
from agents.agent_1_TextImprove import text_improve_node
from agents.agent_2_ClassifyDomain import classify_domain_node
from agents.agent_3_ImpactScoring import impact_scoring_node
from agents.agent_4_UrgencyScoring import urgency_scoring_node
from agents.agent_5_Tri import tri_node
from agents.agent_6_Extracter import extractor_node

# --- ReAct Conditional Logic ---
def check_domain(state): return "retry" if state.get("domain_confidence", 0) < 0.8 else "proceed"
def check_impact(state): return "retry" if state.get("impact_confidence", 0) < 0.8 else "proceed"
def check_urgency(state): return "retry" if state.get("urgency_confidence", 0) < 0.8 else "proceed"
def check_tri(state): return "retry" if state.get("tri_confidence", 0) < 0.8 else "proceed"

def create_app():
    # 2. Build Graph
    builder = StateGraph(GraphState)

    builder.add_node("text_improve", text_improve_node)
    builder.add_node("classify", classify_domain_node)
    builder.add_node("impact", impact_scoring_node)
    builder.add_node("urgency", urgency_scoring_node)
    builder.add_node("tri", tri_node)
    builder.add_node("extractor", extractor_node)
    builder.add_node("db_save", save_to_db_node)
    builder.add_node("redis_push", redis_push_node)

    # Edges
    builder.add_edge(START, "text_improve")
    builder.add_edge("text_improve", "classify")

    builder.add_conditional_edges("classify", check_domain, {"retry": "classify", "proceed": "impact"})
    builder.add_conditional_edges("impact", check_impact, {"retry": "impact", "proceed": "urgency"})
    builder.add_conditional_edges("urgency", check_urgency, {"retry": "urgency", "proceed": "tri"})
    
    builder.add_edge("tri", "extractor")
    builder.add_edge("extractor", "db_save")
    builder.add_edge("db_save", "redis_push")
    builder.add_edge("redis_push", END)

    # 3. Memory/Checkpointing
    connection_kwargs = {"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row}
    pool = ConnectionPool(
        conninfo=DB_URI,
        min_size=1,           # Start with 1 connection, grow as needed
        max_size=10,          # Maximum concurrent connections
        timeout=30,           # Fail fast if can't get connection in 30s
        kwargs=connection_kwargs,
        open=True             # Open pool immediately and wait for first connection
    )
    checkpointer = PostgresSaver(pool)
    checkpointer.setup() 
    
    return builder.compile(checkpointer=checkpointer)
    # return builder.compile()

# Export app for main.py
app = create_app()
import os

def save_graph_image(app):
    try:
        # This creates a PNG of your workflow
        graph_png = app.get_graph().draw_mermaid_png()
        with open("graph_workflow.png", "wb") as f:
            f.write(graph_png)
        print("🖼️ Workflow graph saved as 'graph_workflow.png'")
    except Exception as e:
        print(f"Could not generate image: {e}")
        print("Tip: Install pygraphviz or use the mermaid text instead.")

if __name__ == "__main__":
    save_graph_image(app)