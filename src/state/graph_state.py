"""
Shared state definition for the LangGraph workflow.
Uses TypedDict to define the state schema.
"""

from typing import TypedDict, Optional, List, Dict


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
    wants_recommendations: bool  # True only if user explicitly asks for advice

    # Collaboration (Feature 3)
    collaboration_findings: Optional[dict]  # Synthesis from collaboration agent

    # Session management (Feature 4)
    conversation_history: List[Dict[str, str]]  # Previous Q&A pairs

    # Enhanced validation (Feature 5)
    needs_clarification: bool  # True if query is ambiguous
    clarification_message: str  # Question to ask user for clarification

    # Response and validation
    response: str
    validated: bool

    # Message history (for conversation context)
    messages: list
