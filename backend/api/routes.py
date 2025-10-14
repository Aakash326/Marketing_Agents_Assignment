"""
API route definitions for Portfolio Intelligence endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional
import sys
import os
from pathlib import Path
import logging

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.api.models import (
    QueryRequest, QueryResponse,
    ClarificationRequest,
    SessionResponse, SessionDeleteResponse,
    PortfolioResponse, HoldingInfo
)
from backend.services.workflow_service import WorkflowService
from backend.services.session_service import SessionService
from src.tools.portfolio_tools import load_portfolio_data

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Service instances (will be initialized in main.py)
workflow_service = WorkflowService()
session_service_instance: Optional[SessionService] = None


def get_session_service() -> SessionService:
    """Dependency injection for session service."""
    if session_service_instance is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session service not initialized"
        )
    return session_service_instance


def set_session_service(service: SessionService):
    """Set the global session service instance."""
    global session_service_instance
    session_service_instance = service


@router.post("/query", response_model=QueryResponse, tags=["Query"])
async def query_portfolio(
    request: QueryRequest,
    session_svc: SessionService = Depends(get_session_service)
):
    """
    Main query endpoint for portfolio and market intelligence.
    
    Analyzes the query, routes to appropriate agents, and returns a comprehensive response.
    Handles session management and conversation history automatically.
    
    - **query**: User's question about portfolio or markets
    - **client_id**: Client identifier (format: CLT-XXX)
    - **session_id**: Optional session ID for conversation continuity
    - **conversation_history**: Optional previous conversation messages
    """
    try:
        logger.info(f"Received query from client {request.client_id}: '{request.query[:50]}...'")
        
        # Validate client ID format
        if not WorkflowService.validate_client_id(request.client_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid client_id format. Expected format: CLT-XXX (e.g., CLT-001)"
            )
        
        # Get or create session
        session_id = request.session_id
        if not session_id or not session_svc.session_exists(session_id):
            session_id = session_svc.create_session(request.client_id)
            logger.info(f"Created new session: {session_id}")
        
        session = session_svc.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create or retrieve session"
            )
        
        # Get conversation history
        conversation_history = request.conversation_history or session.get("conversation_history", [])
        
        # Execute workflow
        result = await workflow_service.execute_query(
            query=request.query,
            client_id=request.client_id,
            conversation_history=conversation_history
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["response"]
            )
        
        # Update conversation history if not clarification needed
        if not result["needs_clarification"]:
            conversation_history.append({"role": "user", "content": request.query})
            conversation_history.append({"role": "assistant", "content": result["response"]})
            session_svc.update_session(session_id, conversation_history)
        
        # Add session_id to response
        result["session_id"] = session_id
        
        logger.info(f"Successfully processed query for session: {session_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in query_portfolio: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query execution failed: {str(e)}"
        )


@router.post("/query/clarify", response_model=QueryResponse, tags=["Query"])
async def clarify_query(
    request: ClarificationRequest,
    session_svc: SessionService = Depends(get_session_service)
):
    """
    Handle clarification follow-up for ambiguous queries.
    
    Used when the system needs additional information to answer a query.
    Combines the original query with the clarification to generate a complete response.
    
    - **session_id**: Session ID from the original query
    - **clarification**: User's clarification response
    - **original_query**: The original ambiguous query
    """
    try:
        logger.info(f"Received clarification for session {request.session_id}: '{request.clarification}'")
        
        session = session_svc.get_session(request.session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {request.session_id}"
            )
        
        # Enhanced query with clarification
        enhanced_query = f"{request.original_query} ({request.clarification})"
        logger.info(f"Enhanced query: '{enhanced_query}'")
        
        # Execute workflow with enhanced query
        result = await workflow_service.execute_query(
            query=enhanced_query,
            client_id=session["client_id"],
            conversation_history=session.get("conversation_history", [])
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["response"]
            )
        
        # Update conversation history
        conversation_history = session.get("conversation_history", [])
        conversation_history.append({"role": "user", "content": enhanced_query})
        conversation_history.append({"role": "assistant", "content": result["response"]})
        session_svc.update_session(request.session_id, conversation_history)
        
        result["session_id"] = request.session_id
        
        logger.info(f"Successfully processed clarification for session: {request.session_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in clarify_query: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Clarification failed: {str(e)}"
        )


@router.get("/session/{session_id}", response_model=SessionResponse, tags=["Session"])
async def get_session(
    session_id: str,
    session_svc: SessionService = Depends(get_session_service)
):
    """
    Retrieve session details including conversation history.
    
    Returns complete session information including all conversation messages,
    timestamps, and metadata.
    
    - **session_id**: Unique session identifier
    """
    try:
        session = session_svc.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {session_id}"
            )
        
        # Add message count
        session_response = {
            **session,
            "message_count": len(session.get("conversation_history", []))
        }
        
        return session_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session {session_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve session: {str(e)}"
        )


@router.delete("/session/{session_id}", response_model=SessionDeleteResponse, tags=["Session"])
async def delete_session(
    session_id: str,
    session_svc: SessionService = Depends(get_session_service)
):
    """
    Delete a session and its conversation history.
    
    Permanently removes the session. This action cannot be undone.
    
    - **session_id**: Session identifier to delete
    """
    try:
        success = session_svc.delete_session(session_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {session_id}"
            )
        
        return {
            "success": True,
            "message": "Session deleted successfully",
            "session_id": session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


@router.get("/clients/{client_id}/portfolio", response_model=PortfolioResponse, tags=["Portfolio"])
async def get_client_portfolio(client_id: str):
    """
    Retrieve portfolio holdings for a specific client.
    
    Returns complete portfolio information including all holdings with
    purchase details, quantities, and sectors.
    
    - **client_id**: Client identifier (format: CLT-XXX)
    """
    try:
        logger.info(f"Fetching portfolio for client: {client_id}")
        
        # Validate client ID format
        if not WorkflowService.validate_client_id(client_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid client_id format. Expected format: CLT-XXX (e.g., CLT-001)"
            )
        
        # Load portfolio data (file is in parent directory)
        portfolio_file = os.path.join(os.path.dirname(__file__), "../../portfolios.xlsx")
        portfolio_data = load_portfolio_data(portfolio_file, client_id)
        
        if "error" in portfolio_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=portfolio_data["error"]
            )
        
        # Format holdings
        formatted_holdings = []
        for holding in portfolio_data.get("holdings", []):
            formatted_holdings.append(HoldingInfo(
                symbol=holding["symbol"],
                security_name=holding["security_name"],
                asset_class=holding["asset_class"],
                sector=holding["sector"],
                quantity=holding["quantity"],
                purchase_price=holding["purchase_price"],
                purchase_date=str(holding["purchase_date"])
            ))
        
        response = {
            "client_id": client_id,
            "total_holdings": portfolio_data["total_holdings"],
            "holdings": formatted_holdings
        }
        
        logger.info(f"Successfully retrieved {len(formatted_holdings)} holdings for {client_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching portfolio for {client_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load portfolio: {str(e)}"
        )
