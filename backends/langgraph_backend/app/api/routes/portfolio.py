"""
Portfolio management endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import pandas as pd
import os
from datetime import datetime
import yfinance as yf

logger = logging.getLogger(__name__)

router = APIRouter()


def get_current_price(symbol: str, fallback_price: float) -> float:
    """
    Fetch current market price for a symbol using yfinance.

    Args:
        symbol: Stock ticker symbol
        fallback_price: Purchase price to use if fetch fails

    Returns:
        Current market price or fallback price
    """
    # Special case: CASH always has a price of $1.00
    if symbol.upper() == "CASH":
        return 1.00

    try:
        ticker = yf.Ticker(symbol)
        # Try to get current price from fast_info
        try:
            current_price = ticker.fast_info['lastPrice']
            if current_price and current_price > 0:
                return round(float(current_price), 2)
        except:
            pass

        # Fallback: Try historical data (last close)
        hist = ticker.history(period='1d')
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            if current_price and current_price > 0:
                return round(float(current_price), 2)

        # If all fails, return purchase price (no change)
        logger.warning(f"Could not fetch price for {symbol}, using purchase price")
        return fallback_price

    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return fallback_price


class Holding(BaseModel):
    """Stock holding model."""
    symbol: str
    security_name: Optional[str] = None
    asset_class: Optional[str] = None
    sector: Optional[str] = None
    quantity: int
    purchase_price: float
    purchase_date: Optional[str] = None
    current_price: float = 0.0
    market_value: float = 0.0
    
    # Aliases for backwards compatibility
    @property
    def ticker(self):
        return self.symbol
    
    @property
    def shares(self):
        return self.quantity
    
    @property
    def avg_price(self):
        return self.purchase_price


class Portfolio(BaseModel):
    """Portfolio model."""
    client_id: str
    client_name: str = "Unknown Client"
    total_value: float = 0.0
    holdings: List[Holding] = []
    last_updated: Optional[str] = None


def load_portfolio_from_excel(client_id: str) -> Optional[Portfolio]:
    """Load portfolio data from Excel file."""
    try:
        # Try to find the portfolios.xlsx file
        possible_paths = [
            "../../portfolios.xlsx",
            "../../../portfolios.xlsx",
            "portfolios.xlsx",
            "/Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents/portfolios.xlsx"
        ]
        
        excel_path = None
        for path in possible_paths:
            if os.path.exists(path):
                excel_path = path
                break
        
        if not excel_path:
            logger.warning(f"portfolios.xlsx not found, returning demo data")
            return None
        
        # Read the Excel file
        df = pd.read_excel(excel_path)
        
        # Filter by client ID
        client_data = df[df['client_id'] == client_id]
        
        if client_data.empty:
            return None
        
        # Build holdings list
        holdings = []
        total_value = 0.0
        
        for _, row in client_data.iterrows():
            # Get purchase price from Excel
            purchase_price = float(row['Purchase Price'])
            quantity = int(row['quantity'])
            symbol = str(row['symbol'])
            
            # Fetch real current price from yfinance
            current_price = get_current_price(symbol, purchase_price)
            
            market_value = quantity * current_price
            
            holding = Holding(
                symbol=symbol,
                security_name=str(row.get('security_name', row['symbol'])),
                asset_class=str(row.get('asset_class', 'Unknown')),
                sector=str(row.get('sector', 'Unknown')),
                quantity=quantity,
                purchase_price=purchase_price,
                purchase_date=str(row.get('purchase_date', '')),
                current_price=round(current_price, 2),
                market_value=round(market_value, 2)
            )
            holdings.append(holding)
            total_value += market_value
        
        # Use client_id as client name
        client_name = f"Client {client_id}"
        
        return Portfolio(
            client_id=client_id,
            client_name=client_name,
            total_value=round(total_value, 2),
            holdings=holdings
        )
        
    except Exception as e:
        logger.error(f"Error loading portfolio from Excel: {e}")
        return None


@router.get("/portfolios")
async def list_portfolios() -> List[dict]:
    """
    List all available portfolios.
    
    Returns:
        List of portfolios
    """
    logger.info("Listing portfolios")
    
    # Return demo list of clients
    clients = [{"id": f"CLT-{str(i+1).zfill(3)}", "name": f"Client {i+1}"} for i in range(10)]
    return clients


@router.get("/portfolio/{client_id}")
async def get_portfolio(client_id: str) -> Portfolio:
    """
    Get a specific portfolio by client ID.
    
    Args:
        client_id: The client identifier (e.g., CLT-001)
        
    Returns:
        Portfolio details
    """
    logger.info(f"Getting portfolio for client: {client_id}")
    
    # Try to load from Excel
    portfolio = load_portfolio_from_excel(client_id)
    
    if portfolio:
        return portfolio
    
    # Return demo data if not found
    logger.info(f"Returning demo data for {client_id}")
    
    import random
    demo_stocks = [
        ("AAPL", "Apple Inc.", "Technology"),
        ("MSFT", "Microsoft", "Technology"),
        ("GOOGL", "Alphabet", "Technology"),
        ("TSLA", "Tesla", "Automotive"),
        ("NVDA", "NVIDIA", "Semiconductors"),
        ("AMZN", "Amazon", "E-Commerce"),
    ]
    
    holdings = []
    total_value = 0.0
    
    for symbol, name, sector in random.sample(demo_stocks, k=random.randint(3, 5)):
        quantity = random.randint(10, 100)
        purchase_price = random.uniform(50, 300)
        current_price = purchase_price * random.uniform(0.9, 1.15)
        market_value = quantity * current_price
        
        holdings.append(Holding(
            symbol=symbol,
            security_name=name,
            asset_class="Stock",
            sector=sector,
            quantity=quantity,
            purchase_price=round(purchase_price, 2),
            current_price=round(current_price, 2),
            market_value=round(market_value, 2)
        ))
        total_value += market_value
    
    return Portfolio(
        client_id=client_id,
        client_name=f"Demo Client {client_id}",
        total_value=round(total_value, 2),
        holdings=holdings
    )


@router.get("/portfolio/{client_id}/summary")
async def get_portfolio_summary(client_id: str) -> Dict[str, Any]:
    """
    Returns portfolio summary for dashboard:
    - Total holdings count
    - Total portfolio value
    - Asset allocation breakdown
    - Top performing holdings
    - Sector distribution
    """
    logger.info(f"Getting portfolio summary for client: {client_id}")

    try:
        # Load portfolio data
        portfolio = load_portfolio_from_excel(client_id)

        if not portfolio:
            raise HTTPException(status_code=404, detail=f"Portfolio not found for client {client_id}")

        # Calculate metrics
        total_holdings = len(portfolio.holdings)

        # Asset allocation
        asset_allocation = {}
        for holding in portfolio.holdings:
            asset_class = holding.asset_class or "Unknown"
            if asset_class in asset_allocation:
                asset_allocation[asset_class] += holding.market_value
            else:
                asset_allocation[asset_class] = holding.market_value

        allocation_data = [
            {"name": asset, "value": round(value, 2)}
            for asset, value in asset_allocation.items()
        ]

        # Sector distribution
        sector_dist = {}
        for holding in portfolio.holdings:
            sector = holding.sector or "Unknown"
            if sector in sector_dist:
                sector_dist[sector] += holding.market_value
            else:
                sector_dist[sector] = holding.market_value

        sector_data = [
            {"name": sector, "value": round(value, 2)}
            for sector, value in sector_dist.items()
        ]

        # Top holdings by market value
        sorted_holdings = sorted(portfolio.holdings, key=lambda x: x.market_value, reverse=True)
        top_holdings = [
            {
                "symbol": h.symbol,
                "security_name": h.security_name,
                "quantity": h.quantity,
                "market_value": h.market_value
            }
            for h in sorted_holdings[:5]
        ]

        return {
            "client_id": client_id,
            "total_holdings": total_holdings,
            "total_value": portfolio.total_value,
            "asset_allocation": allocation_data,
            "sector_distribution": sector_data,
            "top_holdings": top_holdings,
            "last_updated": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting portfolio summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolio/{client_id}/query-suggestions")
async def get_query_suggestions(client_id: str) -> Dict[str, List[str]]:
    """
    Returns contextual query suggestions based on client's portfolio
    """
    logger.info(f"Getting query suggestions for client: {client_id}")

    try:
        portfolio = load_portfolio_from_excel(client_id)

        if not portfolio:
            raise HTTPException(status_code=404, detail=f"Portfolio not found for client {client_id}")

        # Get unique symbols for personalized suggestions
        symbols = [h.symbol for h in sorted(portfolio.holdings, key=lambda x: x.market_value, reverse=True)[:3]]

        suggestions = {
            "portfolio": [
                "Show me my complete portfolio",
                "What's my total portfolio value?",
                "Which stocks do I own the most of?",
                "What's my asset allocation?"
            ],
            "performance": [
                "Which of my holdings performed best?",
                f"How is {symbols[0]} doing in my portfolio?" if symbols else "How are my holdings performing?",
                "What are my top gainers?",
                "Show me my portfolio returns"
            ],
            "market": [
                f"What's the current price of {symbols[0]}?" if symbols else "Get current stock prices",
                f"Get latest news on {symbols[1]}" if len(symbols) > 1 else "What's the latest market news?",
                "How are tech stocks performing today?",
                "What are the market trends?"
            ],
            "analysis": [
                "Analyze my portfolio risk",
                "What sectors am I exposed to?",
                "Should I rebalance my portfolio?",
                "Compare my holdings to market benchmarks"
            ]
        }

        return suggestions

    except Exception as e:
        logger.error(f"Error getting query suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))
