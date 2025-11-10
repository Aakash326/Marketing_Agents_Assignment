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
from src.tools.sec_tools import fetch_latest_filing, extract_risk_factors, format_sec_data_for_llm
from src.tools.rag_tools import SimpleKnowledgeBase


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
    conversation_history = state.get("conversation_history", [])

    # Determine which stocks to analyze
    tickers = []

    # If portfolio data is available, analyze those holdings
    if portfolio_data and "holdings" in portfolio_data:
        tickers = get_client_holdings(portfolio_data)

    # If no portfolio data, try to extract ticker from query
    if not tickers:
        # Enhanced ticker extraction with regex
        import re
        query_upper = query.upper()

        # Check conversation history for ticker mentions if query is very short (likely a follow-up)
        context_text = query_upper
        if len(query.split()) <= 3 and conversation_history:
            # User might be saying "yes", "tell me more", etc.
            # Look at last 2 messages for ticker context
            for msg in conversation_history[-4:]:
                if msg.get("role") in ["user", "assistant"]:
                    context_text += " " + msg.get("content", "").upper()

        # Common stock tickers to look for
        common_tickers = [
            "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "TSLA", "META", "NVDA", "AMD",
            "SPY", "QQQ", "VTI", "BND", "VXUS", "VYM", "VTEB", "VOO", "VEA",
            "NFLX", "DIS", "INTC", "CSCO", "ADBE", "CRM", "ORCL", "IBM"
        ]

        # Blacklist of common English words that look like tickers (excluding BUY which can be confused)
        english_words_blacklist = [
            "DATE", "YEAR", "RETURN", "GAIN", "LOSS", "HOLD", "BEST", "WORST",
            "TOP", "TOTAL", "VALUE", "PRICE", "STOCK", "HAVE", "DOES", "WHAT",
            "WHICH", "ABOUT", "FROM", "WITH", "THAT", "THIS", "THEM", "THEY",
            "SHOW", "TELL", "GIVE", "MAKE", "TAKE", "BEEN", "WERE", "WILL",
            "YOUR", "THEIR", "THERE", "WHERE", "WHEN", "WOULD", "COULD", "SHOULD",
            "BUY", "SELL"  # Added BUY and SELL to blacklist
        ]

        # Method 1: Look for exact word matches (separated by spaces)
        words = context_text.split()
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in common_tickers and clean_word not in english_words_blacklist:
                tickers.append(clean_word)

        # Method 2: If no tickers found, try to find any uppercase words that match stock patterns
        if not tickers:
            # Find 2-5 letter uppercase words (common ticker pattern)
            potential_tickers = re.findall(r'\b[A-Z]{2,5}\b', context_text)
            for ticker in potential_tickers:
                # Only accept if it's in common tickers AND not in blacklist
                if ticker in common_tickers and ticker not in english_words_blacklist:
                    tickers.append(ticker)

        # Method 3: Check for general stock recommendation queries
        # If still no tickers and query asks for general recommendations, provide popular stocks
        if not tickers:
            recommendation_patterns = [
                r'which\s+stock.*buy',
                r'what\s+stock.*buy',
                r'recommend.*stock',
                r'suggest.*stock',
                r'best\s+stock',
                r'good\s+stock.*buy',
                r'stock.*recommendation'
            ]

            query_lower = query.lower()
            is_general_recommendation = any(re.search(pattern, query_lower) for pattern in recommendation_patterns)

            if is_general_recommendation:
                # Provide a diversified set of popular stocks for analysis
                tickers = ["AAPL", "MSFT", "NVDA", "GOOGL"]

        # Remove duplicates
        tickers = list(set(tickers))

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

    # Fetch SEC filings for key holdings (limit to 2 to keep it simple and fast)
    sec_data = {}
    if tickers and len(tickers) > 0:
        # Only fetch for first 2 holdings to avoid slowness
        for ticker in tickers[:2]:
            if ticker.upper() != "CASH":
                try:
                    filing = fetch_latest_filing(ticker, "10-K")
                    if filing.get("success"):
                        risks = extract_risk_factors(filing["text"])
                        sec_data[ticker] = {
                            "filing_type": "10-K",
                            "risk_factors": risks
                        }
                except Exception as e:
                    print(f"Error fetching SEC filing for {ticker}: {e}")

    # Format SEC data
    sec_text = format_sec_data_for_llm(sec_data)

    # Search knowledge base for relevant context using RAG
    rag_context = ""
    try:
        kb = SimpleKnowledgeBase()
        kb_results = kb.search(query, n_results=3)

        if kb_results:
            rag_context = "\n\nRelevant Context from Knowledge Base:\n"
            rag_context += "=" * 60 + "\n"
            for result in kb_results:
                ticker = result['metadata'].get('ticker', 'Unknown')
                doc_type = result['metadata'].get('type', 'document')
                rag_context += f"\n[{ticker} - {doc_type}]:\n{result['text'][:500]}...\n"
    except Exception as e:
        rag_context = ""
        print(f"RAG search error: {e}")

    # Create analysis prompt based on whether user wants recommendations
    if not wants_recommendations:
        # INFORMATION MODE: Just report market data
        analysis_prompt = f"""You are a market analysis agent providing factual market information.

# RESPONSE GUIDELINES:
# - Use the Market Data provided below - it contains current prices and information
# - If market data is available for a ticker, report it directly
# - "What's the price of AAPL?" → Look in Market Data section and report AAPL's current price
# - "How's TSLA performing?" → Look in Market Data section and report TSLA's performance
# - DO NOT say "I don't have data" if it's actually present in the Market Data section below
# - DO NOT suggest what to buy or sell
# - DO NOT give investment recommendations
# - Just report the market data factually

User Query: "{query}"

Market Data:
{market_text}

{sec_text}

{rag_context}

Recent News:
{news_text}

IMPORTANT: Check the Market Data section above carefully. If there's price information for the requested stock, provide it. Don't say you don't have the data when it's listed above.
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
Be specific and reference actual prices and performance metrics from the Market Data section.
If the stock's data is shown above, report it. DO NOT say you don't have the data.

Response:"""

    else:
        # ADVISORY MODE: Provide market context for decision-making
        analysis_prompt = f"""You are a market analysis agent providing educational market context.

# RESPONSE GUIDELINES (Advisory Mode):
# - Provide market context for decision-making with specific reasons
# - For each stock analyzed, explain:
#   1. Current performance (price, % change)
#   2. Key strengths (market position, growth, sector trends)
#   3. Potential risks (volatility, market conditions, competition)
# - Present considerations, NOT commands
# - Use "you might consider" NOT "you should"
# - Present market factors and trends, not directives

User Query: "{query}"

Market Data:
{market_text}

{sec_text}

{rag_context}

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

Based on the market data and news above, provide a structured analysis:

For each stock, provide:
1. **Current Status**: Price and recent performance
2. **Strengths**: Why this might be an attractive option (e.g., strong fundamentals, growth potential, market position)
3. **Considerations**: Factors to be aware of (e.g., volatility, risks, market conditions)

Use educational phrases like "you might consider", "one factor to consider", or "investors often look at".

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
