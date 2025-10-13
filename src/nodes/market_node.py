"""
Market agent node for analyzing stock prices and market news.
"""

from typing import Dict
from src.llm.client import get_llm
from src.tools.market_tools import (
    get_multiple_stock_prices,
    search_stock_news,
    format_market_data_for_llm,
    format_news_for_llm
)
from src.tools.portfolio_tools import get_client_holdings


def market_node(state: Dict) -> Dict:
    """
    Fetch and analyze market data for relevant stocks.

    Args:
        state: Current graph state

    Returns:
        Updated state with market data and analysis
    """
    query = state.get("query", "")
    portfolio_data = state.get("portfolio_data", {})
    existing_response = state.get("response", "")
    wants_recommendations = state.get("wants_recommendations", False)

    # Determine which stocks to analyze
    tickers = []

    # If portfolio data is available, analyze those holdings
    if portfolio_data and "holdings" in portfolio_data:
        tickers = get_client_holdings(portfolio_data)

    # If no portfolio data, try to extract ticker from query
    if not tickers:
        # Simple ticker extraction (could be improved with regex)
        words = query.upper().split()
        common_tickers = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA",
            "SPY", "QQQ", "VTI", "BND", "VXUS"
        ]
        for word in words:
            if word in common_tickers:
                tickers.append(word)

    # Fetch market data
    market_data = {}
    if tickers:
        market_data = get_multiple_stock_prices(tickers)

    # Fetch news for top holdings (limit to 2 to avoid rate limits)
    news_data = {}
    top_tickers = tickers[:2]
    for ticker in top_tickers:
        if ticker.upper() != "CASH":
            news_items = search_stock_news(ticker)
            if news_items:
                news_data[ticker] = news_items

    # Format data for LLM
    market_text = format_market_data_for_llm(market_data)
    news_text = format_news_for_llm(news_data)

    # Create analysis prompt based on whether user wants recommendations
    if not wants_recommendations:
        # INFORMATION MODE: Just report market data
        analysis_prompt = f"""You are a market analysis agent providing factual market information.

# RESPONSE GUIDELINES:
# - Report prices, performance, and news factually
# - "What's the price?" → Report current price
# - "How's it performing?" → Show performance numbers
# - "What's the news?" → Summarize recent news
# - DO NOT suggest what to buy or sell
# - DO NOT give investment recommendations
# - Just report the market data

User Query: "{query}"

Market Data:
{market_text}

Recent News:
{news_text}
"""

        # If there's already a response from portfolio agent, build on it
        if existing_response:
            analysis_prompt += f"""

Previous Analysis (from Portfolio Agent):
{existing_response}

Based on the market data and news above, enhance the previous analysis by adding market insights.
Provide specific information about current prices, performance, and any relevant news.
Integrate this market information with the portfolio context.

IMPORTANT: Continue with the same factual tone. NO investment recommendations.

Enhanced Response:"""
        else:
            analysis_prompt += """

Based on the market data and news above, provide a factual answer to the user's query.
Be specific and reference actual prices and performance metrics.
DO NOT suggest what to buy or sell.

Response:"""

    else:
        # ADVISORY MODE: Provide market context for decision-making
        analysis_prompt = f"""You are a market analysis agent providing educational market context.

# RESPONSE GUIDELINES (Advisory Mode):
# - Provide market context for decision-making
# - Present considerations, NOT commands
# - Use "you might consider" NOT "you should"
# - Present market factors and trends, not directives

User Query: "{query}"

Market Data:
{market_text}

Recent News:
{news_text}
"""

        # If there's already a response from portfolio agent, build on it
        if existing_response:
            analysis_prompt += f"""

Previous Analysis (from Portfolio Agent):
{existing_response}

Based on the market data and news above, enhance the previous analysis with market considerations.
Use phrases like "one factor to consider" or "market conditions suggest" rather than "you should".
Present options and trade-offs based on market data.

IMPORTANT: Maintain the educational tone with disclaimers from the previous response.

Enhanced Response:"""
        else:
            analysis_prompt += """

Based on the market data and news above, provide market considerations.
Use phrases like "you might consider" or "one factor to consider".
Present market trends and factors, not commands.

IMPORTANT: End your response with:
"Note: This is educational analysis, not financial advice. Please consult a licensed financial advisor for personalized investment recommendations."

Response:"""

    # Get LLM analysis
    llm = get_llm(temperature=0.5)
    response = llm.invoke(analysis_prompt)
    analysis = response.content

    # Store market data in state
    return {
        **state,
        "market_data": market_data,
        "response": analysis
    }
