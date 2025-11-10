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
        # Show last 4 interactions (8 messages: 4 user + 4 assistant)
        for msg in conversation_history[-8:]:
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")[:300]  # Show more context
            history_context += f"{role}: {content}\n"
        history_context += "\nCRITICAL: The current query may be a follow-up response. Check if:\n"
        history_context += "- User says 'yes', 'no', 'sure', 'okay' → They're answering a question from previous response\n"
        history_context += "- User says 'tell me more', 'what about', 'and' → They want more info about the previous topic\n"
        history_context += "- User mentions 'that', 'it', 'the first one', 'the second stock' → They're referencing previous response\n"
        history_context += "- If unclear what they're referring to, use the assistant's LAST response as the main context\n"

    # Create planning prompt
    planning_prompt = f"""You are a planning agent for a portfolio and market intelligence system.

User Query: "{query}"
Client ID: {client_id}
{history_context}

STEP 1: INTERPRET THE QUERY WITH CONTEXT
- If the query is very short ("yes", "no", "sure", "tell me more", "what about it"), look at the previous assistant response
- Extract what the user is actually asking about from the conversation history
- Combine the current query with the context to understand the FULL intent

STEP 2: ANALYZE DATA NEEDS
Analyze this query and determine:
1. Does this query require portfolio data analysis? (Information about client's holdings, stocks they own, portfolio value, etc.)
2. Does this query require market data analysis? (Real-time stock prices, news, market performance, current valuations, etc.)
3. Is the user asking for investment advice/recommendations? (YES only if query explicitly contains: "how to improve", "what should I do", "recommendations", "suggestions", "advice", "how can I", "should I buy", "should I sell")

Consider these guidelines:
- Queries about "what stocks do I own", "my holdings", "what do I have" → Portfolio data ONLY, NO advice
- Queries about "total value", "portfolio value", "total worth", "how much", "value I hold" → Portfolio data ONLY, NO advice
- Queries about "risk profile", "how risky", "diversified", "diversity", "allocation" → Portfolio data ONLY, NO advice
- Queries about "price of [stock]" or "how is [stock] doing" (without "my") → Market data ONLY, NO advice
- Queries about "my market", "my stocks", "about my market" → BOTH portfolio and market data, NO advice (analyze user's holdings)
- Queries about "my [stock] holdings" or "[stock] in my portfolio" → BOTH portfolio and market data, NO advice
- Queries about portfolio performance, gains, losses, or returns → BOTH portfolio and market data, NO advice
- Queries asking "highest return", "best performer", "worst performer" → BOTH portfolio and market data, NO advice
- Queries asking "how to improve", "what should I do", "optimize", "rebalance" → Data + Wants advice

IMPORTANT CONTEXT UNDERSTANDING:
- "total value" means total portfolio value (sum of all holdings)
- "value I hold" means total portfolio value
- "how much do I have" means total portfolio value
- Ignore common English words like "DO", "OWN", "HOLD", "TOTAL", "BUY", "SELL" as ticker symbols - these are action verbs, not stock symbols
- If query mentions "my" or "I" - it's about the CLIENT'S portfolio, not searching for stocks
- "Should I buy AAPL?" → This is asking about AAPL stock, NOT about a stock ticker called "BUY"
- "Which stock should I buy?" → This is asking for stock recommendations
- Stock ticker symbols are 1-5 uppercase letters (AAPL, MSFT, TSLA, etc.), not action verbs like BUY/SELL

IMPORTANT: Most queries just want information. Only set "Wants Recommendations" to YES if the user explicitly asks for advice or suggestions.

Respond with your analysis and clear decisions in this format:
Context Interpretation: [What is the user actually asking about, considering conversation history?]
Full Intent: [The complete question when combining current query + history context]
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
        portfolio_keywords = ["own", "holdings", "my stocks", "my portfolio", "what stocks",
                            "total value", "portfolio value", "total worth", "how much",
                            "value i hold", "my total", "what do i have",
                            "risk profile", "how risky", "diversified", "diversity",
                            "allocation", "sector allocation"]
        needs_portfolio = any(keyword in query_lower for keyword in portfolio_keywords)

        # Market indicators
        market_keywords = ["price", "market", "news", "performance", "trading", "how is", "doing", "return", "gain", "loss", "profit", "which stock", "what stock", "stock recommendation", "should i buy", "should i sell"]
        needs_market = any(keyword in query_lower for keyword in market_keywords)

        # If query mentions "my" with market/stock keywords, need both portfolio and market
        if "my" in query_lower and any(word in query_lower for word in ["stock", "holding", "market", "portfolio"]):
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
                          "rebalance", "diversify", "which stock", "what stock", "recommend"]
        wants_recommendations = any(keyword in query_lower for keyword in advice_keywords)

    return {
        **state,
        "plan": plan,
        "needs_portfolio": needs_portfolio,
        "needs_market": needs_market,
        "wants_recommendations": wants_recommendations
    }
