"""
Workflow service for integrating with LangGraph workflow.
"""

import logging
import sys
import os
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))

from src.graph.workflow import run_workflow, create_workflow
from src.state.graph_state import GraphState

logger = logging.getLogger(__name__)


class WorkflowService:
    """Service for executing LangGraph workflows."""

    def __init__(self):
        """Initialize workflow service."""
        self.workflow_app = None
        self._initialize_workflow()

    def _initialize_workflow(self):
        """Initialize the LangGraph workflow application."""
        try:
            self.workflow_app = create_workflow()
            logger.info("LangGraph workflow initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize workflow: {str(e)}")
            raise

    async def execute_query(
        self,
        query: str,
        client_id: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Execute a user query through the LangGraph workflow.

        Args:
            query: User's natural language query
            client_id: Client identifier
            conversation_history: Previous conversation context

        Returns:
            Dict containing workflow results

        Raises:
            Exception: If workflow execution fails
        """
        start_time = datetime.utcnow()

        try:
            logger.info(f"Executing query for client {client_id}: {query[:100]}...")

            # Run workflow in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            final_state = await loop.run_in_executor(
                None,
                run_workflow,
                query,
                client_id,
                conversation_history or []
            )

            # Extract relevant information from final state
            result = self._process_workflow_result(final_state, start_time)

            logger.info(f"Query executed successfully in {result['metadata']['execution_time']:.2f}s")

            return result

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
            raise Exception(f"Failed to process query: {str(e)}")

    def _process_workflow_result(self, state: GraphState, start_time: datetime) -> Dict[str, Any]:
        """
        Process workflow final state into API response format.

        Args:
            state: Final workflow state
            start_time: Query start time

        Returns:
            Formatted result dictionary
        """
        execution_time = (datetime.utcnow() - start_time).total_seconds()

        # Determine which agents were used
        agents_used = ["planner"]

        if state.get("needs_portfolio"):
            agents_used.append("portfolio_agent")

        if state.get("needs_market"):
            agents_used.append("market_agent")

        if state.get("collaboration_findings"):
            agents_used.append("collaboration_agent")

        agents_used.append("validator")

        return {
            "answer": state.get("response", ""),
            "agents_used": agents_used,
            "portfolio_data": state.get("portfolio_data"),
            "market_data": state.get("market_data"),
            "collaboration_findings": state.get("collaboration_findings"),
            "needs_clarification": state.get("needs_clarification", False),
            "clarification_message": state.get("clarification_message", ""),
            "metadata": {
                "execution_time": execution_time,
                "workflow_steps": len(agents_used),
                "client_id": state.get("client_id"),
                "validated": state.get("validated", False),
                "plan": state.get("plan", "")
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    def health_check(self) -> Dict[str, str]:
        """
        Check if workflow service is healthy.

        Returns:
            Health status dictionary
        """
        try:
            if self.workflow_app is None:
                return {"status": "unhealthy", "message": "Workflow not initialized"}

            return {"status": "healthy", "message": "Workflow service operational"}

        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}


# Global service instance
_workflow_service: Optional[WorkflowService] = None


def get_workflow_service() -> WorkflowService:
    """Get or create the global workflow service instance."""
    global _workflow_service

    if _workflow_service is None:
        _workflow_service = WorkflowService()

    return _workflow_service
