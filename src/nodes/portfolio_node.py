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
    conversation_history = state.get("conversation_history", [])
    
    # Build context from conversation history for better understanding
    history_context = ""
    if conversation_history and len(conversation_history) > 0:
        history_context = "\n\nRecent Conversation Context:\n"
        for msg in conversation_history[-4:]:
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")[:200]
            history_context += f"{role}: {content}\n"
        history_context += "\nNote: If the current query is very short (e.g., 'yes', 'tell me more'), use the above context to understand what the user is asking about.\n"

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
{history_context}

{portfolio_text}

CRITICAL INSTRUCTIONS - RISK PROFILE ANALYSIS:
You MUST analyze the risk profile and diversification of this portfolio. DO NOT just report the total value.

FORMAT YOUR RESPONSE WITH CLEAN MARKDOWN:
- Use ## for main sections
- Use **bold** for key metrics
- Use bullet points with - for lists
- Keep paragraphs short and readable
- Add blank lines between sections

Perform the following analysis:

## Asset Class Distribution
- Count how many holdings are in each asset class (Stocks, Bonds, ETFs, etc.)
- Calculate percentage of portfolio in each asset class
- Present as: **60% Stocks**, **30% Bonds**, **10% ETFs**

## Sector Allocation
- List all sectors represented
- Count holdings per sector
- Identify dominant sectors
- Present as: **40% Technology**, **25% Healthcare**, etc.

## Concentration Risk
- Are holdings too concentrated in one sector or asset class?
- Is there over-reliance on a few positions?
- Are holdings well-spread across different sectors?

## Risk Assessment
- **Overall Risk Level**: Low / Moderate / High
- **Diversification Quality**: Well-diversified / Moderately diversified / Concentrated
- **Key Risks**: List specific risks identified

Provide a comprehensive risk profile analysis with clean, readable markdown formatting.

Your response:"""
        else:
            # GENERAL INFORMATION MODE
            # Check if asking about performance/returns
            is_performance_query = any(keyword in query_lower for keyword in
                                      ["best return", "worst return", "best performer", "worst performer",
                                       "highest return", "lowest return", "top performer", "bottom performer",
                                       "year-to-date", "ytd", "performance", "gain", "loss"])

            # Check if asking about what stocks they own
            is_holdings_query = any(keyword in query_lower for keyword in
                                   ["what stocks", "what do i own", "my holdings", "what do i have",
                                    "show my stocks", "list my stocks", "my stocks"])

            if is_performance_query:
                analysis_prompt = f"""You are a portfolio performance analysis agent.

USER'S QUESTION: "{query}"
{history_context}

{portfolio_text}

CRITICAL INSTRUCTIONS:
- The user is asking about PERFORMANCE/RETURNS of their holdings
- Words like "DATE", "YEAR", "RETURN", "GAIN", "LOSS" are ENGLISH WORDS, NOT stock ticker symbols
- You MUST analyze the actual holdings data provided above
- Look at each holding's cost basis vs current price to calculate returns
- DO NOT search for ticker symbols like "DATE", "YEAR", "TO", "RETURN"

ANALYZE THE PORTFOLIO DATA:
1. For each holding, calculate the return: ((Current Price - Cost Basis) / Cost Basis) * 100
2. Identify which holdings have the best/worst returns
3. Present the results with clear formatting

FORMAT YOUR RESPONSE:
## Performance Analysis

**Best Performers:**
- **[Ticker]**: +XX.X% return ($XXX,XXX gain)
- **[Ticker]**: +XX.X% return ($XXX,XXX gain)

**Worst Performers:**
- **[Ticker]**: -XX.X% return ($XXX,XXX loss)

**Summary:** Brief analysis of overall portfolio performance

Your response:"""
            elif is_holdings_query:
                analysis_prompt = f"""You are a portfolio analysis agent.

USER'S QUESTION: "{query}"
{history_context}

{portfolio_text}

CRITICAL: The user is asking what stocks/holdings they own. You MUST list all their holdings.

FORMAT YOUR RESPONSE LIKE THIS:

You own the following holdings:

**1. [Ticker Symbol] - [Full Name]**
- Shares: [X,XXX]
- Current Price: $XX.XX
- Market Value: $XXX,XXX.XX

**2. [Ticker Symbol] - [Full Name]**
- Shares: [X,XXX]
- Current Price: $XX.XX
- Market Value: $XXX,XXX.XX

(Continue for all holdings...)

**Total Portfolio Value**: $X,XXX,XXX.XX

Do NOT just report the total value. List ALL holdings with their details.

Your response:"""
            else:
                analysis_prompt = f"""You are a portfolio analysis agent.

USER'S QUESTION: "{query}"
{history_context}

IMPORTANT CONTEXT UNDERSTANDING:
- If the user asks about "total value", "portfolio value", "total worth" - they are asking for the SUM of all holding values
- Words like "TOTAL", "VALUE", "HOLD", "OWN", "DO", "DATE", "YEAR", "TO", "RETURN" in questions are ENGLISH WORDS, NOT stock ticker symbols
- The portfolio data below ALREADY includes "Total Portfolio Value" calculated for you
- Simply read and report the total value from the data provided
- If asking about performance, analyze the holdings' cost basis vs current price

{portfolio_text}

INSTRUCTIONS:
1. The data above already shows "Total Portfolio Value" - use that number
2. If they ask about "total value" or similar - report the "Total Portfolio Value" shown above
3. Do NOT search for ticker symbols like "TOTAL", "VALUE", "HOLD", "OWN", "DATE", "YEAR" - these are English words
4. Analyze the actual portfolio data provided above
5. Be factual and direct
6. Use clean markdown formatting with ## headers and **bold** for emphasis

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
{history_context}

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
