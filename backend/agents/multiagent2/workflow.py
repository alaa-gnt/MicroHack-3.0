import operator
from typing import Annotated, TypedDict, Union, List, Dict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

# Import your Tier-2 State and Agents
from state import Tier2State
from agents.tech_assessor import tech_assessment_node
from agents.stack_designer import tech_stack_node
from agents.market_analyst import market_analysis_node
from agents.feasibility_expert import feasibility_node
from agents.strategist import final_recommendation_node

# --- DB URI for Checkpointing ---
DB_URI = "postgresql://postgres:postgres@localhost:5432/microhack"

# --- ROUTING LOGIC (The ReAct Loops) ---

def route_tech(state: Tier2State):
    """Checks tech assessment quality."""
    # We check if confidence exists for 'tech', default to 0
    conf = state.get("confidences", {}).get("tech", 0)
    retries = state.get("retry_counts", {}).get("tech", 0)
    
    if conf < 0.7 and retries < 2:
        print(f"🔄 Tech Agent Low Confidence ({conf}). Retrying...")
        return "retry"
    return "proceed"

def route_stack(state: Tier2State):
    """Checks tech stack quality."""
    conf = state.get("confidences", {}).get("stack", 0)
    retries = state.get("retry_counts", {}).get("stack", 0)
    
    if conf < 0.7 and retries < 2:
        print(f"🔄 Stack Agent Low Confidence ({conf}). Retrying...")
        return "retry"
    return "proceed"

def route_market(state: Tier2State):
    """Checks market analysis quality."""
    conf = state.get("confidences", {}).get("market", 0)
    retries = state.get("retry_counts", {}).get("market", 0)
    
    if conf < 0.7 and retries < 2:
        print(f"🔄 Market Agent Low Confidence ({conf}). Retrying...")
        return "retry"
    return "proceed"

def route_feasibility(state: Tier2State):
    """The 'Auditor' loop: can send the whole project back to Stack Designer."""
    score = state.get("feasibility_score", 0)
    retries = state.get("retry_counts", {}).get("feasibility", 0)
    
    if score < 0.5 and retries < 2:
        print(f"⚠️ Project Feasibility Critical ({score}). Sending back to redesign Tech Stack.")
        return "retry"
    return "proceed"

# --- GRAPH CONSTRUCTION ---

def create_tier2_app():
    # 1. Initialize Builder
    builder = StateGraph(Tier2State)

    # 2. Add Nodes
    builder.add_node("tech_assessment", tech_assessment_node)
    builder.add_node("tech_stack", tech_stack_node)
    builder.add_node("market_analysis", market_analysis_node)
    builder.add_node("feasibility", feasibility_node)
    builder.add_node("strategist", final_recommendation_node)

    # 3. Define Edges with Conditional Loops
    
    # Entry point
    builder.add_edge(START, "tech_assessment")

    # Loop 1: Tech Assessment
    builder.add_conditional_edges(
        "tech_assessment", 
        route_tech, 
        {"retry": "tech_assessment", "proceed": "tech_stack"}
    )

    # Loop 2: Tech Stack
    builder.add_conditional_edges(
        "tech_stack", 
        route_stack, 
        {"retry": "tech_stack", "proceed": "market_analysis"}
    )

    # Loop 3: Market Analysis
    builder.add_conditional_edges(
        "market_analysis", 
        route_market, 
        {"retry": "market_analysis", "proceed": "feasibility"}
    )

    # Loop 4: The 'Pivot' Loop (Feasibility -> Stack)
    builder.add_conditional_edges(
        "feasibility", 
        route_feasibility, 
        {"retry": "tech_stack", "proceed": "strategist"}
    )

    # Exit point
    builder.add_edge("strategist", END)

    # 4. Persistence (Checkpointing)
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
    # Important: run checkpointer.setup() once in your init script or here
    
    return builder.compile(checkpointer=checkpointer)

# Export the app for the watcher script
app = create_tier2_app()