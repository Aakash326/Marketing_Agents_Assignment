"""
Helper functions for ReportAgent to generate production-grade investment reports.
"""

from typing import Dict, Any, Optional, List, Tuple


def parse_user_question_intent(question: str) -> str:
    """
    Parse user question to determine intent (buy, hold, sell, general).

    Args:
        question: User's original question

    Returns:
        Intent category: "buy", "hold", "sell", "general"
    """
    question_lower = question.lower()

    if any(word in question_lower for word in ["buy", "invest", "purchase", "add", "acquire"]):
        return "buy"
    elif any(word in question_lower for word in ["hold", "keep", "maintain", "retain"]):
        return "hold"
    elif any(word in question_lower for word in ["sell", "exit", "close", "liquidate"]):
        return "sell"
    else:
        return "general"


def generate_direct_answer(
    user_question: str,
    recommendation: str,
    has_existing_position: bool,
    key_insight: str
) -> Dict[str, str]:
    """
    Generate direct YES/NO answer based on user question and recommendation.

    Args:
        user_question: User's original question
        recommendation: Final recommendation (BUY, SELL, HOLD, etc.)
        has_existing_position: Whether user currently owns the stock
        key_insight: Brief reason for the recommendation (1-2 sentences)

    Returns:
        Dictionary with 'answer' and 'reason' keys
    """
    intent = parse_user_question_intent(user_question)
    rec_upper = recommendation.upper()

    # Determine YES/NO based on intent and recommendation
    if intent == "buy":
        if rec_upper in ["BUY", "STRONG BUY"]:
            answer_prefix = "YES"
            answer_suffix = "Excellent opportunity to invest"
        elif rec_upper in ["SELL", "AVOID", "STRONG SELL"]:
            answer_prefix = "NO"
            answer_suffix = "Not recommended at current levels"
        elif rec_upper == "HOLD":
            if has_existing_position:
                answer_prefix = "YES"
                answer_suffix = "Continue holding, but don't add more now"
            else:
                answer_prefix = "NO"
                answer_suffix = "Wait for better entry point"
        elif "WAIT" in rec_upper or "DON'T BUY" in rec_upper:
            answer_prefix = "NO"
            answer_suffix = "Wait for better entry opportunity"
        else:
            answer_prefix = "NEUTRAL"
            answer_suffix = "Mixed signals present"

    elif intent == "hold":
        if rec_upper in ["HOLD", "BUY", "STRONG BUY", "ADD MORE"]:
            answer_prefix = "YES"
            answer_suffix = "Continue holding your position"
        elif rec_upper in ["SELL", "REDUCE POSITION", "STRONG SELL"]:
            answer_prefix = "NO"
            answer_suffix = "Consider reducing or exiting position"
        else:
            answer_prefix = "NEUTRAL"
            answer_suffix = "Reassess based on your goals"

    elif intent == "sell":
        if rec_upper in ["SELL", "STRONG SELL", "REDUCE POSITION"]:
            answer_prefix = "YES"
            answer_suffix = "Time to reduce or exit position"
        elif rec_upper in ["BUY", "HOLD", "STRONG BUY"]:
            answer_prefix = "NO"
            answer_suffix = "Maintain or add to position instead"
        else:
            answer_prefix = "NEUTRAL"
            answer_suffix = "Mixed signals on exit timing"
    else:
        # General question - just state the recommendation
        answer_prefix = rec_upper
        answer_suffix = ""

    # Format the answer
    if answer_suffix:
        answer = f"{answer_prefix} - {answer_suffix}"
    else:
        answer = answer_prefix

    return {
        "answer": answer,
        "reason": key_insight
    }


def calculate_portfolio_context(
    ticker: str,
    portfolio_data: Optional[Dict[str, Any]],
    position_size_pct: float,
    ticker_sector: str = "Unknown"
) -> Dict[str, Any]:
    """
    Calculate how this investment impacts portfolio.

    Args:
        ticker: Stock ticker symbol
        portfolio_data: Portfolio data dictionary with holdings and sector exposure
        position_size_pct: Recommended position size as percentage
        ticker_sector: Sector of the ticker

    Returns:
        Dictionary with portfolio context information
    """
    if not portfolio_data:
        # Return defaults if no portfolio data provided
        return {
            "current_position": "None - New position",
            "action_type": "NEW",
            "ticker_sector": ticker_sector,
            "current_sector_pct": 0.0,
            "new_sector_pct": position_size_pct,
            "position_dollars": 0,
            "position_pct": position_size_pct,
            "has_position": False
        }

    total_value = portfolio_data.get('total_value', 100000)
    holdings = portfolio_data.get('holdings', {})
    sector_exposure = portfolio_data.get('sector_exposure', {})

    # Check current position
    current_position = holdings.get(ticker, None)
    has_position = current_position is not None

    if has_position:
        position_text = f"{current_position['shares']} shares / ${current_position['value']:,.0f} ({current_position['pct']:.1f}%)"
        action_type = "ADD TO"
    else:
        position_text = "None - New position"
        action_type = "NEW"

    # Calculate sector exposure
    current_sector_pct = sector_exposure.get(ticker_sector, 0.0)
    new_sector_pct = current_sector_pct + position_size_pct

    # Position dollar amount
    position_dollars = total_value * (position_size_pct / 100)

    return {
        "current_position": position_text,
        "action_type": action_type,
        "ticker_sector": ticker_sector,
        "current_sector_pct": current_sector_pct,
        "new_sector_pct": new_sector_pct,
        "position_dollars": position_dollars,
        "position_pct": position_size_pct,
        "has_position": has_position
    }


def calculate_risk_reward(
    current_price: float,
    target_price: float,
    stop_loss: float,
    position_size_dollars: float
) -> Dict[str, Any]:
    """
    Calculate comprehensive risk/reward metrics.

    Args:
        current_price: Current stock price
        target_price: Target price
        stop_loss: Stop loss price
        position_size_dollars: Position size in dollars

    Returns:
        Dictionary with risk/reward analysis
    """
    # Percentage changes
    upside_pct = ((target_price - current_price) / current_price) * 100
    downside_pct = ((current_price - stop_loss) / current_price) * 100

    # Dollar amounts
    potential_gain = position_size_dollars * (upside_pct / 100)
    potential_loss = position_size_dollars * (downside_pct / 100)

    # Risk/Reward Ratio
    if downside_pct > 0:
        rr_ratio = upside_pct / downside_pct
    else:
        rr_ratio = 999.0  # Essentially infinite if no downside

    # Assessment
    if rr_ratio >= 3.0:
        assessment = "Excellent"
        emoji = "🟢"
        explanation = "Strong risk/reward favoring entry. Over 3:1 ratio indicates asymmetric upside."
    elif rr_ratio >= 2.0:
        assessment = "Good"
        emoji = "🟡"
        explanation = "Favorable risk/reward profile. 2:1+ ratio supports position entry."
    elif rr_ratio >= 1.5:
        assessment = "Fair"
        emoji = "🟠"
        explanation = "Acceptable risk/reward. Entry justified by other strong factors."
    else:
        assessment = "Poor"
        emoji = "🔴"
        explanation = "Unfavorable risk/reward. Consider waiting for better entry point."

    return {
        "ratio": rr_ratio,
        "upside_pct": upside_pct,
        "downside_pct": downside_pct,
        "potential_gain": potential_gain,
        "potential_loss": potential_loss,
        "assessment": assessment,
        "emoji": emoji,
        "explanation": explanation
    }


def generate_comparative_reasoning(
    ticker: str,
    rsi: Optional[float],
    macd_signal: Optional[str],
    pe_ratio: Optional[float],
    sector: str,
    upcoming_earnings: Optional[str] = None
) -> List[str]:
    """
    Generate comparative reasoning: Why THIS stock NOW vs alternatives.

    Args:
        ticker: Stock ticker symbol
        rsi: RSI value
        macd_signal: MACD signal (bullish, bearish, neutral)
        pe_ratio: P/E ratio
        sector: Stock sector
        upcoming_earnings: Upcoming earnings date if any

    Returns:
        List of reasoning points
    """
    points = []

    # Valuation opportunity
    if rsi is not None:
        if rsi < 30:
            points.append(f"Oversold entry point (RSI {rsi:.1f}) - stock trading below recent averages")
        elif rsi > 70:
            points.append(f"Overbought caution (RSI {rsi:.1f}) - stock may be overextended short-term")
        else:
            points.append(f"Neutral technical position (RSI {rsi:.1f}) - room for upward movement")

    # Technical timing
    if macd_signal:
        if macd_signal.lower() == "bullish":
            points.append("Bullish momentum shift confirmed by MACD crossover")
        elif macd_signal.lower() == "bearish":
            points.append("Bearish momentum developing - MACD showing weakness")

    # Fundamental catalysts
    if upcoming_earnings:
        points.append(f"Upcoming earnings catalyst ({upcoming_earnings}) creates near-term event timeline")

    # Sector context
    if sector and sector != "Unknown":
        points.append(f"{sector} sector positioning provides thematic exposure")

    # If no specific points, add generic one
    if not points:
        points.append(f"{ticker} showing unique characteristics warranting analysis at current levels")

    return points


def extract_sector_from_analysis(agent_outputs: Dict[str, Any], ticker: str) -> str:
    """
    Extract sector information from agent outputs.

    Args:
        agent_outputs: Dictionary of agent analysis outputs
        ticker: Stock ticker symbol

    Returns:
        Sector name or "Technology" as default
    """
    # Check DataAnalyst output for sector info
    data_analyst_output = agent_outputs.get('DataAnalyst', '')

    # Common sectors to look for
    sectors = [
        "Technology", "Healthcare", "Financial", "Consumer", "Energy",
        "Industrial", "Materials", "Utilities", "Real Estate", "Communication"
    ]

    for sector in sectors:
        if sector.lower() in str(data_analyst_output).lower():
            return sector

    # Default fallback - most stocks are tech or can be categorized there
    return "Technology"


def clean_debug_markers(text: str) -> str:
    """
    Remove debug artifacts from text.

    Args:
        text: Text potentially containing debug markers

    Returns:
        Cleaned text
    """
    debug_markers = [
        "FINAL_ANALYSIS_COMPLETE",
        "RISK_ANALYSIS_COMPLETE",
        "MARKET_DATA_COMPLETE",
        "QUANTITATIVE_ANALYSIS_COMPLETE",
        "STRATEGY_DEVELOPMENT_COMPLETE",
        "DATA_ANALYSIS_COMPLETE",
        "DEBUG:",
        "TODO:",
        "[PLACEHOLDER]"
    ]

    cleaned = text
    for marker in debug_markers:
        cleaned = cleaned.replace(marker, "")

    # Clean up extra whitespace
    lines = [line.rstrip() for line in cleaned.split('\n')]
    cleaned = '\n'.join(lines)

    # Remove multiple consecutive blank lines
    while '\n\n\n' in cleaned:
        cleaned = cleaned.replace('\n\n\n', '\n\n')

    return cleaned.strip()
