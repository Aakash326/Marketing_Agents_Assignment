"""
Portfolio agent node for analyzing client portfolio data.
"""

from typing import Dict
from src.llm.client import get_llm
from src.tools.portfolio_tools import (
    load_portfolio_data,
    format_portfolio_for_llm,
    get_client_holdings
)


def portfolio_node(state: Dict) -> Dict:
    """
    Load and analyze portfolio data for the client.

    Args:
        state: Current graph state

    Returns:
        Updated state with portfolio data and analysis
    """
    query = state.get("query", "")
    client_id = state.get("client_id", "")

    # Load portfolio data
    portfolio_data = load_portfolio_data("portfolios.xlsx", client_id)

    # Format portfolio for LLM
    portfolio_text = format_portfolio_for_llm(portfolio_data)

    # Create analysis prompt
    analysis_prompt = f"""You are a portfolio analysis agent helping a client understand their investments.

Client ID: {client_id}
User Query: "{query}"

Portfolio Data:
{portfolio_text}

Based on the portfolio data above, provide a helpful and accurate answer to the user's query.
Be specific and reference actual holdings from the portfolio.
If the query cannot be fully answered with just portfolio data, mention what additional information might be needed.

Response:"""

    # Get LLM analysis
    llm = get_llm(temperature=0.5)
    response = llm.invoke(analysis_prompt)
    analysis = response.content

    # Store portfolio data in state
    return {
        **state,
        "portfolio_data": portfolio_data,
        "response": analysis
    }
