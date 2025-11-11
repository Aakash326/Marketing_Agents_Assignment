#!/usr/bin/env python3
"""
Test script to verify recommendation extraction from report format
"""

import re

# Sample report from ReportAgent (your example)
sample_report = """1. **EXECUTIVE SUMMARY:**

🎯 **ANSWER:** YES, consider investing in MSFT for one year.
💡 **REASON:** Strong earnings growth and solid fundamentals indicate potential for future appreciation.

📊 **RECOMMENDATION:** BUY - MSFT
💪 **CONFIDENCE LEVEL:** 7/10
💰 **TARGET PRICE:** $600.00
⏰ **TIME HORIZON:** Medium-term (6-12 months)

📁 **PORTFOLIO CONTEXT:**
   - Current MSFT position: None - New position 
   - Technology exposure: 0% → 6.0% after this position
"""

def test_extraction(content):
    """Test the new extraction logic"""
    recommendation = None
    confidence = None
    
    print("="*80)
    print("TESTING RECOMMENDATION & CONFIDENCE EXTRACTION")
    print("="*80)
    
    # Extract recommendation
    rec_match = re.search(r'RECOMMENDATION:\*?\*?\s*([A-Z\s\-]+?)(?:\n|$)', content, re.IGNORECASE | re.MULTILINE)
    if rec_match:
        rec_text = rec_match.group(1).strip()
        print(f"✅ Found RECOMMENDATION line: '{rec_text}'")
        
        if 'BUY' in rec_text.upper():
            recommendation = 'BUY'
        elif 'SELL' in rec_text.upper():
            recommendation = 'SELL'
        elif 'HOLD' in rec_text.upper():
            recommendation = 'HOLD'
        
        print(f"✅ Extracted recommendation: {recommendation}")
    else:
        print("❌ Could not find RECOMMENDATION line")
    
    # Extract confidence
    conf_match = re.search(r'CONFIDENCE\s+LEVEL:\*?\*?\s*(\d+)/10', content, re.IGNORECASE)
    if conf_match:
        confidence = int(conf_match.group(1)) * 10
        print(f"✅ Extracted confidence: {confidence}%")
    else:
        print("❌ Could not find CONFIDENCE LEVEL")
    
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    print(f"Recommendation: {recommendation}")
    print(f"Confidence: {confidence}%")
    print("="*80)
    
    # Check if correct
    expected_rec = "BUY"
    expected_conf = 70
    
    if recommendation == expected_rec and confidence == expected_conf:
        print("\n✅ ✅ ✅ EXTRACTION WORKING CORRECTLY! ✅ ✅ ✅")
        return True
    else:
        print(f"\n❌ EXTRACTION FAILED!")
        print(f"   Expected: {expected_rec} at {expected_conf}%")
        print(f"   Got: {recommendation} at {confidence}%")
        return False

if __name__ == "__main__":
    success = test_extraction(sample_report)
    exit(0 if success else 1)
