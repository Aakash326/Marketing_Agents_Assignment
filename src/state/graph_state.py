"""
Shared state definition for the LangGraph workflow.
Uses TypedDict to define the state schema.
"""

from typing import TypedDict, Optional


class GraphState(TypedDict):
    """
    State schema for the multi-agent portfolio analysis workflow.

    This state is passed between all nodes in the LangGraph workflow.
    """
    # User inputs
    query: str
    client_id: str

    # Data collected by agents
    portfolio_data: Optional[dict]
    market_data: Optional[dict]

    # Planning and routing
    plan: str
    needs_portfolio: bool
    needs_market: bool

    # Response and validation
    response: str
    validated: bool

    # Message history (for conversation context)
    messages: list
