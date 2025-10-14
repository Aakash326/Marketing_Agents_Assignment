"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class QueryRequest(BaseModel):
    """Request model for portfolio query endpoint."""
    query: str = Field(..., description="User's question about portfolio or markets", min_length=1)
    client_id: str = Field(..., description="Client identifier (e.g., CLT-001)", pattern=r"^CLT-\d{3}$")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=[],
        description="Previous conversation messages"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What stocks do I own?",
                "client_id": "CLT-001",
                "session_id": None,
                "conversation_history": []
            }
        }


class AgentActivity(BaseModel):
    """Details about which agents were activated."""
    planner_used: bool = Field(description="Planning agent was used")
    portfolio_used: bool = Field(description="Portfolio agent was used")
    market_used: bool = Field(description="Market agent was used")
    collaboration_used: bool = Field(description="Collaboration agent was used")
    validator_used: bool = Field(description="Validator agent was used")


class QueryMetadata(BaseModel):
    """Metadata about query execution."""
    query_time_ms: int = Field(description="Query execution time in milliseconds")
    timestamp: str = Field(description="ISO timestamp of response")


class QueryResponse(BaseModel):
    """Response model for portfolio query endpoint."""
    success: bool = Field(description="Whether the query was successful")
    session_id: str = Field(description="Session ID for this conversation")
    response: str = Field(description="AI-generated response to the query")
    needs_clarification: bool = Field(description="Whether the query needs clarification")
    clarification_message: Optional[str] = Field(description="Clarification request if needed")
    agent_activity: AgentActivity = Field(description="Details about agent activation")
    metadata: QueryMetadata = Field(description="Query execution metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "response": "You own 6 holdings: VTI, BND, VXUS...",
                "needs_clarification": False,
                "clarification_message": None,
                "agent_activity": {
                    "planner_used": True,
                    "portfolio_used": True,
                    "market_used": False,
                    "collaboration_used": False,
                    "validator_used": True
                },
                "metadata": {
                    "query_time_ms": 1234,
                    "timestamp": "2025-01-15T10:30:00Z"
                }
            }
        }


class ClarificationRequest(BaseModel):
    """Request model for clarification follow-up."""
    session_id: str = Field(..., description="Session ID from previous query")
    clarification: str = Field(..., description="User's clarification response", min_length=1)
    original_query: str = Field(..., description="Original ambiguous query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "clarification": "AAPL",
                "original_query": "How's that stock doing?"
            }
        }


class ConversationMessage(BaseModel):
    """A single message in conversation history."""
    role: str = Field(..., description="Message role (user or assistant)")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp")


class SessionResponse(BaseModel):
    """Response model for session details."""
    session_id: str = Field(description="Unique session identifier")
    client_id: str = Field(description="Associated client ID")
    conversation_history: List[Dict[str, str]] = Field(description="Conversation messages")
    created_at: datetime = Field(description="Session creation timestamp")
    last_activity: datetime = Field(description="Last activity timestamp")
    message_count: int = Field(description="Number of messages in conversation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "client_id": "CLT-001",
                "conversation_history": [
                    {"role": "user", "content": "What stocks do I own?"},
                    {"role": "assistant", "content": "You own 6 holdings..."}
                ],
                "created_at": "2025-01-15T10:00:00",
                "last_activity": "2025-01-15T10:30:00",
                "message_count": 2
            }
        }


class SessionDeleteResponse(BaseModel):
    """Response model for session deletion."""
    success: bool = Field(description="Whether deletion was successful")
    message: str = Field(description="Status message")
    session_id: str = Field(description="Deleted session ID")


class HoldingInfo(BaseModel):
    """Information about a portfolio holding."""
    symbol: str = Field(description="Stock ticker symbol")
    security_name: str = Field(description="Full security name")
    asset_class: str = Field(description="Asset class type")
    sector: str = Field(description="Market sector")
    quantity: float = Field(description="Number of shares")
    purchase_price: float = Field(description="Purchase price per share")
    purchase_date: str = Field(description="Date of purchase")


class PortfolioResponse(BaseModel):
    """Response model for client portfolio information."""
    client_id: str = Field(description="Client identifier")
    total_holdings: int = Field(description="Total number of holdings")
    holdings: List[HoldingInfo] = Field(description="List of portfolio holdings")
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "CLT-001",
                "total_holdings": 6,
                "holdings": [
                    {
                        "symbol": "VTI",
                        "security_name": "Vanguard Total Stock Market ETF",
                        "asset_class": "Equity ETF",
                        "sector": "Broad Market",
                        "quantity": 3500,
                        "purchase_price": 121.06,
                        "purchase_date": "2024-01-16"
                    }
                ]
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(description="Service health status")
    service: str = Field(description="Service name")
    version: str = Field(description="API version")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(description="HTTP status code")
