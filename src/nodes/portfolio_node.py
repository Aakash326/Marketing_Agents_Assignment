"""
Portfolio agent node for analyzing client portfolio data.
"""

import os
from pathlib import Path
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
    wants_recommendations = state.get("wants_recommendations", False)

    # Get path to portfolios.xlsx (in project root)
    project_root = Path(__file__).parent.parent.parent
    portfolio_file = project_root / "portfolios.xlsx"
    
    # Load portfolio data
    portfolio_data = load_portfolio_data(str(portfolio_file), client_id)

    # Format portfolio for LLM
    portfolio_text = format_portfolio_for_llm(portfolio_data)

    # Create analysis prompt based on whether user wants recommendations
    if not wants_recommendations:
        # INFORMATION MODE: Just answer the question factually

        # Check if this is a risk/diversification query
        query_lower = query.lower()
        is_risk_query = any(keyword in query_lower for keyword in
                           ["risk", "risky", "diversif", "allocation", "sector", "concentration"])

        if is_risk_query:
            # RISK ANALYSIS MODE
            analysis_prompt = f"""You are a portfolio risk analysis agent.

USER'S QUESTION: "{query}"

{portfolio_text}

CRITICAL INSTRUCTIONS - RISK PROFILE ANALYSIS:
You MUST analyze the risk profile and diversification of this portfolio. DO NOT just report the total value.

Perform the following analysis:

1. ASSET CLASS DISTRIBUTION:
   - Count how many holdings are in each asset class (Stocks, Bonds, ETFs, etc.)
   - Calculate percentage of portfolio in each asset class
   - Example: "60% Stocks, 30% Bonds, 10% ETFs"

2. SECTOR ALLOCATION:
   - List all sectors represented (Technology, Healthcare, Consumer, Financial, etc.)
   - Count holdings per sector
   - Identify dominant sectors
   - Example: "40% Technology, 25% Healthcare, 20% Consumer, 15% Financial"

3. CONCENTRATION RISK:
   - Are holdings too concentrated in one sector or asset class?
   - Is there over-reliance on a few positions?
   - Are holdings well-spread across different sectors?

4. RISK ASSESSMENT:
   - Overall risk level: Low, Moderate, or High
   - Diversification quality: Well-diversified, Moderately diversified, or Concentrated
   - Key risks identified

Provide a comprehensive risk profile analysis based on the portfolio data above.

Your response:"""
        else:
            # GENERAL INFORMATION MODE
            analysis_prompt = f"""You are a portfolio analysis agent.

USER'S QUESTION: "{query}"

IMPORTANT CONTEXT UNDERSTANDING:
- If the user asks about "total value", "portfolio value", "total worth" - they are asking for the SUM of all holding values
- Words like "TOTAL", "VALUE", "HOLD", "OWN", "DO" in questions are ENGLISH WORDS, NOT stock ticker symbols
- The portfolio data below ALREADY includes "Total Portfolio Value" calculated for you
- Simply read and report the total value from the data provided

{portfolio_text}

INSTRUCTIONS:
1. The data above already shows "Total Portfolio Value" - use that number
2. If they ask "what stocks do I own" - list the holdings
3. If they ask about "total value" or similar - report the "Total Portfolio Value" shown above
4. Do NOT search for ticker symbols like "TOTAL", "VALUE", "HOLD", "OWN" - these are English words
5. Be factual and direct

Your response:"""
    else:
        # ADVISORY MODE: Provide considerations with disclaimers
        analysis_prompt = f"""You are a portfolio analysis agent providing educational considerations.

# RESPONSE GUIDELINES (Advisory Mode):
# - Present considerations, NOT commands
# - Use "you might consider" NOT "you should"
# - Present options and factors, not directives
# - Always end with disclaimer

Client ID: {client_id}
User Query: "{query}"

Portfolio Data:
{portfolio_text}

The user is asking for investment considerations. Provide:
- Analysis of current portfolio composition
- Factors to consider (NOT commands like "you should buy X")
- Use phrases like "you might consider" or "one approach could be"
- Present options and trade-offs, not directives
- Be balanced and educational

IMPORTANT: End your response with this disclaimer:
"Note: This is educational analysis, not financial advice. Please consult a licensed financial advisor for personalized investment recommendations."

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
