"""
Stock analysis endpoint using AutoGen 6-agent workflow.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
import asyncio

# Project root is added to sys.path in main.py

logger = logging.getLogger(__name__)

router = APIRouter()


class StockAnalysisRequest(BaseModel):
    """Request model for stock analysis."""
    symbol: str
    portfolio_value: float = 100000.0
    risk_per_trade: float = 2.0
    question: Optional[str] = "Should I buy this stock?"


class StockAnalysisResponse(BaseModel):
    """Response model for stock analysis."""
    symbol: str
    recommendation: str
    confidence: int
    summary: str
    execution_plan: dict
    agent_outputs: dict
    timestamp: str


@router.post("/analyze-stock", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest):
    """
    Run the AutoGen 6-agent stock analysis workflow
    """
    try:
        logger.info(f"Starting 6-agent analysis for {request.symbol}")

        # Import the real AutoGen workflow
        from src.workflows.trading_workflow import run_fast_6agent_analysis

        logger.info(f"Successfully imported trading_workflow")

        # Run the real 6-agent analysis
        result = await run_fast_6agent_analysis(
            stock_symbol=request.symbol,
            question=request.question or "Should I buy this stock?"
        )
        
        # Convert to response format (result is a dict)
        return StockAnalysisResponse(
            symbol=result.get('symbol', request.symbol),
            recommendation=result.get('recommendation', 'HOLD'),
            confidence=result.get('confidence', 50),
            summary=result.get('summary', 'Analysis completed'),
            execution_plan=result.get('execution_plan', {}),
            agent_outputs=result.get('agent_outputs', {}),
            timestamp=result.get('timestamp', '')
        )
        
    except Exception as e:
        logger.error(f"Error in stock analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Stock analysis failed: {str(e)}"
        )


@router.get("/analyze-stock/{symbol}", response_model=StockAnalysisResponse)
async def analyze_stock_get(
    symbol: str,
    portfolio_value: float = 100000.0,
    risk_per_trade: float = 2.0
):
    """
    Run 6-agent AutoGen workflow to analyze a stock (GET endpoint).
    
    Args:
        symbol: Stock ticker symbol
        portfolio_value: Total portfolio value in USD
        risk_per_trade: Risk percentage per trade (1-5%)
        
    Returns:
        Comprehensive stock analysis from 6 AI agents
    """
    request = StockAnalysisRequest(
        symbol=symbol.upper(),
        portfolio_value=portfolio_value,
        risk_per_trade=risk_per_trade
    )
    
    return await analyze_stock(request)
