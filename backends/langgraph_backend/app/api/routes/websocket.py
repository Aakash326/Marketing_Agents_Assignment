"""
WebSocket endpoint for real-time agent status updates.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connected for session: {session_id}")

    def disconnect(self, session_id: str):
        """Remove a WebSocket connection."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket disconnected for session: {session_id}")

    async def send_status(self, session_id: str, agent: str, status: str, metadata: Dict = None):
        """
        Send agent status update to a specific session.

        Args:
            session_id: Session identifier
            agent: Agent name (planner, portfolio, market, collaboration, validator)
            status: Status (idle, working, complete, error)
            metadata: Additional metadata about the agent's execution
        """
        if session_id in self.active_connections:
            message = {
                "type": "agent_status",
                "agent": agent,
                "status": status,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
                logger.debug(f"Sent status update to {session_id}: {agent} - {status}")
            except Exception as e:
                logger.error(f"Error sending WebSocket message: {e}")
                self.disconnect(session_id)

    async def send_message(self, session_id: str, message_type: str, data: Dict):
        """
        Send a generic message to a specific session.

        Args:
            session_id: Session identifier
            message_type: Type of message
            data: Message data
        """
        if session_id in self.active_connections:
            message = {
                "type": message_type,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending WebSocket message: {e}")
                self.disconnect(session_id)


# Global connection manager instance
manager = ConnectionManager()


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time agent status updates.

    Args:
        websocket: WebSocket connection
        session_id: Unique session identifier
    """
    await manager.connect(session_id, websocket)

    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()

            # Echo back or handle commands
            try:
                message = json.loads(data)
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }))
                else:
                    await websocket.send_text(json.dumps({
                        "type": "ack",
                        "message": "Message received",
                        "original": data
                    }))
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info(f"Client {session_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        manager.disconnect(session_id)
