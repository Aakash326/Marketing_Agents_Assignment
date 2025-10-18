"""
Portfolio data service for accessing and managing portfolio information.
"""

import logging
import sys
import os
import pandas as pd
from typing import Dict, Any, List, Optional

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))

from src.tools.portfolio_tools import load_portfolio_data

logger = logging.getLogger(__name__)


class PortfolioService:
    """Service for managing portfolio data operations."""

    def __init__(self, portfolio_file_path: str = "portfolios.xlsx"):
        """
        Initialize portfolio service.

        Args:
            portfolio_file_path: Path to portfolio Excel file
        """
        self.portfolio_file_path = portfolio_file_path
        self._portfolio_cache: Optional[pd.DataFrame] = None

    def _load_portfolios(self) -> pd.DataFrame:
        """Load portfolio data with caching."""
        if self._portfolio_cache is None:
            try:
                self._portfolio_cache = load_portfolio_data(self.portfolio_file_path)
                logger.info(f"Loaded {len(self._portfolio_cache)} portfolio records")
            except Exception as e:
                logger.error(f"Failed to load portfolio data: {str(e)}")
                raise

        return self._portfolio_cache

    def get_client_portfolio(self, client_id: str) -> Dict[str, Any]:
        """
        Get portfolio data for a specific client.

        Args:
            client_id: Client identifier (e.g., 'CLT-001')

        Returns:
            Portfolio data dictionary

        Raises:
            ValueError: If client not found
        """
        try:
            df = self._load_portfolios()

            # Filter for specific client
            client_df = df[df['ClientID'] == client_id]

            if client_df.empty:
                raise ValueError(f"Client {client_id} not found")

            # Get client info
            first_row = client_df.iloc[0]
            client_name = first_row.get('ClientName', 'Unknown')

            # Calculate portfolio metrics
            holdings = []
            total_value = 0.0

            for _, row in client_df.iterrows():
                shares = row.get('Shares', 0)
                current_price = row.get('CurrentPrice', 0)
                market_value = shares * current_price
                total_value += market_value

                holding = {
                    "ticker": row.get('Ticker', ''),
                    "shares": float(shares),
                    "current_price": float(current_price),
                    "market_value": float(market_value),
                    "cost_basis": float(row.get('CostBasis', 0)) if 'CostBasis' in row else None,
                }

                # Calculate gain/loss if cost basis available
                if holding["cost_basis"]:
                    gain_loss = market_value - holding["cost_basis"]
                    gain_loss_pct = (gain_loss / holding["cost_basis"]) * 100 if holding["cost_basis"] > 0 else 0
                    holding["gain_loss"] = float(gain_loss)
                    holding["gain_loss_pct"] = float(gain_loss_pct)

                holdings.append(holding)

            return {
                "client_id": client_id,
                "client_name": client_name,
                "total_value": total_value,
                "holdings": holdings,
                "cash_balance": first_row.get('CashBalance', None),
                "ytd_return": first_row.get('YTDReturn', None)
            }

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error getting portfolio for {client_id}: {str(e)}")
            raise Exception(f"Failed to retrieve portfolio: {str(e)}")

    def get_all_clients(self) -> List[Dict[str, Any]]:
        """
        Get list of all clients with basic info.

        Returns:
            List of client dictionaries
        """
        try:
            df = self._load_portfolios()

            # Group by client
            clients = []
            for client_id in df['ClientID'].unique():
                client_df = df[df['ClientID'] == client_id]
                first_row = client_df.iloc[0]

                # Calculate total portfolio value
                total_value = (client_df['Shares'] * client_df['CurrentPrice']).sum()

                clients.append({
                    "client_id": client_id,
                    "client_name": first_row.get('ClientName', 'Unknown'),
                    "portfolio_value": float(total_value)
                })

            return clients

        except Exception as e:
            logger.error(f"Error getting client list: {str(e)}")
            raise Exception(f"Failed to retrieve clients: {str(e)}")

    def refresh_cache(self):
        """Force refresh of portfolio cache."""
        self._portfolio_cache = None
        logger.info("Portfolio cache cleared")

    def health_check(self) -> Dict[str, str]:
        """
        Check if portfolio service is healthy.

        Returns:
            Health status dictionary
        """
        try:
            if not os.path.exists(self.portfolio_file_path):
                return {"status": "unhealthy", "message": f"Portfolio file not found: {self.portfolio_file_path}"}

            # Try to load data
            df = self._load_portfolios()

            if df.empty:
                return {"status": "unhealthy", "message": "Portfolio file is empty"}

            return {"status": "healthy", "message": f"{len(df)} portfolio records loaded"}

        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}


# Global service instance
_portfolio_service: Optional[PortfolioService] = None


def get_portfolio_service(portfolio_file_path: str = "portfolios.xlsx") -> PortfolioService:
    """Get or create the global portfolio service instance."""
    global _portfolio_service

    if _portfolio_service is None:
        _portfolio_service = PortfolioService(portfolio_file_path)

    return _portfolio_service
