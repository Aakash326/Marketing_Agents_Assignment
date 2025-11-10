"""
Validator tools for checking response quality and detecting hallucinations.
Enhanced with ambiguity detection and improved fact-checking (Feature 5).
"""

from typing import Dict, List, Tuple
import re


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


def detect_ambiguity(query: str, conversation_history: List[Dict] = None) -> Tuple[bool, str]:
    """
    Detect if a query is ambiguous and needs clarification (Feature 5).

    Args:
        query: User's question
        conversation_history: Optional conversation history for context

    Returns:
        Tuple of (is_ambiguous, clarification_message)
    """
    query_lower = query.lower().strip()

    # Check for vague pronouns without clear antecedents
    vague_pronouns = ["it", "that stock", "that one", "this one", "the stock", "them", "those"]
    for pronoun in vague_pronouns:
        if pronoun in query_lower:
            # Check if there's context from history
            if not conversation_history or len(conversation_history) == 0:
                return (True, f"Which specific stock are you referring to when you say '{pronoun}'?")

    # Check for relative terms without context
    relative_terms = {
        "best": ("Best by what metric? (highest return, highest value, lowest risk?)", ["return", "value", "gain", "loss", "price", "performance", "profit"]),
        "worst": ("Worst by what metric? (lowest return, highest loss, highest volatility?)", ["return", "value", "gain", "loss", "price", "performance"]),
        "top": ("Top by what criterion? (return, value, gain?)", ["return", "value", "gain", "performer", "holding"]),
        "most": ("Most in what sense? (shares, value, percentage?)", ["shares", "value", "percentage", "allocation", "weight"]),
        "first": ("First in what order? (alphabetically, by value, by return?)", ["alphabetically", "value", "return", "largest", "biggest"])
    }

    for term, (clarification, context_words) in relative_terms.items():
        if term in query_lower and len(query_lower) < 80:  # Short queries more likely to be ambiguous
            # Check if there's specific context - the query should have one of the context words
            has_context = any(word in query_lower for word in context_words)
            if not has_context:
                return (True, clarification)

    # Check for vague time references
    time_references = {
        "recent": "How recent? (past week, month, quarter?)",
        "lately": "What time period do you mean? (past week, month?)",
        "previously": "When specifically? (last week, last month?)"
    }

    for ref, clarification in time_references.items():
        if ref in query_lower:
            # Check if there's a specific timeframe mentioned
            has_timeframe = any(word in query_lower for word in ["week", "month", "year", "day", "quarter"])
            if not has_timeframe:
                return (True, clarification)

    # Check for incomplete comparisons
    if "compared to" in query_lower or "versus" in query_lower or "vs" in query_lower:
        # Should have two things being compared
        words = query_lower.split()
        if len(words) < 5:  # Too short to have full comparison
            return (True, "What are you comparing? Please specify both items.")

    # Query seems clear
    return (False, "")


def enhanced_fact_check(
    response: str,
    portfolio_data: Dict,
    market_data: Dict
) -> Dict:
    """
    Enhanced fact-checking for hallucination detection (Feature 5).

    Args:
        response: Generated response
        portfolio_data: Portfolio information
        market_data: Market data

    Returns:
        Dictionary with fact-check results
    """
    issues = []
    hallucinations = []

    # Extract all stock tickers mentioned in response (3-5 letter uppercase words)
    ticker_pattern = r'\b[A-Z]{2,5}\b'
    mentioned_tickers = set(re.findall(ticker_pattern, response))

    # Get actual tickers from data
    portfolio_tickers = set()
    if portfolio_data and "holdings" in portfolio_data:
        portfolio_tickers = {h["symbol"] for h in portfolio_data["holdings"]}

    market_tickers = set()
    if market_data:
        market_tickers = set(market_data.keys())

    # Check for tickers mentioned that aren't in any data source
    known_tickers = portfolio_tickers | market_tickers
    # Filter common English words that match ticker pattern (comprehensive list)
    common_words = {
        # Common 2-letter words
        "AM", "AN", "AS", "AT", "BE", "BY", "DO", "GO", "HE", "IF", "IN", "IS", "IT",
        "ME", "MY", "NO", "OF", "ON", "OR", "SO", "TO", "UP", "US", "WE", "YA",
        # Common 3-letter words
        "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HAD", "HER",
        "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM", "HIS", "HOW", "ITS",
        "MAY", "NEW", "NOW", "OLD", "SEE", "TWO", "WAY", "WHO", "BOY", "DID", "CAR",
        "EAT", "FAR", "FUN", "GOT", "HOT", "LET", "MAN", "OWN", "RAN", "SAT", "SAY",
        "SHE", "TOP", "TRY", "USE", "WIN", "YES", "YET", "BIG", "WHY", "CUT", "OFF",
        "PUT", "RUN", "SET", "SIT", "TEN", "BAD", "BAG", "BED", "BOX", "END", "FEW",
        "LAW", "LAY", "LEG", "LET", "LIE", "LOT", "LOW", "MAP", "MET", "MIX", "NOR",
        "ODD", "OIL", "PAY", "PER", "PIT", "POT", "RED", "ROW", "SIX", "SKY", "SUM",
        "TAX", "TEA", "TIP", "TON", "TOO", "TOY", "VAN", "WAR", "WET", "WIN", "WON",
        # Common 4-letter words  
        "THAT", "WITH", "HAVE", "THIS", "WILL", "YOUR", "FROM", "THEY", "BEEN", "WERE",
        "WHAT", "WOULD", "THERE", "THEIR", "WHICH", "THAN", "THEM", "BEST", "EACH",
        "FIND", "GIVE", "JUST", "KNOW", "MADE", "MAKE", "MANY", "MORE", "MOST", "MUCH",
        "ONLY", "OVER", "SAID", "SAME", "SOME", "SUCH", "TAKE", "TELL", "THAN", "THEN",
        "VERY", "WANT", "WELL", "WENT", "WHEN", "DOES", "COME", "GOOD", "HELP", "HERE",
        "INTO", "LAST", "LIFE", "LIKE", "LONG", "LOOK", "NEED", "NEXT", "OPEN", "PART",
        "SEEM", "SHOW", "SIDE", "SURE", "TALK", "TURN", "USED", "WORK", "YEAR", "ALSO",
        "BACK", "BOTH", "CALL", "CAME", "CASE", "DONE", "DOWN", "EVEN", "FACT", "FEEL",
        "FOUR", "FREE", "FULL", "GAVE", "GETS", "GOES", "GONE", "HALF", "HAND", "HEAD",
        "HIGH", "HOME", "KEEP", "KIND", "KNEW", "KNOW", "LATE", "LEAD", "LEFT", "LESS",
        "LINE", "LIST", "LIVE", "LONG", "LOSE", "LOST", "MAIN", "MEAN", "MEET", "MIND",
        "MOVE", "MUST", "NAME", "NEAR", "ONCE", "PASS", "PAST", "PLAY", "PULL", "PUSH",
        "READ", "REAL", "REST", "RISE", "ROOM", "SAVE", "SEEN", "SELF", "SELL", "SENT",
        "SOON", "STAY", "STEP", "STOP", "TEAM", "TEND", "TEST", "TEXT", "THUS", "TOLD",
        "TOOK", "TOWN", "TREE", "TRUE", "UPON", "VIEW", "WAIT", "WALK", "WEEK", "WIDE",
        "WISH", "WITH", "WORD", "WORE", "YARD",
        # Common 5-letter words
        "ABOUT", "AFTER", "AGAIN", "BEING", "BELOW", "COULD", "DOING", "EVERY", "FIRST",
        "FOUND", "GOING", "GREAT", "GROUP", "LARGE", "LATER", "LEAVE", "MIGHT", "NEVER",
        "OTHER", "PLACE", "RIGHT", "SHALL", "SINCE", "SMALL", "STILL", "THEIR", "THERE",
        "THESE", "THING", "THINK", "THOSE", "THREE", "TIMES", "TODAY", "UNDER", "UNTIL",
        "USING", "WANTS", "WHERE", "WHICH", "WHILE", "WHOSE", "WOMAN", "WORLD", "WOULD",
        "WRITE", "YEARS", "YOUNG",
        # Financial terms that aren't tickers
        "ETF", "ETFS", "FUND", "FUNDS", "STOCK", "STOCKS", "BOND", "BONDS", "PRICE",
        "PRICES", "SHARE", "SHARES", "ASSET", "ASSETS", "MARKET", "CASH", "OWNS", "HOLDINGS",
        "RETURN", "RETURNS", "GAIN", "GAINS", "LOSS", "LOSSES", "VALUE", "VALUES",
        "TOTAL", "HOLD", "HOLDING", "WORTH", "PORTFOLIO", "PORTFOLIOS",
        "RISK", "RISKS", "PROFILE", "DIVERSITY", "DIVERSIFIED", "ALLOCATION",
        "CLT", "CLASS", "BUY", "SELL", "TRADE", "SHOULD", "WOULD", "COULD"
    }
    unknown_tickers = mentioned_tickers - known_tickers - common_words

    if unknown_tickers:
        hallucinations.append(f"Mentions tickers not in available data: {', '.join(unknown_tickers)}")

    # Extract all numerical values from response (prices, percentages, etc.)
    number_pattern = r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)\%?'
    numbers_in_response = re.findall(number_pattern, response)

    # Verify price reasonableness for mentioned stocks
    for ticker in mentioned_tickers & known_tickers:
        if market_data and ticker in market_data:
            actual_price = market_data[ticker].get('current_price', 0)
            
            # Skip if actual_price is None or not a valid number
            if actual_price is None:
                continue

            # Check if response mentions a price for this ticker
            # Look for patterns like "$150" or "150.50" near the ticker
            ticker_context = response[max(0, response.find(ticker)-50):response.find(ticker)+50]
            price_in_context = re.findall(r'\$?(\d+(?:\.\d{2})?)', ticker_context)

            if price_in_context and actual_price > 0:
                for price_str in price_in_context:
                    price = float(price_str.replace(',', ''))
                    # Check if mentioned price is wildly different from actual (>50% off)
                    if abs(price - actual_price) / actual_price > 0.5 and price > 1:
                        issues.append(f"Price for {ticker} seems incorrect: mentioned ${price}, actual ${actual_price:.2f}")

    # Check for contradictory percentage changes
    percentage_pattern = r'([+-]?\d+(?:\.\d+)?)\%'
    percentages = re.findall(percentage_pattern, response)

    if len(percentages) > 1:
        # Check if there are contradictory signs
        has_positive = any(float(p) > 0 for p in percentages)
        has_negative = any(float(p) < 0 for p in percentages)

        if has_positive and has_negative:
            # This might be OK (e.g., different stocks), but flag as potential issue
            issues.append("Response contains both positive and negative percentage changes - verify this is correct")

    return {
        "hallucinations": hallucinations,
        "issues": issues,
        "has_hallucinations": len(hallucinations) > 0,
        "fact_check_passed": len(hallucinations) == 0
    }


def check_data_sufficiency(
    query: str,
    portfolio_data: Dict,
    market_data: Dict
) -> Tuple[bool, str]:
    """
    Check if we have sufficient data to answer the query (Feature 5).

    Args:
        query: User's question
        portfolio_data: Portfolio information
        market_data: Market data

    Returns:
        Tuple of (is_sufficient, help_message)
    """
    query_lower = query.lower()

    # Check if query asks about specific ticker
    ticker_pattern = r'\b[A-Z]{2,5}\b'
    mentioned_tickers = set(re.findall(ticker_pattern, query.upper()))

    # Filter common English words that match ticker pattern (comprehensive list)
    common_words = {
        # Common 2-letter words
        "AM", "AN", "AS", "AT", "BE", "BY", "DO", "GO", "HE", "IF", "IN", "IS", "IT",
        "ME", "MY", "NO", "OF", "ON", "OR", "SO", "TO", "UP", "US", "WE", "YA",
        # Common 3-letter words
        "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HAD", "HER",
        "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM", "HIS", "HOW", "ITS",
        "MAY", "NEW", "NOW", "OLD", "SEE", "TWO", "WAY", "WHO", "BOY", "DID", "CAR",
        "EAT", "FAR", "FUN", "GOT", "HOT", "LET", "MAN", "OWN", "RAN", "SAT", "SAY",
        "SHE", "TOP", "TRY", "USE", "WIN", "YES", "YET", "BIG", "WHY", "CUT", "OFF",
        "PUT", "RUN", "SET", "SIT", "TEN", "BAD", "BAG", "BED", "BOX", "END", "FEW",
        "LAW", "LAY", "LEG", "LET", "LIE", "LOT", "LOW", "MAP", "MET", "MIX", "NOR",
        "ODD", "OIL", "PAY", "PER", "PIT", "POT", "RED", "ROW", "SIX", "SKY", "SUM",
        "TAX", "TEA", "TIP", "TON", "TOO", "TOY", "VAN", "WAR", "WET", "WIN", "WON",
        # Common 4-letter words  
        "THAT", "WITH", "HAVE", "THIS", "WILL", "YOUR", "FROM", "THEY", "BEEN", "WERE",
        "WHAT", "WOULD", "THERE", "THEIR", "WHICH", "THAN", "THEM", "BEST", "EACH",
        "FIND", "GIVE", "JUST", "KNOW", "MADE", "MAKE", "MANY", "MORE", "MOST", "MUCH",
        "ONLY", "OVER", "SAID", "SAME", "SOME", "SUCH", "TAKE", "TELL", "THAN", "THEN",
        "VERY", "WANT", "WELL", "WENT", "WHEN", "DOES", "COME", "GOOD", "HELP", "HERE",
        "INTO", "LAST", "LIFE", "LIKE", "LONG", "LOOK", "NEED", "NEXT", "OPEN", "PART",
        "SEEM", "SHOW", "SIDE", "SURE", "TALK", "TURN", "USED", "WORK", "YEAR", "ALSO",
        "BACK", "BOTH", "CALL", "CAME", "CASE", "DONE", "DOWN", "EVEN", "FACT", "FEEL",
        "FOUR", "FREE", "FULL", "GAVE", "GETS", "GOES", "GONE", "HALF", "HAND", "HEAD",
        "HIGH", "HOME", "KEEP", "KIND", "KNEW", "KNOW", "LATE", "LEAD", "LEFT", "LESS",
        "LINE", "LIST", "LIVE", "LONG", "LOSE", "LOST", "MAIN", "MEAN", "MEET", "MIND",
        "MOVE", "MUST", "NAME", "NEAR", "ONCE", "PASS", "PAST", "PLAY", "PULL", "PUSH",
        "READ", "REAL", "REST", "RISE", "ROOM", "SAVE", "SEEN", "SELF", "SELL", "SENT",
        "SOON", "STAY", "STEP", "STOP", "TEAM", "TEND", "TEST", "TEXT", "THUS", "TOLD",
        "TOOK", "TOWN", "TREE", "TRUE", "UPON", "VIEW", "WAIT", "WALK", "WEEK", "WIDE",
        "WISH", "WITH", "WORD", "WORE", "YARD",
        # Common 5-letter words
        "ABOUT", "AFTER", "AGAIN", "BEING", "BELOW", "COULD", "DOING", "EVERY", "FIRST",
        "FOUND", "GOING", "GREAT", "GROUP", "LARGE", "LATER", "LEAVE", "MIGHT", "NEVER",
        "OTHER", "PLACE", "RIGHT", "SHALL", "SINCE", "SMALL", "STILL", "THEIR", "THERE",
        "THESE", "THING", "THINK", "THOSE", "THREE", "TIMES", "TODAY", "UNDER", "UNTIL",
        "USING", "WANTS", "WHERE", "WHICH", "WHILE", "WHOSE", "WOMAN", "WORLD", "WOULD",
        "WRITE", "YEARS", "YOUNG",
        # Financial terms that aren't tickers
        "ETF", "ETFS", "FUND", "FUNDS", "STOCK", "STOCKS", "BOND", "BONDS", "PRICE",
        "PRICES", "SHARE", "SHARES", "ASSET", "ASSETS", "MARKET", "CASH", "OWNS", "HOLDINGS",
        "RETURN", "RETURNS", "GAIN", "GAINS", "LOSS", "LOSSES", "VALUE", "VALUES",
        "TOTAL", "HOLD", "HOLDING", "WORTH", "PORTFOLIO", "PORTFOLIOS",
        "RISK", "RISKS", "PROFILE", "DIVERSITY", "DIVERSIFIED", "ALLOCATION",
        "CLT", "CLASS", "BUY", "SELL", "TRADE", "SHOULD", "WOULD", "COULD"
    }

    # Filter out common words first
    mentioned_tickers = mentioned_tickers - common_words

    if mentioned_tickers:
        # Check if we have data for this ticker
        portfolio_tickers = set()
        if portfolio_data and "holdings" in portfolio_data:
            portfolio_tickers = {h["symbol"] for h in portfolio_data["holdings"]}

        market_tickers = set()
        if market_data:
            market_tickers = set(market_data.keys())

        known_tickers = portfolio_tickers | market_tickers

        for ticker in mentioned_tickers:
            if ticker not in known_tickers:
                if "portfolio" in query_lower or "my" in query_lower:
                    return (False, f"Your portfolio doesn't contain {ticker}. Did you mean a different stock?")
                else:
                    return (False, f"I don't have market data for {ticker}. Would you like me to search for it?")

    # Check for portfolio queries without portfolio data
    portfolio_keywords = ["my stocks", "my holdings", "my portfolio", "what do i own"]
    if any(kw in query_lower for kw in portfolio_keywords):
        if not portfolio_data or "holdings" not in portfolio_data or not portfolio_data["holdings"]:
            return (False, "I don't have your portfolio data loaded. Please check the client ID.")

    # Check for price queries without market data
    if "price" in query_lower or "trading" in query_lower:
        if not market_data or len(market_data) == 0:
            return (False, "I don't have current market data. There may be a connectivity issue with market data sources.")

    return (True, "")
