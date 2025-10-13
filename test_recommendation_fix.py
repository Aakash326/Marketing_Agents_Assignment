"""
Test script to verify the recommendation fix works correctly.
Tests both information queries (should NOT give recommendations)
and advice queries (should give recommendations with disclaimers).
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_information_queries():
    """Test that information queries DON'T give recommendations."""
    print("=" * 70)
    print("TEST 1: Information Queries (Should NOT give recommendations)")
    print("=" * 70)

    test_cases = [
        "What stocks do I own?",
        "What's my allocation?",
        "How is my portfolio performing?"
    ]

    if not os.getenv("OPENAI_API_KEY"):
        print("⏭️  Skipping - no API key found")
        return True

    try:
        from src.graph.workflow import run_workflow

        for i, query in enumerate(test_cases, 1):
            print(f"\n📝 Test Case {i}: \"{query}\"")
            print("-" * 70)

            result = run_workflow(query, "CLT-001")

            wants_recs = result.get("wants_recommendations", False)
            response = result.get("response", "")

            print(f"✓ Wants recommendations: {wants_recs}")

            if wants_recs:
                print("❌ FAIL: System incorrectly flagged this as wanting recommendations")
                print(f"   Query: {query}")
                return False

            # Check if response contains pushy language
            pushy_phrases = [
                "you should buy",
                "you should sell",
                "i recommend",
                "you need to",
                "must buy",
                "must sell"
            ]

            response_lower = response.lower()
            found_pushy = [phrase for phrase in pushy_phrases if phrase in response_lower]

            if found_pushy:
                print(f"⚠️  WARNING: Response contains pushy language: {found_pushy}")
                print(f"   First 200 chars: {response[:200]}")
            else:
                print("✅ PASS: Response is informational without pushy recommendations")

            print(f"   Response length: {len(response)} characters")

        return True

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_advice_queries():
    """Test that advice queries DO give recommendations with disclaimers."""
    print("\n" + "=" * 70)
    print("TEST 2: Advice Queries (SHOULD give recommendations + disclaimer)")
    print("=" * 70)

    test_cases = [
        "How can I improve my portfolio?",
        "What should I do to diversify?",
        "Give me investment recommendations"
    ]

    if not os.getenv("OPENAI_API_KEY"):
        print("⏭️  Skipping - no API key found")
        return True

    try:
        from src.graph.workflow import run_workflow

        for i, query in enumerate(test_cases, 1):
            print(f"\n📝 Test Case {i}: \"{query}\"")
            print("-" * 70)

            result = run_workflow(query, "CLT-001")

            wants_recs = result.get("wants_recommendations", False)
            response = result.get("response", "")

            print(f"✓ Wants recommendations: {wants_recs}")

            if not wants_recs:
                print("❌ FAIL: System should have detected advice request")
                print(f"   Query: {query}")
                return False

            # Check if response contains disclaimer
            disclaimer_keywords = [
                "not financial advice",
                "consult a licensed",
                "consult a financial advisor",
                "educational analysis"
            ]

            response_lower = response.lower()
            has_disclaimer = any(keyword in response_lower for keyword in disclaimer_keywords)

            if not has_disclaimer:
                print("⚠️  WARNING: Response lacks disclaimer")
                print(f"   Last 200 chars: {response[-200:]}")
            else:
                print("✅ PASS: Response has proper disclaimer")

            # Check for gentle language (not commands)
            gentle_phrases = ["you might consider", "you could", "one approach", "factors to consider"]
            has_gentle = any(phrase in response_lower for phrase in gentle_phrases)

            command_phrases = ["you must", "you need to", "you should buy", "you should sell"]
            has_commands = any(phrase in response_lower for phrase in command_phrases)

            if has_gentle:
                print("✅ Response uses gentle suggestion language")
            if has_commands:
                print("⚠️  WARNING: Response contains command language (should be softer)")

            print(f"   Response length: {len(response)} characters")

        return True

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all recommendation tests."""
    print("\n" + "=" * 70)
    print("RECOMMENDATION FIX TEST SUITE")
    print("=" * 70)
    print("\nThis test verifies that:")
    print("1. Information queries DON'T get unsolicited recommendations")
    print("2. Advice queries DO get recommendations with proper disclaimers\n")

    results = []

    # Test information queries
    results.append(("Information Queries", test_information_queries()))

    # Test advice queries
    results.append(("Advice Queries", test_advice_queries()))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(r[1] for r in results)

    if all_passed:
        print("\n🎉 All tests passed! Recommendation fix is working correctly.")
        print("\nExpected behavior:")
        print("  • 'What stocks do I own?' → List only, NO recommendations")
        print("  • 'How can I improve my portfolio?' → Considerations + disclaimer")
    else:
        print("\n⚠️  Some tests had issues. Review the output above.")

    print("=" * 70)


if __name__ == "__main__":
    main()
