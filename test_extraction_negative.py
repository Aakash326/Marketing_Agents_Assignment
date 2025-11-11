#!/usr/bin/env python3
"""
Test extraction logic for both positive and negative recommendations
"""

import re

def extract_recommendation_and_confidence(content):
    """Extract recommendation and confidence from report content"""
    recommendation = None
    confidence = None
    
    # Extract recommendation
    rec_match = re.search(r'RECOMMENDATION:\*?\*?\s*([A-Z\s\-\']+?)(?:\n|$)', content, re.IGNORECASE | re.MULTILINE)
    if rec_match:
        rec_text = rec_match.group(1).strip()
        print(f"✅ Found RECOMMENDATION line: '{rec_text}'")
        
        # Check negative patterns FIRST
        rec_upper = rec_text.upper()
        
        if "DON'T BUY" in rec_upper or "DONT BUY" in rec_upper or "DO NOT BUY" in rec_upper:
            recommendation = 'AVOID'
        elif "DON'T SELL" in rec_upper or "DONT SELL" in rec_upper:
            recommendation = 'HOLD'
        elif 'WAIT' in rec_upper:
            recommendation = 'WAIT'
        elif 'AVOID' in rec_upper:
            recommendation = 'AVOID'
        elif 'HOLD' in rec_upper:
            recommendation = 'HOLD'
        elif 'STRONG BUY' in rec_upper:
            recommendation = 'STRONG BUY'
        elif 'BUY' in rec_upper:
            recommendation = 'BUY'
        elif 'SELL' in rec_upper:
            recommendation = 'SELL'
        else:
            words = rec_text.split()
            recommendation = words[0].upper() if words else 'HOLD'
        
        print(f"✅ Extracted recommendation: {recommendation}")
    
    # Extract confidence
    conf_match = re.search(r'CONFIDENCE\s+LEVEL:\*?\*?\s*(\d+)/10', content, re.IGNORECASE)
    if conf_match:
        confidence = int(conf_match.group(1)) * 10
        print(f"✅ Extracted confidence: {confidence}%")
    
    return recommendation, confidence


# Test Case 1: BUY recommendation
print("=" * 80)
print("TEST CASE 1: BUY Recommendation")
print("=" * 80)

buy_report = """1. **EXECUTIVE SUMMARY:**

🎯 **ANSWER:** YES, consider investing in MSFT for one year.
💡 **REASON:** Strong earnings growth and solid fundamentals.

📊 **RECOMMENDATION:** BUY - MSFT
💪 **CONFIDENCE LEVEL:** 7/10
💰 **TARGET PRICE:** $600.00
⏰ **TIME HORIZON:** Medium-term (6-12 months)
"""

rec1, conf1 = extract_recommendation_and_confidence(buy_report)
print(f"\n📊 Result: {rec1} at {conf1}%")

expected_rec1 = "BUY"
expected_conf1 = 70

if rec1 == expected_rec1 and conf1 == expected_conf1:
    print("✅ ✅ ✅ TEST 1 PASSED! ✅ ✅ ✅\n")
else:
    print(f"❌ TEST 1 FAILED!")
    print(f"   Expected: {expected_rec1} at {expected_conf1}%")
    print(f"   Got: {rec1} at {conf1}%\n")


# Test Case 2: DON'T BUY recommendation
print("=" * 80)
print("TEST CASE 2: DON'T BUY (WAIT) Recommendation")
print("=" * 80)

dont_buy_report = """1. **EXECUTIVE SUMMARY:**

🎯 **ANSWER:** Don't invest in MSFT right now.
💡 **REASON:** The stock shows neutral technical signals and upcoming earnings that could affect performance.

📊 **RECOMMENDATION:** DON'T BUY - WAIT - MSFT
💪 **CONFIDENCE LEVEL:** 6/10
💰 **TARGET PRICE:** $626.46
⏰ **TIME HORIZON:** 12 months
"""

rec2, conf2 = extract_recommendation_and_confidence(dont_buy_report)
print(f"\n📊 Result: {rec2} at {conf2}%")

expected_rec2 = "AVOID"  # or "WAIT" - both are acceptable
expected_conf2 = 60

if rec2 in ["AVOID", "WAIT"] and conf2 == expected_conf2:
    print("✅ ✅ ✅ TEST 2 PASSED! ✅ ✅ ✅\n")
else:
    print(f"❌ TEST 2 FAILED!")
    print(f"   Expected: AVOID or WAIT at {expected_conf2}%")
    print(f"   Got: {rec2} at {conf2}%\n")


# Summary
print("=" * 80)
print("SUMMARY")
print("=" * 80)

if (rec1 == expected_rec1 and conf1 == expected_conf1 and 
    rec2 in ["AVOID", "WAIT"] and conf2 == expected_conf2):
    print("✅ ✅ ✅ ALL TESTS PASSED! ✅ ✅ ✅")
    print("\nThe extraction logic correctly handles:")
    print("  1. Positive recommendations (BUY)")
    print("  2. Negative recommendations (DON'T BUY)")
    print("  3. Confidence levels (X/10 format)")
else:
    print("❌ SOME TESTS FAILED - Check extraction logic!")
