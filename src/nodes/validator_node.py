"""
Validator agent node for checking response quality and accuracy.
Enhanced with ambiguity detection and clarification requests (Feature 5).
"""

from typing import Dict
from src.tools.validator_tools import (
    validate_response,
    check_data_coverage,
    detect_ambiguity,
    enhanced_fact_check,
    check_data_sufficiency
)


def validator_node(state: Dict) -> Dict:
    """
    Validate the generated response for accuracy and data grounding.
    Enhanced with ambiguity detection and clarification requests (Feature 5).

    Args:
        state: Current graph state

    Returns:
        Updated state with validation results
    """
    query = state.get("query", "")
    response = state.get("response", "")
    portfolio_data = state.get("portfolio_data", {})
    market_data = state.get("market_data", {})
    conversation_history = state.get("conversation_history", [])

    # FEATURE 5: Enhanced Validation with Clarification Requests

    # Step 1: Check for ambiguous queries FIRST (before even validating response)
    is_ambiguous, clarification_msg = detect_ambiguity(query, conversation_history)

    if is_ambiguous:
        # Query is ambiguous - request clarification from user
        return {
            **state,
            "needs_clarification": True,
            "clarification_message": clarification_msg,
            "validated": False
        }

    # Step 2: Check data sufficiency
    has_sufficient_data, insufficiency_msg = check_data_sufficiency(query, portfolio_data, market_data)

    if not has_sufficient_data:
        # Not enough data to answer - inform user
        return {
            **state,
            "response": insufficiency_msg,
            "validated": True,
            "needs_clarification": False
        }

    # Step 3: Enhanced fact-checking for hallucinations
    fact_check = enhanced_fact_check(response, portfolio_data, market_data)

    if fact_check["has_hallucinations"]:
        # Detected hallucinations - add warning to response
        enhanced_response = response + "\n\n---\n"
        enhanced_response += "⚠️ Warning: Response validation detected potential issues:\n"
        for hallucination in fact_check["hallucinations"]:
            enhanced_response += f"- {hallucination}\n"

        return {
            **state,
            "response": enhanced_response,
            "validated": True,
            "needs_clarification": False
        }

    # Step 4: Original validation checks
    data_sources = {
        "portfolio_data": portfolio_data,
        "market_data": market_data
    }

    validation_result = validate_response(response, query, data_sources)
    coverage = check_data_coverage(query, portfolio_data, market_data)

    is_valid = validation_result["is_valid"]
    confidence = validation_result["confidence"]
    issues = validation_result["issues"]

    # If validation fails, enhance the response with a disclaimer
    if not is_valid or confidence < 0.7:
        enhanced_response = response + "\n\n---\n"
        enhanced_response += "Note: This response may have limitations. "
        if issues:
            enhanced_response += f"Issues detected: {', '.join(issues[:2])}"
        if not coverage["sufficient_data"]:
            enhanced_response += f" Missing data: {', '.join(coverage['missing_data'])}"

        return {
            **state,
            "response": enhanced_response,
            "validated": True,
            "needs_clarification": False
        }

    # If validation passes, return state as-is
    return {
        **state,
        "validated": True,
        "needs_clarification": False
    }
