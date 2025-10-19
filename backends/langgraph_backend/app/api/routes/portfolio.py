"""
Portfolio management endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
import pandas as pd
import os

logger = logging.getLogger(__name__)

router = APIRouter()


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
            # Use purchase price as current price (can be enhanced with live data)
            purchase_price = float(row['Purchase Price'])
            current_price = purchase_price * (1 + (hash(str(row['symbol'])) % 20 - 10) / 100)  # Simulated price change
            quantity = int(row['quantity'])
            market_value = quantity * current_price
            
            holding = Holding(
                symbol=str(row['symbol']),
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
