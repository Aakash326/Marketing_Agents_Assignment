"""
Collaboration agent node for synthesizing findings from multiple agents.
Handles complex queries requiring cross-agent analysis.
"""

from typing import Dict
from src.llm.client import get_llm


def collaboration_node(state: Dict) -> Dict:
    """
    Synthesize findings from Portfolio and Market agents.
    Identifies connections between market events and portfolio holdings.

    Args:
        state: Current graph state

    Returns:
        Updated state with collaboration findings and enhanced response
    """
    query = state.get("query", "")
    portfolio_data = state.get("portfolio_data", {})
    market_data = state.get("market_data", {})
    existing_response = state.get("response", "")
    wants_recommendations = state.get("wants_recommendations", False)

    # Extract key information for synthesis
    portfolio_summary = ""
    returns_data = []  # Store calculated returns for each holding
    
    if portfolio_data and "holdings" in portfolio_data:
        holdings_count = len(portfolio_data["holdings"])
        portfolio_summary = f"Portfolio has {holdings_count} holdings:\n"
        
        for holding in portfolio_data["holdings"]:
            symbol = holding['symbol']
            quantity = holding['quantity']
            purchase_price = holding.get('purchase_price', 0)
            
            # Get current price from market data
            current_price = None
            if market_data and symbol in market_data:
                market_info = market_data[symbol]
                if "error" not in market_info:
                    current_price = market_info.get('current_price', None)
            
            # Calculate return if we have both prices
            if purchase_price and current_price and current_price > 0:
                return_pct = ((current_price - purchase_price) / purchase_price) * 100
                dollar_gain = (current_price - purchase_price) * quantity
                
                returns_data.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'purchase_price': purchase_price,
                    'current_price': current_price,
                    'return_pct': return_pct,
                    'dollar_gain': dollar_gain
                })
                
                portfolio_summary += f"- {symbol}: {quantity} shares @ ${purchase_price:.2f} (now ${current_price:.2f}, {return_pct:+.2f}% return, ${dollar_gain:+,.2f} gain)\n"
            else:
                portfolio_summary += f"- {symbol}: {quantity} shares @ ${purchase_price:.2f} (current price unavailable)\n"

    # Sort returns by percentage for easy comparison
    returns_data.sort(key=lambda x: x['return_pct'], reverse=True)

    market_summary = ""
    if market_data:
        market_summary = "Market data available for:\n"
        for ticker, data in list(market_data.items())[:10]:  # Show all
            if "error" not in data:
                price = data.get('current_price', 0)
                change = data.get('day_change_pct', 0)
                market_summary += f"- {ticker}: ${price:.2f} ({change:+.2f}% today)\n"

    # Create collaboration prompt based on mode
    if not wants_recommendations:
        # INFORMATION MODE: Synthesize facts
        collaboration_prompt = f"""You are a collaboration agent that synthesizes findings from multiple analysis agents.

# RESPONSE GUIDELINES:
# - Connect portfolio holdings with market data
# - Calculate and show returns (percentage and dollar gains)
# - Use specific numbers and facts
# - DO NOT give investment recommendations
# - Just synthesize the information

User Query: "{query}"

Portfolio Information with Returns:
{portfolio_summary}

Market Information:
{market_summary}

Previous Agent Responses:
{existing_response}

Your task:
1. If asked about returns/performance: Show calculated returns with specific percentages and dollar amounts
2. If asked "which has highest return": Clearly identify the best performer with its return percentage
3. Connect market data to specific holdings
4. Calculate specific impacts (e.g., if stock up 5%, what's the dollar impact?)
5. Provide a clear, synthesized answer with real numbers

IMPORTANT: Use the ACTUAL calculated returns shown above. Be factual and specific. NO recommendations.

Synthesized Response:"""

    else:
        # ADVISORY MODE: Synthesize with considerations
        collaboration_prompt = f"""You are a collaboration agent that synthesizes findings from multiple analysis agents.

# RESPONSE GUIDELINES (Advisory Mode):
# - Connect portfolio holdings with market events
# - Present considerations and factors
# - Use "you might consider" NOT "you should"
# - Show implications, not directives

User Query: "{query}"

Portfolio Information:
{portfolio_summary}

Market Information:
{market_summary}

Previous Agent Responses:
{existing_response}

Your task:
1. Identify which portfolio holdings are affected by market events
2. Analyze the implications for the client's position
3. Present factors to consider (NOT commands)
4. Provide educational synthesis with disclaimer

Use phrases like "this could impact" or "factors to consider include" rather than "you should".

IMPORTANT: End with disclaimer:
"Note: This is educational analysis, not financial advice. Please consult a licensed financial advisor for personalized investment recommendations."

Synthesized Response:"""

    # Get LLM synthesis
    llm = get_llm(temperature=0.5)
    response = llm.invoke(collaboration_prompt)
    synthesis = response.content

    # Store collaboration findings
    collaboration_findings = {
        "synthesized": True,
        "portfolio_holdings_analyzed": len(portfolio_data.get("holdings", [])),
        "market_data_points": len(market_data) if market_data else 0,
        "synthesis": synthesis[:500]  # Store summary
    }

    return {
        **state,
        "collaboration_findings": collaboration_findings,
        "response": synthesis  # Replace response with synthesized version
    }


def needs_collaboration(state: Dict) -> bool:
    """
    Determine if a query needs collaboration agent.

    Collaboration is needed when query mentions BOTH:
    - Market events/news/specific stocks
    - Portfolio/holdings/impact context
    
    OR when query requires return/performance calculations

    Args:
        state: Current graph state

    Returns:
        True if collaboration is needed
    """
    query = state.get("query", "").lower()

    # Return/performance queries ALWAYS need collaboration (need to combine portfolio + market data)
    return_indicators = [
        "return", "gain", "loss", "profit", "performance",
        "highest", "best", "worst", "compared", "how much did", "how well"
    ]
    needs_return_calc = any(indicator in query for indicator in return_indicators)

    # Market event indicators
    market_indicators = [
        "news", "announcement", "partnership", "deal", "earnings",
        "report", "merger", "acquisition", "price", "stock price"
    ]

    # Portfolio impact indicators
    portfolio_indicators = [
        "my portfolio", "my holdings", "my stocks", "my position",
        "affect me", "impact on me", "impact my", "affect my"
    ]

    has_market = any(indicator in query for indicator in market_indicators)
    has_portfolio = any(indicator in query for indicator in portfolio_indicators)

    # Also check if both portfolio and market agents ran
    has_both_data = (
        state.get("portfolio_data") is not None and
        state.get("market_data") is not None
    )

    return needs_return_calc or (has_market and has_portfolio) or has_both_data
