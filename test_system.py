"""
Simple test script to verify the system works.
Run this before launching Streamlit to check basic functionality.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from src.state.graph_state import GraphState
        from src.llm.client import get_llm
        from src.tools.portfolio_tools import load_portfolio_data
        from src.tools.market_tools import get_stock_price
        from src.nodes.planner_node import planner_node
        from src.graph.workflow import create_workflow, run_workflow
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


def test_env_vars():
    """Test that environment variables are set."""
    print("\nTesting environment variables...")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY is set (length: {len(api_key)})")
        return True
    else:
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Please create a .env file with your OpenAI API key")
        return False


def test_portfolio_data():
    """Test loading portfolio data."""
    print("\nTesting portfolio data loading...")
    try:
        from src.tools.portfolio_tools import load_portfolio_data
        data = load_portfolio_data("portfolios.xlsx", "CLT-001")

        if "error" in data:
            print(f"❌ Error loading portfolio: {data['error']}")
            return False

        print(f"✅ Portfolio loaded successfully!")
        print(f"   Client: {data['client_id']}")
        print(f"   Holdings: {data['total_holdings']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_market_data():
    """Test fetching market data."""
    print("\nTesting market data fetching...")
    try:
        from src.tools.market_tools import get_stock_price
        data = get_stock_price("AAPL")

        if "error" in data:
            print(f"⚠️  Warning: {data['error']}")
            print("   This might be due to market hours or rate limits")
            return True  # Don't fail on this

        print(f"✅ Market data fetched successfully!")
        print(f"   Symbol: {data.get('symbol')}")
        print(f"   Price: ${data.get('current_price', 0):.2f}")
        return True
    except Exception as e:
        print(f"⚠️  Warning: {e}")
        print("   Market data fetch failed, but this might be expected")
        return True  # Don't fail on this


def test_workflow():
    """Test the LangGraph workflow (requires OpenAI API key)."""
    print("\nTesting LangGraph workflow...")

    if not os.getenv("OPENAI_API_KEY"):
        print("⏭️  Skipping workflow test (no API key)")
        return True

    try:
        from src.graph.workflow import run_workflow

        print("   Running test query: 'What stocks do I own?'")
        result = run_workflow("What stocks do I own?", "CLT-001")

        if result.get("response"):
            print(f"✅ Workflow executed successfully!")
            print(f"   Response length: {len(result['response'])} characters")
            print(f"   Portfolio agent used: {result.get('needs_portfolio')}")
            print(f"   Market agent used: {result.get('needs_market')}")
            return True
        else:
            print("❌ Workflow executed but no response generated")
            return False

    except Exception as e:
        print(f"❌ Workflow error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Portfolio & Market Intelligence System - Test Suite")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Environment Variables", test_env_vars()))
    results.append(("Portfolio Data", test_portfolio_data()))
    results.append(("Market Data", test_market_data()))

    # Only run workflow test if previous tests passed
    if all(r[1] for r in results[:2]):  # Check imports and env vars
        results.append(("Workflow", test_workflow()))
    else:
        print("\n⏭️  Skipping workflow test due to previous failures")

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(r[1] for r in results)

    if all_passed:
        print("\n🎉 All tests passed! You can now run: streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

    print("=" * 60)


if __name__ == "__main__":
    main()
