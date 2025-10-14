"""
Session management service for handling conversation history.
Uses in-memory storage (can be upgraded to Redis/database later).
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class SessionService:
    """
    Manages user sessions and conversation history.
    
    Current Implementation: In-memory storage
    Future: Can be replaced with Redis or database
    """
    
    def __init__(self, max_conversation_history: int = 10):
        """
        Initialize session service.
        
        Args:
            max_conversation_history: Maximum number of messages to keep (5 Q&A pairs)
        """
        # In-memory storage: {session_id: session_data}
        self.sessions: Dict[str, Dict] = {}
        self.max_conversation_history = max_conversation_history
        logger.info(f"SessionService initialized with max_history={max_conversation_history}")
    
    def create_session(self, client_id: str) -> str:
        """
        Create a new session for a client.
        
        Args:
            client_id: Client identifier (e.g., CLT-001)
            
        Returns:
            Generated session ID
        """
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "session_id": session_id,
            "client_id": client_id,
            "conversation_history": [],
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        
        logger.info(f"Created new session: {session_id} for client: {client_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve session data by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data dictionary or None if not found
        """
        session = self.sessions.get(session_id)
        
        if session:
            logger.debug(f"Retrieved session: {session_id}")
        else:
            logger.warning(f"Session not found: {session_id}")
        
        return session
    
    def update_session(
        self, 
        session_id: str, 
        conversation_history: List[Dict[str, str]]
    ) -> bool:
        """
        Update conversation history for a session.
        
        Args:
            session_id: Session identifier
            conversation_history: Updated conversation messages
            
        Returns:
            True if successful, False if session not found
        """
        if session_id not in self.sessions:
            logger.error(f"Cannot update non-existent session: {session_id}")
            return False
        
        # Keep only the last N messages
        trimmed_history = conversation_history[-self.max_conversation_history:]
        
        self.sessions[session_id]["conversation_history"] = trimmed_history
        self.sessions[session_id]["last_activity"] = datetime.now()
        
        logger.info(
            f"Updated session: {session_id} "
            f"(messages: {len(trimmed_history)}/{len(conversation_history)})"
        )
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        
        logger.warning(f"Cannot delete non-existent session: {session_id}")
        return False
    
    def cleanup_old_sessions(self, hours: int = 24) -> int:
        """
        Remove sessions older than specified hours.
        
        Args:
            hours: Age threshold in hours
            
        Returns:
            Number of sessions deleted
        """
        now = datetime.now()
        cutoff_time = now - timedelta(hours=hours)
        
        to_delete = []
        for sid, session in self.sessions.items():
            if session["last_activity"] < cutoff_time:
                to_delete.append(sid)
        
        for sid in to_delete:
            del self.sessions[sid]
        
        if to_delete:
            logger.info(f"Cleaned up {len(to_delete)} old sessions (older than {hours}h)")
        
        return len(to_delete)
    
    def get_all_sessions(self) -> List[Dict]:
        """
        Get all active sessions (for debugging/monitoring).
        
        Returns:
            List of session data dictionaries
        """
        return list(self.sessions.values())
    
    def get_session_count(self) -> int:
        """
        Get count of active sessions.
        
        Returns:
            Number of active sessions
        """
        return len(self.sessions)
    
    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session exists, False otherwise
        """
        return session_id in self.sessions
