"""
Portfolio analysis tools for reading and processing client portfolio data.
"""

import pandas as pd
from typing import Dict, List, Optional


def load_portfolio_data(excel_path: str, client_id: str) -> Dict:
    """
    Load portfolio data for a specific client from Excel file.

    Args:
        excel_path: Path to the portfolios.xlsx file
        client_id: Client identifier (e.g., 'CLT-001')

    Returns:
        Dictionary containing portfolio information for the client
    """
    try:
        df = pd.read_excel(excel_path)

        # Filter for specific client
        client_portfolio = df[df['client_id'] == client_id]

        if client_portfolio.empty:
            return {
                "error": f"No portfolio found for client {client_id}",
                "holdings": []
            }

        # Convert to list of holdings
        holdings = []
        for _, row in client_portfolio.iterrows():
            holding = {
                "symbol": row['symbol'],
                "security_name": row['security_name'],
                "asset_class": row['asset_class'],
                "quantity": row['quantity'],
                "purchase_date": str(row['purchase_date']),
                "purchase_price": row['Purchase Price'],
                "sector": row['sector']
            }
            holdings.append(holding)

        return {
            "client_id": client_id,
            "holdings": holdings,
            "total_holdings": len(holdings)
        }

    except Exception as e:
        return {
            "error": f"Error loading portfolio: {str(e)}",
            "holdings": []
        }


def get_client_holdings(portfolio_data: Dict) -> List[str]:
    """
    Extract list of stock tickers from portfolio data.

    Args:
        portfolio_data: Portfolio dictionary from load_portfolio_data

    Returns:
        List of stock ticker symbols
    """
    if "holdings" not in portfolio_data:
        return []

    tickers = [holding["symbol"] for holding in portfolio_data["holdings"]]
    return tickers


def calculate_portfolio_summary(
    portfolio_data: Dict,
    current_prices: Dict[str, float]
) -> Dict:
    """
    Calculate portfolio summary with current values and gains/losses.

    Args:
        portfolio_data: Portfolio dictionary from load_portfolio_data
        current_prices: Dictionary mapping ticker symbols to current prices

    Returns:
        Dictionary with portfolio summary statistics
    """
    if "holdings" not in portfolio_data or not portfolio_data["holdings"]:
        return {
            "total_value": 0,
            "total_cost": 0,
            "total_gain_loss": 0,
            "total_gain_loss_pct": 0,
            "holdings_summary": []
        }

    total_value = 0
    total_cost = 0
    holdings_summary = []

    for holding in portfolio_data["holdings"]:
        symbol = holding["symbol"]
        quantity = holding["quantity"]
        purchase_price = holding["purchase_price"]

        # Calculate cost basis
        cost_basis = quantity * purchase_price

        # Get current price (default to purchase price if not available)
        current_price = current_prices.get(symbol, purchase_price)
        current_value = quantity * current_price

        # Calculate gain/loss
        gain_loss = current_value - cost_basis
        gain_loss_pct = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0

        holdings_summary.append({
            "symbol": symbol,
            "security_name": holding["security_name"],
            "quantity": quantity,
            "purchase_price": purchase_price,
            "current_price": current_price,
            "cost_basis": cost_basis,
            "current_value": current_value,
            "gain_loss": gain_loss,
            "gain_loss_pct": gain_loss_pct
        })

        total_value += current_value
        total_cost += cost_basis

    total_gain_loss = total_value - total_cost
    total_gain_loss_pct = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0

    return {
        "total_value": total_value,
        "total_cost": total_cost,
        "total_gain_loss": total_gain_loss,
        "total_gain_loss_pct": total_gain_loss_pct,
        "holdings_summary": holdings_summary
    }


def format_portfolio_for_llm(portfolio_data: Dict) -> str:
    """
    Format portfolio data as a readable string for LLM consumption.

    Args:
        portfolio_data: Portfolio dictionary from load_portfolio_data

    Returns:
        Formatted string representation of portfolio
    """
    if "error" in portfolio_data:
        return f"Error: {portfolio_data['error']}"

    if not portfolio_data.get("holdings"):
        return "No holdings found in portfolio."

    # Calculate total portfolio value based on purchase prices
    total_value = 0.0
    for holding in portfolio_data["holdings"]:
        holding_value = holding['quantity'] * holding['purchase_price']
        total_value += holding_value

    output = f"Portfolio for {portfolio_data['client_id']}:\n\n"
    output += f"Total Holdings: {portfolio_data['total_holdings']}\n"
    output += f"Total Portfolio Value (at purchase prices): ${total_value:,.2f}\n\n"
    output += "Holdings Breakdown:\n"

    for i, holding in enumerate(portfolio_data["holdings"], 1):
        holding_value = holding['quantity'] * holding['purchase_price']
        output += f"{i}. {holding['security_name']} ({holding['symbol']})\n"
        output += f"   - Asset Class: {holding['asset_class']}\n"
        output += f"   - Sector: {holding['sector']}\n"
        output += f"   - Quantity: {holding['quantity']}\n"
        output += f"   - Purchase Price: ${holding['purchase_price']:.2f}\n"
        output += f"   - Purchase Date: {holding['purchase_date']}\n"
        output += f"   - Holding Value: ${holding_value:,.2f}\n\n"

    return output
