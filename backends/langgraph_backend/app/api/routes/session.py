"""
Session management endpoints for conversation tracking.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from app.models.session import (
    create_session,
    get_conversation_history,
    get_session,
    delete_session,
    add_message,
    Message
)

logger = logging.getLogger(__name__)

router = APIRouter()


class CreateSessionRequest(BaseModel):
    """Request to create a new session."""
    client_id: str


class CreateSessionResponse(BaseModel):
    """Response with new session ID."""
    session_id: str
    client_id: str


class AddMessageRequest(BaseModel):
    """Request to add a message to a session."""
    role: str
    content: str
    metadata: Dict[str, Any] = {}


class ConversationHistoryResponse(BaseModel):
    """Response with conversation history."""
    session_id: str
    messages: List[Message]
    total_messages: int


@router.post("/sessions", response_model=CreateSessionResponse)
async def new_session(request: CreateSessionRequest):
    """
    Create a new conversation session.

    Args:
        request: Session creation request with client_id

    Returns:
        Session ID and client ID
    """
    logger.info(f"Creating new session for client: {request.client_id}")

    session_id = create_session(request.client_id)

    return CreateSessionResponse(
        session_id=session_id,
        client_id=request.client_id
    )


@router.get("/sessions/{session_id}/history", response_model=ConversationHistoryResponse)
async def get_history(session_id: str, limit: int = 10):
    """
    Get conversation history for a session.

    Args:
        session_id: Session identifier
        limit: Maximum number of messages to return

    Returns:
        Conversation history
    """
    logger.info(f"Getting history for session: {session_id}")

    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    history = get_conversation_history(session_id, limit)

    return ConversationHistoryResponse(
        session_id=session_id,
        messages=history,
        total_messages=len(session.messages)
    )


@router.post("/sessions/{session_id}/messages")
async def add_message_to_session(session_id: str, request: AddMessageRequest):
    """
    Add a message to a session.

    Args:
        session_id: Session identifier
        request: Message to add

    Returns:
        Success status
    """
    logger.info(f"Adding message to session: {session_id}")

    success = add_message(
        session_id=session_id,
        role=request.role,
        content=request.content,
        metadata=request.metadata
    )

    if not success:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return {"status": "success", "message": "Message added to session"}


@router.delete("/sessions/{session_id}")
async def remove_session(session_id: str):
    """
    Delete a session.

    Args:
        session_id: Session identifier

    Returns:
        Success status
    """
    logger.info(f"Deleting session: {session_id}")

    success = delete_session(session_id)

    if not success:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return {"status": "success", "message": "Session deleted"}


@router.get("/sessions/{session_id}")
async def get_session_info(session_id: str):
    """
    Get session information.

    Args:
        session_id: Session identifier

    Returns:
        Session details
    """
    logger.info(f"Getting session info: {session_id}")

    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return {
        "session_id": session.session_id,
        "client_id": session.client_id,
        "message_count": len(session.messages),
        "created_at": session.created_at.isoformat(),
        "updated_at": session.updated_at.isoformat()
    }
