# Recommendation Fix Summary

## Problem Solved
The agents were giving too many unsolicited investment recommendations instead of just answering questions. They acted like financial advisors rather than analytical assistants.

## Solution
Added a `wants_recommendations` flag to distinguish between:
- **Information queries** → Factual answers only, NO recommendations
- **Advice queries** → Educational considerations with disclaimers

---

## Changes Made

### 1. Updated State Schema ([src/state/graph_state.py](src/state/graph_state.py))
Added new field:
```python
wants_recommendations: bool  # True only if user explicitly asks for advice
```

### 2. Updated Planner Agent ([src/nodes/planner_node.py](src/nodes/planner_node.py))
- Detects if user wants advice by looking for keywords like:
  - "how to improve", "what should I do", "recommendations"
  - "suggestions", "advice", "should I buy", "should I sell"
- Sets `wants_recommendations = True` only when these are detected
- **Default is False** (most queries are information-seeking)

### 3. Updated Portfolio Agent ([src/nodes/portfolio_node.py](src/nodes/portfolio_node.py))
Two modes:

**Information Mode** (`wants_recommendations = False`):
- Lists holdings, shows performance, describes allocation
- NO investment recommendations
- NO suggestions about what to buy/sell
- Just answers what was asked

**Advisory Mode** (`wants_recommendations = True`):
- Provides educational considerations
- Uses gentle language: "you might consider" NOT "you should"
- Presents options and trade-offs
- Ends with disclaimer

### 4. Updated Market Agent ([src/nodes/market_node.py](src/nodes/market_node.py))
Same two-mode approach:

**Information Mode**:
- Reports prices, performance, news factually
- NO suggestions about buying/selling

**Advisory Mode**:
- Provides market context for decision-making
- Gentle suggestions, not commands
- Includes disclaimer

### 5. Updated Workflow ([src/graph/workflow.py](src/graph/workflow.py))
Initialized `wants_recommendations: False` in initial state

---

## Testing

### Test Information Queries
Run these to verify NO recommendations are given:
```bash
python test_recommendation_fix.py
```

Or test manually in Streamlit:
- "What stocks do I own?" → Should list holdings only
- "What's my allocation?" → Should show breakdown only
- "How is my portfolio performing?" → Should show numbers only

### Test Advice Queries
These SHOULD give recommendations with disclaimers:
- "How can I improve my portfolio?"
- "What should I do to diversify?"
- "Give me investment recommendations"

Expected: Gentle suggestions + disclaimer

---

## Key Behavioral Changes

### Before Fix
**User**: "What stocks do I own?"
**System**: "You own AAPL, MSFT, TSLA. I recommend selling TSLA and buying more bonds for diversification..."

❌ **Problem**: Unsolicited recommendations

### After Fix
**User**: "What stocks do I own?"
**System**: "You currently own the following holdings:
1. Vanguard Total Stock Market ETF (VTI) - 82.5 shares
2. Vanguard Total Bond Market ETF (BND) - 121.4 shares
3. Vanguard Total International Stock ETF (VXUS) - 158.8 shares
..."

✅ **Result**: Just answers the question

### With Advice Request
**User**: "How can I improve my portfolio?"
**System**: "Based on your current allocation, you might consider a few factors:
- Your portfolio is well-diversified across major asset classes
- One approach could be to review your risk tolerance...
- You might consider examining the ratio between stocks and bonds...

Note: This is educational analysis, not financial advice. Please consult a licensed financial advisor for personalized investment recommendations."

✅ **Result**: Helpful considerations + disclaimer

---

## Disclaimer Template

When `wants_recommendations = True`, responses end with:

> "Note: This is educational analysis, not financial advice. Please consult a licensed financial advisor for personalized investment recommendations."

---

## Language Guidelines

### ✅ DO Use (Information Mode)
- "You currently own..."
- "Your portfolio consists of..."
- "The current price is..."
- "Performance shows..."

### ❌ DON'T Use (Information Mode)
- "You should buy..."
- "I recommend selling..."
- "You need to..."
- "You must diversify..."

### ✅ DO Use (Advisory Mode)
- "You might consider..."
- "One approach could be..."
- "Factors to consider include..."
- "Market conditions suggest..."

### ❌ DON'T Use (Advisory Mode)
- "You must buy..."
- "You should definitely sell..."
- "The only option is..."
- Commands without alternatives

---

## Files Modified

1. [src/state/graph_state.py](src/state/graph_state.py) - Added field
2. [src/nodes/planner_node.py](src/nodes/planner_node.py) - Detection logic
3. [src/nodes/portfolio_node.py](src/nodes/portfolio_node.py) - Conditional prompts
4. [src/nodes/market_node.py](src/nodes/market_node.py) - Conditional prompts
5. [src/graph/workflow.py](src/graph/workflow.py) - Initialize field

## Test Files Created

1. [test_recommendation_fix.py](test_recommendation_fix.py) - Automated test suite

---

## Success Criteria

✅ Information queries return facts only (no recommendations)
✅ Advice queries return considerations (not commands) with disclaimers
✅ System still works as before, just less pushy
✅ No complex additions to the codebase (simple flag + prompt changes)

---

## Running the System

After these changes, run:
```bash
streamlit run app.py
```

The system will now be much less aggressive with recommendations!
