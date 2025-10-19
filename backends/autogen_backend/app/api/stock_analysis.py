"""
Stock analysis endpoint using AutoGen 6-agent workflow
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging
import asyncio
from datetime import datetime
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, PROJECT_ROOT)

try:
    from src.workflows.trading_workflow import run_6agent_analysis
except ImportError as e:
    logging.error(f"Failed to import trading_workflow: {e}")
    run_6agent_analysis = None

logger = logging.getLogger(__name__)

router = APIRouter()


class StockAnalysisRequest(BaseModel):
    """Request model for stock analysis."""
    symbol: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    question: str = Field(..., min_length=5, max_length=500, description="Analysis question")
    portfolio_value: float = Field(default=100000.0, gt=0, description="Portfolio value in USD")
    risk_per_trade: float = Field(default=2.0, ge=0.1, le=10.0, description="Risk per trade percentage")


class StockAnalysisResponse(BaseModel):
    """Response model for stock analysis."""
    symbol: str
    question: str
    recommendation: str
    confidence: int
    summary: str
    execution_plan: str
    technical_analysis: Optional[str] = None
    fundamental_analysis: Optional[str] = None
    risk_assessment: Optional[str] = None
    agent_outputs: Dict[str, str]
    timestamp: str


@router.post("/stock-analysis", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest) -> StockAnalysisResponse:
    """
    Analyze a stock using the 6-agent AutoGen workflow.

    This endpoint orchestrates 6 specialized agents:
    1. OrganiserAgent - Collects market data and technical indicators
    2. RiskManager - Calculates position sizing and stop-loss levels
    3. DataAnalyst - Fetches fundamental data and news
    4. QuantitativeAnalyst - Generates technical signals
    5. StrategyDeveloper - Determines entry/exit strategy
    6. ReportAgent - Synthesizes final recommendation

    Args:
        request: Stock analysis request with symbol and question

    Returns:
        Comprehensive analysis with recommendation and agent outputs
    """
    logger.info(f"Processing stock analysis request: {request.symbol} - {request.question}")

    if run_6agent_analysis is None:
        raise HTTPException(
            status_code=500,
            detail="Trading workflow not available. Please check AutoGen installation."
        )

    try:
        # Run the 6-agent workflow asynchronously
        result = await run_6agent_analysis(
            request.symbol,
            request.question
        )

        # TradingWorkflowResult already contains structured data
        # Extract execution plan as string from the dict
        execution_plan_str = str(result.execution_plan) if result.execution_plan else "No execution plan generated"

        # Build response using the structured result
        response = StockAnalysisResponse(
            symbol=result.symbol,
            question=request.question,
            recommendation=result.recommendation,
            confidence=result.confidence,
            summary=result.summary,
            execution_plan=execution_plan_str,
            technical_analysis=result.agent_outputs.get('QuantitativeAnalyst', 'No technical analysis available'),
            fundamental_analysis=result.agent_outputs.get('DataAnalyst', 'No fundamental analysis available'),
            risk_assessment=result.agent_outputs.get('RiskManager', 'No risk assessment available'),
            agent_outputs=result.agent_outputs,
            timestamp=result.timestamp
        )

        logger.info(f"Analysis completed successfully: {result.recommendation} with {result.confidence}% confidence")
        return response

    except Exception as e:
        logger.error(f"Error during stock analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/agents/status")
async def get_agents_status():
    """Get status of all 6 agents."""
    return {
        "agents": [
            {"name": "OrganiserAgent", "status": "ready", "description": "Market data & technical analysis"},
            {"name": "RiskManager", "status": "ready", "description": "Position sizing & risk management"},
            {"name": "DataAnalyst", "status": "ready", "description": "Fundamental analysis & news"},
            {"name": "QuantitativeAnalyst", "status": "ready", "description": "Technical signal generation"},
            {"name": "StrategyDeveloper", "status": "ready", "description": "Entry/exit strategy"},
            {"name": "ReportAgent", "status": "ready", "description": "Final recommendation synthesis"}
        ],
        "workflow_available": run_6agent_analysis is not None
    }
