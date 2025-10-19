"""
Query endpoint for portfolio intelligence queries.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging

# Project root is added to sys.path in main.py
from src.graph.workflow import run_workflow

logger = logging.getLogger(__name__)

router = APIRouter()


class QueryRequest(BaseModel):
    """Request model for portfolio queries."""
    query: str = Field(..., min_length=1, max_length=1000)
    client_id: str = Field(..., pattern=r"^CLT-\d{3}$")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default=None)


class QueryResponse(BaseModel):
    """Response model for portfolio queries."""
    answer: str
    agents_used: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    sources: List[str] = Field(default_factory=list)
    needs_clarification: bool = Field(default=False)
    clarification_message: Optional[str] = Field(default=None)


@router.post("/query", response_model=QueryResponse)
async def query_portfolio(request: QueryRequest) -> QueryResponse:
    """
    Process a natural language query about portfolios using LangGraph multi-agent workflow.

    Args:
        request: The query request containing the question, client_id, and optional conversation history

    Returns:
        QueryResponse with the answer, agents used, metadata, and sources
    """
    logger.info(f"Processing query for {request.client_id}: {request.query}")

    try:
        # Run the LangGraph workflow
        result = run_workflow(
            query=request.query,
            client_id=request.client_id,
            conversation_history=request.conversation_history or []
        )

        # Extract agents used from the workflow execution
        agents_used = []
        if result.get("needs_portfolio"):
            agents_used.append("portfolio_agent")
        if result.get("needs_market"):
            agents_used.append("market_agent")
        if result.get("collaboration_findings"):
            agents_used.append("collaboration_agent")
        agents_used.append("validator")

        # Build metadata
        metadata = {
            "validated": result.get("validated", False),
            "plan": result.get("plan", ""),
        }

        # Add collaboration findings if present
        if result.get("collaboration_findings"):
            metadata["collaboration"] = result["collaboration_findings"]

        # Build response
        response = QueryResponse(
            answer=result.get("response", "No response generated."),
            agents_used=agents_used,
            metadata=metadata,
            sources=result.get("sources", []),
            needs_clarification=result.get("needs_clarification", False),
            clarification_message=result.get("clarification_message")
        )

        logger.info(f"Query processed successfully. Agents used: {agents_used}")
        return response

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )
