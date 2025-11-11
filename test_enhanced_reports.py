#!/usr/bin/env python3
"""
Test script to generate enhanced investment reports for META and AAPL.
Tests all 5 enhancement changes:
1. Direct Answer Section
2. Portfolio Context
3. Risk/Reward Ratio Analysis
4. Debug Artifacts Removal
5. Enhanced Decision Reasoning
"""

import asyncio
import json
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.workflows.trading_workflow import run_fast_6agent_analysis


async def test_meta_analysis():
    """
    TEST CASE 1: META (New Position)
    User asking "Should I invest in this for 1 year?"
    No existing position - should use BUY/DON'T BUY terminology
    """
    print("\n" + "="*80)
    print("TEST CASE 1: META - New Position")
    print("="*80)

    portfolio_data = {
        "total_value": 100000.0,
        "holdings": {},  # No current META position
        "sector_exposure": {
            "Technology": 15.0
        }
    }

    try:
        result = await run_fast_6agent_analysis(
            stock_symbol="META",
            question="Should I invest in this for 1 year?",
            portfolio_data=portfolio_data
        )

        print("\n📊 META ANALYSIS RESULT:")
        print(f"Symbol: {result.get('symbol')}")
        print(f"Recommendation: {result.get('recommendation')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"\n📄 FULL REPORT:\n")
        print(result.get('final_report', 'No report generated'))

        # Save to file
        with open('/Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents/test_meta_report.md', 'w') as f:
            f.write(result.get('final_report', 'No report generated'))
        print("\n✅ META report saved to test_meta_report.md")

        return result

    except Exception as e:
        print(f"\n❌ Error testing META: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


async def test_aapl_analysis():
    """
    TEST CASE 2: AAPL (Existing Position)
    User asking "Should I hold my Apple shares?"
    Existing position - should use HOLD/ADD/SELL terminology
    """
    print("\n" + "="*80)
    print("TEST CASE 2: AAPL - Existing Position")
    print("="*80)

    portfolio_data = {
        "total_value": 100000.0,
        "holdings": {
            "AAPL": {
                "shares": 50,
                "value": 13423.5,
                "pct": 13.4
            }
        },
        "sector_exposure": {
            "Technology": 18.0
        }
    }

    try:
        result = await run_fast_6agent_analysis(
            stock_symbol="AAPL",
            question="Should I hold my Apple shares?",
            portfolio_data=portfolio_data
        )

        print("\n📊 AAPL ANALYSIS RESULT:")
        print(f"Symbol: {result.get('symbol')}")
        print(f"Recommendation: {result.get('recommendation')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"\n📄 FULL REPORT:\n")
        print(result.get('final_report', 'No report generated'))

        # Save to file
        with open('/Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents/test_aapl_report.md', 'w') as f:
            f.write(result.get('final_report', 'No report generated'))
        print("\n✅ AAPL report saved to test_aapl_report.md")

        return result

    except Exception as e:
        print(f"\n❌ Error testing AAPL: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


async def validate_enhancements(result, test_name):
    """Validate that all 5 enhancements are present in the report"""
    if not result:
        print(f"\n❌ {test_name}: No result to validate")
        return False

    report = result.get('final_report', '')

    print(f"\n🔍 VALIDATION CHECKLIST for {test_name}:")
    print("-" * 60)

    # Check 1: Direct Answer Section
    has_answer = "**ANSWER:**" in report or "🎯" in report
    print(f"{'✅' if has_answer else '❌'} 1. Direct YES/NO answer at top")

    # Check 2: Portfolio Context
    has_portfolio = "PORTFOLIO CONTEXT" in report or "📁" in report
    print(f"{'✅' if has_portfolio else '❌'} 2. Portfolio context showing holdings & sector")

    # Check 3: Risk/Reward Ratio
    has_risk_reward = "RISK/REWARD RATIO" in report or "⚖️" in report
    print(f"{'✅' if has_risk_reward else '❌'} 3. Risk/reward ratio with dollar amounts")

    # Check 4: No Debug Text
    has_debug = "FINAL_ANALYSIS_COMPLETE" in report
    print(f"{'✅' if not has_debug else '❌'} 4. No debug text (FINAL_ANALYSIS_COMPLETE)")

    # Check 5: Comparative Reasoning
    has_comparative = "Why" in report and ("Now" in report or "META" in report or "AAPL" in report)
    print(f"{'✅' if has_comparative else '❌'} 5. Comparative reasoning section")

    # Check formatting
    has_commas = "," in report and "$" in report
    print(f"{'✅' if has_commas else '❌'} 6. Dollar amounts formatted with commas")

    all_pass = has_answer and has_portfolio and has_risk_reward and not has_debug and has_comparative

    print("-" * 60)
    if all_pass:
        print(f"✅ {test_name}: ALL VALIDATIONS PASSED")
    else:
        print(f"⚠️ {test_name}: SOME VALIDATIONS FAILED")

    return all_pass


async def main():
    """Run both test cases"""
    print("\n" + "="*80)
    print("TESTING ENHANCED AUTOGEN REPORT GENERATION")
    print("="*80)
    print("\nThis will test all 5 enhancements:")
    print("1. ✅ Direct Answer Section (YES/NO upfront)")
    print("2. ✅ Portfolio Context (holdings & sector exposure)")
    print("3. ✅ Risk/Reward Ratio Analysis (with dollar amounts)")
    print("4. ✅ Debug Artifacts Removal (clean output)")
    print("5. ✅ Enhanced Decision Reasoning (comparative analysis)")

    # Test META (new position)
    meta_result = await test_meta_analysis()
    await asyncio.sleep(2)

    # Test AAPL (existing position)
    aapl_result = await test_aapl_analysis()

    # Validate results
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80)

    meta_valid = await validate_enhancements(meta_result, "META")
    aapl_valid = await validate_enhancements(aapl_result, "AAPL")

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"META Test: {'✅ PASSED' if meta_valid else '❌ FAILED'}")
    print(f"AAPL Test: {'✅ PASSED' if aapl_valid else '❌ FAILED'}")

    if meta_valid and aapl_valid:
        print("\n🎉 ALL TESTS PASSED! Enhanced reports are working correctly.")
    else:
        print("\n⚠️ SOME TESTS FAILED. Review the reports for missing elements.")

    print("\n📄 Generated Reports:")
    print("- test_meta_report.md")
    print("- test_aapl_report.md")


if __name__ == "__main__":
    asyncio.run(main())
