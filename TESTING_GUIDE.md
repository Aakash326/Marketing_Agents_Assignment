# Testing Guide - Recommendation Fix

## Quick Test Commands

### Option 1: Run Automated Tests
```bash
python test_recommendation_fix.py
```

This will test both information queries (should NOT give recommendations) and advice queries (should give recommendations with disclaimers).

### Option 2: Manual Testing with Streamlit
```bash
streamlit run app.py
```

Then select a client (e.g., CLT-001) and try the queries below.

---

## Test Cases

### ✅ Information Queries (Should NOT give recommendations)

| Query | Expected Behavior |
|-------|-------------------|
| "What stocks do I own?" | Lists holdings only. NO buy/sell suggestions. |
| "What's my portfolio allocation?" | Shows asset breakdown only. NO recommendations. |
| "How is my portfolio performing?" | Shows performance numbers only. NO advice. |
| "What's the current price of NVDA?" | Reports price and performance. NO trading suggestions. |

**Success Criteria**:
- Response answers the question directly
- NO phrases like "you should buy", "I recommend selling", "you need to"
- Just factual information

---

### ✅ Advice Queries (SHOULD give recommendations with disclaimers)

| Query | Expected Behavior |
|-------|-------------------|
| "How can I improve my portfolio?" | Provides considerations + disclaimer. Gentle language. |
| "What should I do to diversify?" | Educational suggestions + disclaimer. Not commands. |
| "Give me investment recommendations" | Options and factors + disclaimer. Balanced tone. |
| "Should I buy more tech stocks?" | Factors to consider + disclaimer. No direct answer. |

**Success Criteria**:
- Response provides educational considerations
- Uses gentle language: "you might consider", "one approach could be"
- Does NOT use commands: "you must", "you should definitely"
- Ends with disclaimer about consulting a financial advisor

---

## Example Expected Responses

### Information Query: "What stocks do I own?"

**Expected Response** (approximate):
```
You currently own the following holdings:

1. Vanguard Total Stock Market ETF (VTI) - 82.5 shares
   - Asset Class: Stocks
   - Sector: Broad Market
   - Purchase Price: $121.06

2. Vanguard Total Bond Market ETF (BND) - 121.4 shares
   - Asset Class: Bonds
   - Sector: Government Bonds
   - Purchase Price: $82.26

[... continues with other holdings ...]

Your portfolio consists of 7 holdings across various asset classes.
```

**What to check**:
- ❌ Should NOT say: "I recommend selling..." or "You should buy..."
- ✅ Should ONLY: List the holdings factually

---

### Advice Query: "How can I improve my portfolio?"

**Expected Response** (approximate):
```
Based on your current portfolio composition, here are some factors you might consider:

Current Allocation Analysis:
- Your portfolio appears well-diversified across major asset classes
- You hold both domestic and international exposure
- Bond allocation provides some stability

Considerations:
- You might consider reviewing your risk tolerance and time horizon
- One approach could be examining the balance between growth and income holdings
- Factors to evaluate include your current exposure to various sectors
- Market conditions and personal financial goals are important considerations

Note: This is educational analysis, not financial advice. Please consult a licensed financial advisor for personalized investment recommendations.
```

**What to check**:
- ✅ Should use: "you might consider", "one approach could be"
- ❌ Should NOT use: "you must buy", "you should definitely sell"
- ✅ Should include: Disclaimer at the end

---

## Red Flags to Watch For

### ❌ BAD (Too pushy):
- "You should buy more bonds"
- "I recommend selling your tech stocks"
- "You need to diversify immediately"
- "You must add international exposure"

### ✅ GOOD (Informational):
- "Your current allocation is 60% stocks, 40% bonds"
- "NVDA is currently trading at $127.45"
- "Your portfolio contains 7 holdings"

### ✅ GOOD (Advisory with gentle language):
- "You might consider reviewing your sector exposure"
- "One factor to evaluate is your bond allocation"
- "Some investors consider diversifying across asset classes"

---

## Debugging

If the system is still giving unwanted recommendations:

1. **Check the query**: Does it contain advice keywords?
   - Keywords: "improve", "should I", "recommendations", "advice"
   - If present, system will enable advisory mode (expected)

2. **Check the planner output**: In Streamlit, expand "View Agent Activity"
   - Look for "Wants Recommendations: YES/NO"
   - Should be NO for information queries

3. **Check the response**: Look for pushy phrases
   - Search for: "you should", "I recommend", "you must"
   - These should NOT appear in information queries

---

## Quick Validation Checklist

After running tests, verify:

- [ ] "What stocks do I own?" → Lists holdings only
- [ ] "What's my allocation?" → Shows breakdown only
- [ ] "How's my portfolio doing?" → Shows numbers only
- [ ] "How can I improve?" → Considerations + disclaimer
- [ ] No information query gives unsolicited recommendations
- [ ] All advice queries include disclaimers
- [ ] Advisory mode uses gentle language, not commands

---

## Expected Test Output

When running `python test_recommendation_fix.py`, you should see:

```
======================================================================
RECOMMENDATION FIX TEST SUITE
======================================================================

This test verifies that:
1. Information queries DON'T get unsolicited recommendations
2. Advice queries DO get recommendations with proper disclaimers

======================================================================
TEST 1: Information Queries (Should NOT give recommendations)
======================================================================

📝 Test Case 1: "What stocks do I own?"
----------------------------------------------------------------------
✓ Wants recommendations: False
✅ PASS: Response is informational without pushy recommendations
   Response length: 542 characters

[... more test cases ...]

======================================================================
TEST SUMMARY
======================================================================
✅ PASS - Information Queries
✅ PASS - Advice Queries

🎉 All tests passed! Recommendation fix is working correctly.
```

---

## Need Help?

If tests fail or system behaves unexpectedly:

1. Check `.env` has `OPENAI_API_KEY`
2. Restart Streamlit app: `streamlit run app.py`
3. Review [RECOMMENDATION_FIX.md](RECOMMENDATION_FIX.md) for implementation details
4. Check [src/nodes/planner_node.py](src/nodes/planner_node.py) detection logic
