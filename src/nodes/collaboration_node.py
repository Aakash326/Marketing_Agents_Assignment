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
    if portfolio_data and "holdings" in portfolio_data:
        holdings_count = len(portfolio_data["holdings"])
        portfolio_summary = f"Portfolio has {holdings_count} holdings:\n"
        for holding in portfolio_data["holdings"][:5]:  # Top 5
            portfolio_summary += f"- {holding['symbol']}: {holding['quantity']} shares\n"

    market_summary = ""
    if market_data:
        market_summary = "Market data available for:\n"
        for ticker, data in list(market_data.items())[:5]:  # Top 5
            if "error" not in data:
                price = data.get('current_price', 0)
                change = data.get('day_change_pct', 0)
                market_summary += f"- {ticker}: ${price:.2f} ({change:+.2f}%)\n"

    # Create collaboration prompt based on mode
    if not wants_recommendations:
        # INFORMATION MODE: Synthesize facts
        collaboration_prompt = f"""You are a collaboration agent that synthesizes findings from multiple analysis agents.

# RESPONSE GUIDELINES:
# - Connect portfolio holdings with market data
# - Show clear relationships and impacts
# - Use specific numbers and facts
# - DO NOT give investment recommendations
# - Just synthesize the information

User Query: "{query}"

Portfolio Information:
{portfolio_summary}

Market Information:
{market_summary}

Previous Agent Responses:
{existing_response}

Your task:
1. Identify which portfolio holdings are mentioned in the query
2. Connect market data to those specific holdings
3. Calculate specific impacts (e.g., if stock up 5%, what's the dollar impact on holdings?)
4. Provide a clear, synthesized answer

IMPORTANT: Be factual and specific. Show connections clearly. NO recommendations.

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

    Args:
        state: Current graph state

    Returns:
        True if collaboration is needed
    """
    query = state.get("query", "").lower()

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

    return (has_market and has_portfolio) or has_both_data
