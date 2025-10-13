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
    wants_recommendations = state.get("wants_recommendations", False)

    # Load portfolio data
    portfolio_data = load_portfolio_data("portfolios.xlsx", client_id)

    # Format portfolio for LLM
    portfolio_text = format_portfolio_for_llm(portfolio_data)

    # Create analysis prompt based on whether user wants recommendations
    if not wants_recommendations:
        # INFORMATION MODE: Just answer the question factually
        analysis_prompt = f"""You are a portfolio analysis agent providing factual information.

# RESPONSE GUIDELINES:
# - Answer queries factually with NO recommendations
# - "What do I own?" → List holdings only
# - "How's it performing?" → Show numbers only
# - "What's my allocation?" → Show breakdown only
# - DO NOT suggest what to buy or sell
# - DO NOT give investment recommendations
# - Just answer what they asked

Client ID: {client_id}
User Query: "{query}"

Portfolio Data:
{portfolio_text}

Provide a clear, factual answer to the user's query:
- List what they own if asked
- Show performance numbers if asked
- Describe their current allocation if asked
- Be specific and reference actual holdings
- DO NOT suggest what they should buy or sell
- DO NOT give investment recommendations
- Just answer the question directly

Response:"""
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
