"""
LangGraph workflow orchestration for multi-agent portfolio analysis.
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from src.state.graph_state import GraphState
from src.nodes.planner_node import planner_node
from src.nodes.portfolio_node import portfolio_node
from src.nodes.market_node import market_node
from src.nodes.validator_node import validator_node


def route_after_planner(state: GraphState) -> Literal["portfolio_agent", "market_agent", "validator"]:
    """
    Route after planner based on what data is needed.

    If only portfolio needed -> portfolio_agent
    If only market needed -> market_agent
    If both needed -> portfolio_agent (then market_agent will follow)
    If neither needed -> validator (direct to end with planner's response)
    """
    needs_portfolio = state.get("needs_portfolio", False)
    needs_market = state.get("needs_market", False)

    if needs_portfolio:
        return "portfolio_agent"
    elif needs_market:
        return "market_agent"
    else:
        # No specific agent needed, just validate and end
        return "validator"


def route_after_portfolio(state: GraphState) -> Literal["market_agent", "validator"]:
    """
    Route after portfolio agent.

    If market data also needed -> market_agent
    Otherwise -> validator
    """
    needs_market = state.get("needs_market", False)

    if needs_market:
        return "market_agent"
    else:
        return "validator"


def create_workflow() -> StateGraph:
    """
    Create and compile the LangGraph workflow.

    Returns:
        Compiled workflow graph
    """
    # Create the graph with our state schema
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("portfolio_agent", portfolio_node)
    workflow.add_node("market_agent", market_node)
    workflow.add_node("validator", validator_node)

    # Set entry point
    workflow.add_edge(START, "planner")

    # Add conditional edges from planner
    workflow.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "portfolio_agent": "portfolio_agent",
            "market_agent": "market_agent",
            "validator": "validator"
        }
    )

    # Add conditional edges from portfolio agent
    workflow.add_conditional_edges(
        "portfolio_agent",
        route_after_portfolio,
        {
            "market_agent": "market_agent",
            "validator": "validator"
        }
    )

    # Market agent always goes to validator
    workflow.add_edge("market_agent", "validator")

    # Validator goes to END
    workflow.add_edge("validator", END)

    # Compile the workflow
    app = workflow.compile()

    return app


def run_workflow(query: str, client_id: str) -> dict:
    """
    Run the workflow with a user query.

    Args:
        query: User's question
        client_id: Client identifier (e.g., 'CLT-001')

    Returns:
        Final state after workflow execution
    """
    # Create workflow
    app = create_workflow()

    # Initialize state
    initial_state = {
        "query": query,
        "client_id": client_id,
        "portfolio_data": None,
        "market_data": None,
        "plan": "",
        "needs_portfolio": False,
        "needs_market": False,
        "wants_recommendations": False,
        "response": "",
        "validated": False,
        "messages": []
    }

    # Run the workflow
    final_state = app.invoke(initial_state)

    return final_state
