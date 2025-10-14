"""
Workflow service that wraps the existing LangGraph workflow.
Handles query execution and response formatting.
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional
import time
import logging

# Add parent directory to path to import src modules
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.graph.workflow import run_workflow

logger = logging.getLogger(__name__)


class WorkflowService:
    """
    Service for executing the portfolio intelligence workflow.
    Wraps the existing LangGraph workflow with minimal changes.
    """
    
    @staticmethod
    async def execute_query(
        query: str,
        client_id: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict:
        """
        Execute the portfolio intelligence workflow.
        
        Args:
            query: User's question
            client_id: Client identifier (e.g., CLT-001)
            conversation_history: Previous conversation messages
            
        Returns:
            Structured result dictionary with formatted response
        """
        start_time = time.time()
        
        logger.info(f"Executing query for client {client_id}: '{query[:50]}...'")
        
        try:
            # Run the existing LangGraph workflow
            result = run_workflow(
                query=query,
                client_id=client_id,
                conversation_history=conversation_history or []
            )
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            logger.info(
                f"Query completed in {execution_time_ms}ms "
                f"(needs_clarification: {result.get('needs_clarification', False)})"
            )
            
            # Format response according to API schema
            formatted_result = {
                "success": True,
                "response": result.get("response", ""),
                "needs_clarification": result.get("needs_clarification", False),
                "clarification_message": result.get("clarification_message"),
                "agent_activity": {
                    "planner_used": True,  # Planner always runs
                    "portfolio_used": result.get("needs_portfolio", False),
                    "market_used": result.get("needs_market", False),
                    "collaboration_used": result.get("collaboration_findings") is not None,
                    "validator_used": result.get("validated", False)
                },
                "metadata": {
                    "query_time_ms": execution_time_ms,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
            }
            
            return formatted_result
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            logger.error(f"Query execution failed after {execution_time_ms}ms: {str(e)}", exc_info=True)
            
            # Return error response
            return {
                "success": False,
                "response": f"An error occurred while processing your query: {str(e)}",
                "needs_clarification": False,
                "clarification_message": None,
                "agent_activity": {
                    "planner_used": False,
                    "portfolio_used": False,
                    "market_used": False,
                    "collaboration_used": False,
                    "validator_used": False
                },
                "metadata": {
                    "query_time_ms": execution_time_ms,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
            }
    
    @staticmethod
    def validate_client_id(client_id: str) -> bool:
        """
        Validate client ID format.
        
        Args:
            client_id: Client identifier to validate
            
        Returns:
            True if valid, False otherwise
        """
        import re
        pattern = r"^CLT-\d{3}$"
        return bool(re.match(pattern, client_id))
