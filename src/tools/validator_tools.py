"""
Validator tools for checking response quality and detecting hallucinations.
"""

from typing import Dict, List


def validate_response(
    response: str,
    query: str,
    data_sources: Dict
) -> Dict:
    """
    Validate that the response is grounded in the provided data sources.

    Args:
        response: The generated response to validate
        query: The original user query
        data_sources: Dictionary containing portfolio_data and market_data

    Returns:
        Dictionary with validation results
    """
    issues = []
    is_valid = True
    confidence = 1.0

    # Basic validation checks
    if not response or len(response.strip()) < 10:
        issues.append("Response is too short or empty")
        is_valid = False
        confidence = 0.0
        return {
            "is_valid": is_valid,
            "issues": issues,
            "confidence": confidence
        }

    # Check if response contains generic/vague statements
    vague_phrases = [
        "I don't have access",
        "I cannot see",
        "I don't have information",
        "unable to provide"
    ]

    for phrase in vague_phrases:
        if phrase.lower() in response.lower():
            issues.append(f"Response contains vague statement: '{phrase}'")
            confidence -= 0.2

    # Validate portfolio data references
    portfolio_data = data_sources.get("portfolio_data", {})
    if portfolio_data and "holdings" in portfolio_data:
        holdings_count = len(portfolio_data["holdings"])

        # Check if response mentions holdings when it should
        if holdings_count > 0 and "portfolio" in query.lower():
            has_stock_mentions = any(
                holding["symbol"] in response or holding["security_name"] in response
                for holding in portfolio_data["holdings"]
            )

            if not has_stock_mentions:
                issues.append("Response doesn't reference any actual portfolio holdings")
                confidence -= 0.3

    # Validate market data references
    market_data = data_sources.get("market_data", {})
    if market_data:
        # Check if response references actual market data when discussing prices
        price_keywords = ["price", "trading", "market", "value"]
        if any(keyword in query.lower() for keyword in price_keywords):
            # Response should have some numerical data when prices are queried
            has_numbers = any(char.isdigit() for char in response)
            if not has_numbers:
                issues.append("Response lacks specific numerical data for price query")
                confidence -= 0.2

    # Check for contradictions in response
    contradiction_pairs = [
        ("increase", "decrease"),
        ("gain", "loss"),
        ("up", "down"),
        ("positive", "negative")
    ]

    for word1, word2 in contradiction_pairs:
        if word1 in response.lower() and word2 in response.lower():
            # This might indicate a contradiction (needs more sophisticated checking)
            # For now, just flag as a warning
            issues.append(f"Response contains potentially contradictory terms: '{word1}' and '{word2}'")
            confidence -= 0.1

    # Final validation decision
    if confidence < 0.5:
        is_valid = False

    # Ensure confidence is between 0 and 1
    confidence = max(0.0, min(1.0, confidence))

    return {
        "is_valid": is_valid,
        "issues": issues,
        "confidence": confidence
    }


def check_data_coverage(
    query: str,
    portfolio_data: Dict,
    market_data: Dict
) -> Dict:
    """
    Check if we have sufficient data to answer the query.

    Args:
        query: User's question
        portfolio_data: Portfolio information
        market_data: Market information

    Returns:
        Dictionary with coverage analysis
    """
    coverage = {
        "has_portfolio_data": False,
        "has_market_data": False,
        "sufficient_data": False,
        "missing_data": []
    }

    # Check portfolio data
    if portfolio_data and "holdings" in portfolio_data:
        if portfolio_data["holdings"]:
            coverage["has_portfolio_data"] = True
        else:
            coverage["missing_data"].append("No holdings found in portfolio")
    else:
        coverage["missing_data"].append("Portfolio data not loaded")

    # Check market data
    if market_data and len(market_data) > 0:
        coverage["has_market_data"] = True
    else:
        if "price" in query.lower() or "market" in query.lower():
            coverage["missing_data"].append("Market data not available")

    # Determine if we have sufficient data
    query_lower = query.lower()

    # Portfolio-only queries
    if any(keyword in query_lower for keyword in ["own", "holdings", "stocks do i have"]):
        coverage["sufficient_data"] = coverage["has_portfolio_data"]

    # Market-only queries
    elif "price of" in query_lower or "how is" in query_lower:
        coverage["sufficient_data"] = coverage["has_market_data"]

    # Combined queries
    elif any(keyword in query_lower for keyword in ["in my portfolio", "my holdings"]):
        coverage["sufficient_data"] = (
            coverage["has_portfolio_data"] and coverage["has_market_data"]
        )

    # Default: require at least one data source
    else:
        coverage["sufficient_data"] = (
            coverage["has_portfolio_data"] or coverage["has_market_data"]
        )

    return coverage
