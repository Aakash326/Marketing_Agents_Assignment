"""
Validator agent node for checking response quality and accuracy.
"""

from typing import Dict
from src.tools.validator_tools import validate_response, check_data_coverage


def validator_node(state: Dict) -> Dict:
    """
    Validate the generated response for accuracy and data grounding.

    Args:
        state: Current graph state

    Returns:
        Updated state with validation results
    """
    query = state.get("query", "")
    response = state.get("response", "")
    portfolio_data = state.get("portfolio_data", {})
    market_data = state.get("market_data", {})

    # Prepare data sources for validation
    data_sources = {
        "portfolio_data": portfolio_data,
        "market_data": market_data
    }

    # Validate the response
    validation_result = validate_response(response, query, data_sources)

    # Check data coverage
    coverage = check_data_coverage(query, portfolio_data, market_data)

    # Determine if response is acceptable
    is_valid = validation_result["is_valid"]
    confidence = validation_result["confidence"]
    issues = validation_result["issues"]

    # If validation fails, enhance the response with a disclaimer
    if not is_valid or confidence < 0.7:
        # Add a note about limitations
        enhanced_response = response + "\n\n---\n"
        enhanced_response += "Note: This response may have limitations. "
        if issues:
            enhanced_response += f"Issues detected: {', '.join(issues[:2])}"
        if not coverage["sufficient_data"]:
            enhanced_response += f" Missing data: {', '.join(coverage['missing_data'])}"

        return {
            **state,
            "response": enhanced_response,
            "validated": True
        }

    # If validation passes, return state as-is
    return {
        **state,
        "validated": True
    }
