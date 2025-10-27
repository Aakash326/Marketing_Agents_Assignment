"""
Test Script for 6-Agent Trading Analysis Workflow

This script demonstrates how to use the AutoGen-based 6-agent trading analysis system.
It runs comprehensive analysis on a stock symbol and displays the results.

Usage:
    python test_6agent_workflow.py [STOCK_SYMBOL]

Example:
    python test_6agent_workflow.py AAPL
    python test_6agent_workflow.py MSFT
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.workflows.trading_workflow import run_fast_6agent_analysis


async def test_single_stock(symbol: str = "AAPL"):
    """
    Test 6-agent analysis for a single stock.

    Args:
        symbol: Stock ticker symbol
    """
    print("=" * 100)
    print(" " * 30 + "6-AGENT TRADING ANALYSIS TEST")
    print("=" * 100)
    print()
    print(f"🔍 Analyzing: {symbol}")
    print(f"📊 This will run 6 specialized AI agents in sequence:")
    print("   1. OrganiserAgent - Market data & technical indicators")
    print("   2. RiskManager - Position sizing & risk metrics")
    print("   3. DataAnalyst - Fundamental analysis & news research")
    print("   4. QuantitativeAnalyst - Technical signal generation")
    print("   5. StrategyDeveloper - Execution strategy creation")
    print("   6. ReportAgent - Final recommendation synthesis")
    print()
    print("⏳ Please wait 30-90 seconds for complete analysis...")
    print("=" * 100)
    print()

    try:
        # Run analysis using the new fast workflow
        result = await run_fast_6agent_analysis(
            stock_symbol=symbol,
            question="Should I buy this stock?"
        )

        # Display formatted results
        print("\n" + "=" * 100)
        print(f"📊 ANALYSIS COMPLETE FOR {result['symbol']}")
        print("=" * 100)
        print(f"\n{result['final_report']}\n")

        # Display conversation history
        if 'messages' in result:
            print("\n" + "=" * 100)
            print(" " * 35 + "AGENT CONVERSATION")
            print("=" * 100)
            print()
            for msg in result['messages'][-10:]:  # Show last 10 messages
                speaker = msg.source if hasattr(msg, 'source') else 'Unknown'
                content = msg.content if hasattr(msg, 'content') else str(msg)
                print(f"📌 {speaker}:")
                print(f"   {content[:200]}...")  # First 200 chars
                print()

        print()
        print("=" * 100)
        print("✅ Analysis Complete!")
        print("=" * 100)

        return result

    except Exception as e:
        print(f"\n❌ ERROR: Analysis failed for {symbol}")
        print(f"   Error message: {str(e)}")
        print()
        print("🔧 Troubleshooting:")
        print("   1. Check that OPENAI_API_KEY is set in .env file")
        print("   2. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("   3. Verify internet connection for market data APIs")
        print("   4. Check that stock symbol is valid (e.g., AAPL, MSFT, GOOGL)")
        print()
        raise


async def test_multiple_stocks():
    """
    Test 6-agent analysis for multiple stocks in batch.
    """
    print("=" * 100)
    print(" " * 30 + "6-AGENT BATCH ANALYSIS TEST")
    print("=" * 100)
    print()

    symbols = ["AAPL", "MSFT", "GOOGL"]
    print(f"🔍 Analyzing {len(symbols)} stocks: {', '.join(symbols)}")
    print("⏳ This may take several minutes...")
    print()

    results = {}

    try:
        for symbol in symbols:
            print(f"\n📊 Analyzing {symbol}...")
            try:
                result = await run_fast_6agent_analysis(
                    stock_symbol=symbol,
                    question="Should I buy this stock?"
                )
                results[symbol] = result
                print(f"✅ {symbol} complete")
            except Exception as e:
                print(f"❌ {symbol} failed: {str(e)}")
                results[symbol] = None

        print("\n" + "=" * 100)
        print(" " * 35 + "BATCH RESULTS SUMMARY")
        print("=" * 100)
        print()

        for symbol, result in results.items():
            if result:
                print(f"📊 {symbol}:")
                print(f"   Final Report Preview: {result.get('final_report', 'N/A')[:100]}...")
                print()
            else:
                print(f"❌ {symbol}: Analysis failed")
                print()

        print("=" * 100)
        print("✅ Batch Analysis Complete!")
        print("=" * 100)

        return results

    except Exception as e:
        print(f"\n❌ ERROR: Batch analysis failed")
        print(f"   Error message: {str(e)}")
        raise


async def interactive_mode():
    """
    Interactive mode for testing multiple stocks.
    """
    print("=" * 100)
    print(" " * 30 + "6-AGENT INTERACTIVE MODE")
    print("=" * 100)
    print()
    print("Enter stock symbols to analyze (or 'quit' to exit)")
    print()

    while True:
        symbol = input("📊 Enter stock symbol (e.g., AAPL): ").strip().upper()

        if symbol in ['QUIT', 'EXIT', 'Q']:
            print("\n👋 Goodbye!")
            break

        if not symbol:
            continue

        try:
            await test_single_stock(symbol)

            another = input("\n🔄 Analyze another stock? (yes/no): ").strip().lower()
            if another not in ['yes', 'y']:
                print("\n👋 Goodbye!")
                break

        except Exception as e:
            print(f"\n❌ Error analyzing {symbol}: {str(e)}")
            continue_anyway = input("\n🔄 Try another stock? (yes/no): ").strip().lower()
            if continue_anyway not in ['yes', 'y']:
                break


def main():
    """Main entry point for test script."""
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in environment")
        print("   Please set OPENAI_API_KEY in your .env file")
        print("   Example: OPENAI_API_KEY=sk-...")
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--batch":
            # Batch mode
            asyncio.run(test_multiple_stocks())
        elif sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            # Interactive mode
            asyncio.run(interactive_mode())
        else:
            # Single stock mode
            symbol = sys.argv[1].upper()
            asyncio.run(test_single_stock(symbol))
    else:
        # Default: analyze AAPL
        print("ℹ️  No stock symbol provided, defaulting to AAPL")
        print("   Usage: python test_6agent_workflow.py [SYMBOL]")
        print("   Example: python test_6agent_workflow.py MSFT")
        print("   Options:")
        print("      --batch        : Analyze multiple stocks (AAPL, MSFT, GOOGL)")
        print("      --interactive  : Interactive mode to analyze multiple stocks")
        print()
        asyncio.run(test_single_stock("AAPL"))


if __name__ == "__main__":
    main()
