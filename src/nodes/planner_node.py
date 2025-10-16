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
    conversation_history = state.get("conversation_history", [])

    # Format conversation history if available (Feature 4: Session Management)
    history_context = ""
    if conversation_history and len(conversation_history) > 0:
        history_context = "\n\nPrevious Conversation (for context):\n"
        # Show last 3 interactions
        for msg in conversation_history[-3:]:
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")[:200]  # Truncate long messages
            history_context += f"{role}: {content}...\n"
        history_context += "\nIMPORTANT: Consider this history when interpreting the current query. User may reference previous responses (e.g., 'the first one', 'that stock', 'tell me more').\n"

    # Create planning prompt
    planning_prompt = f"""You are a planning agent for a portfolio and market intelligence system.

User Query: "{query}"
Client ID: {client_id}
{history_context}

Analyze this query and determine:
1. Does this query require portfolio data analysis? (Information about client's holdings, stocks they own, etc.)
2. Does this query require market data analysis? (Stock prices, news, market performance, etc.)
3. Is the user asking for investment advice/recommendations? (YES only if query explicitly contains: "how to improve", "what should I do", "recommendations", "suggestions", "advice", "how can I", "should I buy", "should I sell")

Consider these guidelines:
- Queries about "what stocks do I own" or "my holdings" → Need portfolio data, NO advice
- Queries about "price of [stock]" or "how is [stock] doing" → Need market data, NO advice
- Queries about "my [stock] holdings" or "[stock] in my portfolio" → Need BOTH portfolio and market data, NO advice
- Queries about portfolio performance, gains, losses, or returns → Need BOTH portfolio and market data, NO advice
- Queries asking "highest return" or "best performer" → Need BOTH portfolio and market data, NO advice
- Queries asking "how to improve" or "what should I do" → Need data + Wants advice

IMPORTANT: Most queries just want information. Only set "Wants Recommendations" to YES if the user explicitly asks for advice or suggestions.

Respond with your analysis and clear decisions in this format:
Analysis: [Your reasoning]
Portfolio Data Needed: [YES or NO]
Market Data Needed: [YES or NO]
Wants Recommendations: [YES or NO]
"""

    # Get LLM decision
    llm = get_llm(temperature=0.3)
    response = llm.invoke(planning_prompt)
    plan = response.content

    # Parse the response to extract decisions
    needs_portfolio = "Portfolio Data Needed: YES" in plan or "portfolio data needed: yes" in plan.lower()
    needs_market = "Market Data Needed: YES" in plan or "market data needed: yes" in plan.lower()
    wants_recommendations = "Wants Recommendations: YES" in plan or "wants recommendations: yes" in plan.lower()

    # Fallback logic if parsing fails - be conservative and enable both
    if not needs_portfolio and not needs_market:
        # If we can't parse, make educated guesses
        query_lower = query.lower()

        # Portfolio indicators
        portfolio_keywords = ["own", "holdings", "my stocks", "my portfolio", "what stocks"]
        needs_portfolio = any(keyword in query_lower for keyword in portfolio_keywords)

        # Market indicators
        market_keywords = ["price", "market", "news", "performance", "trading", "how is", "doing", "return", "gain", "loss", "profit"]
        needs_market = any(keyword in query_lower for keyword in market_keywords)

        # If query mentions a specific stock and portfolio, need both
        if "my" in query_lower and any(word in query_lower for word in ["stock", "holding"]):
            needs_portfolio = True
            needs_market = True
        
        # Queries about returns/performance need both portfolio and market data
        if any(keyword in query_lower for keyword in ["return", "gain", "loss", "profit", "performance"]):
            needs_portfolio = True
            needs_market = True

    # Fallback for wants_recommendations - only True if explicit advice keywords present
    if not wants_recommendations:
        query_lower = query.lower()
        advice_keywords = ["how to improve", "what should i do", "recommendations", "suggestions",
                          "advice", "how can i", "should i buy", "should i sell", "optimize",
                          "rebalance", "diversify"]
        wants_recommendations = any(keyword in query_lower for keyword in advice_keywords)

    return {
        **state,
        "plan": plan,
        "needs_portfolio": needs_portfolio,
        "needs_market": needs_market,
        "wants_recommendations": wants_recommendations
    }
