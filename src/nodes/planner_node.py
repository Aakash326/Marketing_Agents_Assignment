"""
Planner node that determines which agents should be activated.
"""

from typing import Dict
from src.llm.client import get_llm


def planner_node(state: Dict) -> Dict:
    """
    Analyze the user query and determine which agents need to be activated.

    Args:
        state: Current graph state

    Returns:
        Updated state with planning decisions
    """
    query = state.get("query", "")
    client_id = state.get("client_id", "")

    # Create planning prompt
    planning_prompt = f"""You are a planning agent for a portfolio and market intelligence system.

User Query: "{query}"
Client ID: {client_id}

Analyze this query and determine:
1. Does this query require portfolio data analysis? (Information about client's holdings, stocks they own, etc.)
2. Does this query require market data analysis? (Stock prices, news, market performance, etc.)

Consider these guidelines:
- Queries about "what stocks do I own" or "my holdings" → Need portfolio data
- Queries about "price of [stock]" or "how is [stock] doing" → Need market data
- Queries about "my [stock] holdings" or "[stock] in my portfolio" → Need BOTH portfolio and market data
- Queries about portfolio performance or gains/losses → Need BOTH

Respond with your analysis and clear decisions in this format:
Analysis: [Your reasoning]
Portfolio Data Needed: [YES or NO]
Market Data Needed: [YES or NO]
"""

    # Get LLM decision
    llm = get_llm(temperature=0.3)
    response = llm.invoke(planning_prompt)
    plan = response.content

    # Parse the response to extract decisions
    needs_portfolio = "Portfolio Data Needed: YES" in plan or "portfolio data needed: yes" in plan.lower()
    needs_market = "Market Data Needed: YES" in plan or "market data needed: yes" in plan.lower()

    # Fallback logic if parsing fails - be conservative and enable both
    if not needs_portfolio and not needs_market:
        # If we can't parse, make educated guesses
        query_lower = query.lower()

        # Portfolio indicators
        portfolio_keywords = ["own", "holdings", "my stocks", "my portfolio", "what stocks"]
        needs_portfolio = any(keyword in query_lower for keyword in portfolio_keywords)

        # Market indicators
        market_keywords = ["price", "market", "news", "performance", "trading", "how is", "doing"]
        needs_market = any(keyword in query_lower for keyword in market_keywords)

        # If query mentions a specific stock and portfolio, need both
        if "my" in query_lower and any(word in query_lower for word in ["stock", "holding"]):
            needs_portfolio = True
            needs_market = True

    return {
        **state,
        "plan": plan,
        "needs_portfolio": needs_portfolio,
        "needs_market": needs_market
    }
