#!/usr/bin/env python3
"""
Fast 6-Agent Trading Analysis Workflow
Based on the working 7-agent workflow but with ComplianceOfficer removed for speed
"""

import asyncio
import os
import sys
from typing import Dict, Any

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import TextMessage

# Import agents from autogen module
from src.agents.autogen import (
    create_organiser_agent,
    create_risk_manager,
    create_data_analyst,
    create_quantitative_analyst,
    create_strategy_developer,
    create_report_agent
)

def create_fast_6agent_team():
    """Create fast 6-agent team (7-agent minus ComplianceOfficer)"""
    print("🚀 Initializing Fast 6-Agent Trading Team...")
    
    try:
        # Create agents individually with error handling
        print("📊 Creating OrganiserAgent...")
        organiser = create_organiser_agent()

        print("⚠️ Creating RiskManager...")
        risk_mgr = create_risk_manager()

        print("📈 Creating DataAnalyst...")
        data_ana = create_data_analyst()

        print("🔢 Creating QuantitativeAnalyst...")
        quant_ana = create_quantitative_analyst()

        print("🎯 Creating StrategyDeveloper...")
        strategy_dev = create_strategy_developer()

        print("📋 Creating ReportAgent...")
        report_agt = create_report_agent()
        
        agents = [organiser, risk_mgr, data_ana, quant_ana, strategy_dev, report_agt]
        
        # Fast 6-agent configuration - allow more messages for function calls
        team = RoundRobinGroupChat(
            participants=agents,
            termination_condition=TextMentionTermination("FINAL_ANALYSIS_COMPLETE"),
            max_turns=25  # Allow for function calls and responses
        )
        
        print("✅ Fast 6-agent team created successfully")
        return team
        
    except Exception as e:
        print(f"❌ Error creating team: {str(e)}")
        print("💡 Please check your agent configurations and API keys.")
        raise

async def run_6agent_analysis(stock_symbol: str, question: str):
    """
    Main entry point for 6-agent stock analysis.
    Alias for run_fast_6agent_analysis for backwards compatibility.
    """
    return await run_fast_6agent_analysis(stock_symbol, question)


async def run_fast_6agent_analysis(stock_symbol: str, question: str):
    """Run fast 6-agent analysis using proven 7-agent pattern"""
    from datetime import datetime

    # Create team using proven method
    team = create_fast_6agent_team()

    # Fast 6-agent question pattern - one message per agent
    # Simpler, more direct question to ensure agent participation
    enhanced_question = f"""TRADING ANALYSIS REQUEST: {question} for {stock_symbol}

AGENT WORKFLOW:
1. OrganiserAgent: Get current market data for {stock_symbol}
2. RiskManager: Assess position risk
3. DataAnalyst: Research fundamentals
4. QuantitativeAnalyst: Analyze technical signals
5. StrategyDeveloper: Recommend strategy
6. ReportAgent: Provide final recommendation

Each agent should respond with their analysis. Start the analysis now."""

    task = TextMessage(
        content=enhanced_question,
        source='user'
    )

    print(f"🤖 6 agents analyzing: {question} ({stock_symbol})")

    # Collect results for return
    agent_outputs = {}
    all_messages = []
    final_report = ""
    recommendation = "HOLD"
    confidence = 50

    try:
        result_stream = team.run_stream(task=task)

        message_count = 0
        agent_responses = []

        async for message in result_stream:
            message_count += 1

            # Handle different message types
            if hasattr(message, 'content'):
                source = getattr(message, 'source', 'Unknown')
                content = str(message.content)

                print(f"\n{'='*80}")
                print(f"📝 Message {message_count} from {source}")
                print(f"{'='*80}")
                print(content)

                # Store message
                all_messages.append(message)

                # Track agent responses (exclude user messages and function calls)
                if source != 'user' and not content.startswith('[FunctionCall') and not content.startswith('[FunctionExecutionResult'):
                    agent_responses.append(source)
                    agent_outputs[source] = content

                    # Extract final report from ReportAgent
                    if source == 'ReportAgent':
                        final_report = content
                        # Try to extract recommendation and confidence
                        if 'BUY' in content.upper():
                            recommendation = 'BUY'
                        elif 'SELL' in content.upper():
                            recommendation = 'SELL'
                        # Look for confidence percentage
                        import re
                        conf_match = re.search(r'confidence[:\s]+(\d+)%', content, re.IGNORECASE)
                        if conf_match:
                            confidence = int(conf_match.group(1))

                # Check for completion markers
                if any(marker in content for marker in [
                    "FINAL_ANALYSIS_COMPLETE",
                    "RISK_ANALYSIS_COMPLETE",
                    "MARKET_DATA_COMPLETE",
                    "QUANTITATIVE_ANALYSIS_COMPLETE",
                    "STRATEGY_DEVELOPMENT_COMPLETE"
                ]):
                    print(f"\n✅ Agent {source} completed their analysis!")

                # Stop if we have responses from all 6 agents or hit final report
                if len(set(agent_responses)) >= 6 or "FINAL_ANALYSIS_COMPLETE" in content:
                    print(f"\n✅ All agents have provided their analysis!")
                    break

            # Safety stop after reasonable number of messages
            if message_count >= 30:
                print(f"\n⏹️ Stopping after {message_count} messages")
                break

        print(f"\n✅ Analysis complete! {message_count} total messages.")
        print(f"🤖 Agents that responded: {list(set(agent_responses))}")

        # Return structured result matching backend expectations
        return {
            'symbol': stock_symbol,
            'recommendation': recommendation,
            'confidence': confidence,
            'summary': final_report[:500] if final_report else "Analysis completed",
            'execution_plan': {
                'entry_price': 'See report',
                'stop_loss': 'See report',
                'target_price': 'See report',
                'timeline': 'See report'
            },
            'agent_outputs': agent_outputs,
            'timestamp': datetime.now().isoformat(),
            'final_report': final_report,
            'messages': all_messages
        }

    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        print("💡 The agents may need different configuration or API setup.")
        raise

class FastSelection:
    """Same selection interface as working 7-agent workflow"""
    
    def __init__(self):
        self.company_choices = {
            # Tech Giants
            "1": {"symbol": "AAPL", "name": "Apple Inc."},
            "2": {"symbol": "MSFT", "name": "Microsoft Corporation"},
            "3": {"symbol": "GOOGL", "name": "Alphabet Inc."},
            "4": {"symbol": "AMZN", "name": "Amazon.com Inc."},
            "5": {"symbol": "META", "name": "Meta Platforms Inc."},
            "6": {"symbol": "NVDA", "name": "NVIDIA Corporation"},
            "7": {"symbol": "TSLA", "name": "Tesla, Inc."},
            "8": {"symbol": "NFLX", "name": "Netflix Inc."},
            
            # Financial Services
            "9": {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
            "10": {"symbol": "BAC", "name": "Bank of America Corp."},
            "11": {"symbol": "WFC", "name": "Wells Fargo & Company"},
            "12": {"symbol": "GS", "name": "Goldman Sachs Group Inc."},
            "13": {"symbol": "V", "name": "Visa Inc."},
            "14": {"symbol": "MA", "name": "Mastercard Inc."},
            
            # Healthcare & Pharma
            "15": {"symbol": "JNJ", "name": "Johnson & Johnson"},
            "16": {"symbol": "PFE", "name": "Pfizer Inc."},
            "17": {"symbol": "UNH", "name": "UnitedHealth Group Inc."},
            "18": {"symbol": "ABBV", "name": "AbbVie Inc."},
            
            # Consumer & Retail
            "19": {"symbol": "WMT", "name": "Walmart Inc."},
            "20": {"symbol": "PG", "name": "Procter & Gamble Co."},
            "21": {"symbol": "KO", "name": "Coca-Cola Company"},
            "22": {"symbol": "PEP", "name": "PepsiCo Inc."},
            "23": {"symbol": "HD", "name": "Home Depot Inc."},
            
            # Transportation & Services
            "24": {"symbol": "UBER", "name": "Uber Technologies Inc."},
            "25": {"symbol": "LYFT", "name": "Lyft Inc."},
            "26": {"symbol": "SPOT", "name": "Spotify Technology S.A."},
            
            # Energy & Utilities
            "27": {"symbol": "XOM", "name": "Exxon Mobil Corporation"},
            "28": {"symbol": "CVX", "name": "Chevron Corporation"},
            
            # Aerospace & Defense
            "29": {"symbol": "BA", "name": "Boeing Company"},
            "30": {"symbol": "LMT", "name": "Lockheed Martin Corp."}
        }
        
        self.investment_choices = {
            "1": {
                "name": "💰 Buying Decision",
                "description": "Should I buy this stock now? Complete investment analysis.",
                "question": "Should I buy {symbol} stock now? Provide comprehensive buying analysis with entry strategy, price targets, and risk assessment."
            },
            "2": {
                "name": "💸 Selling Decision", 
                "description": "Should I sell this stock now? Exit strategy analysis.",
                "question": "Should I sell {symbol} stock now? Analyze if this is a good time to exit my position and provide sell/hold recommendation."
            },
            "3": {
                "name": "📅 1-Year Investment Plan",
                "description": "Should I invest in this stock for 1 year? Long-term investment strategy.",
                "question": "Should I invest in {symbol} for 1 year? Provide comprehensive 1-year investment strategy, price targets, risks, and expected returns."
            },
            "4": {
                "name": "🏥 General Health Check",
                "description": "Overall company and stock health assessment.",
                "question": "Perform a comprehensive health check on {symbol}. How is the company's financial health, market position, and stock performance?"
            },
            "5": {
                "name": "📈 Next 5-Day Outlook",
                "description": "Short-term price movement and catalysts for next 5 days.",
                "question": "Analyze {symbol} for the next 5 days. What are the key catalysts, technical signals, and short-term price targets?"
            },
            "6": {
                "name": "🚀 Growth Potential Analysis",
                "description": "Long-term growth prospects and investment potential.",
                "question": "Evaluate {symbol} long-term growth potential. What are the growth drivers, competitive advantages, and 1-3 year outlook?"
            },
            "7": {
                "name": "⚠️ Risk Assessment",
                "description": "Comprehensive risk analysis and downside protection.",
                "question": "Conduct a thorough risk analysis for {symbol}. What are the main risks, downside scenarios, and how to protect against them?"
            },
            "8": {
                "name": "🏢 Sector Comparison",
                "description": "How does this company compare to its sector peers?",
                "question": "Compare {symbol} to its sector peers. How does it rank in terms of valuation, growth, and competitive position?"
            },
            "9": {
                "name": "📊 Options Strategy",
                "description": "Options trading opportunities and strategies analysis.",
                "question": "Analyze options strategies for {symbol}. What are the best options plays, volatility outlook, and risk/reward scenarios?"
            },
            "10": {
                "name": "🌱 ESG & Sustainability",
                "description": "Environmental, Social, and Governance analysis.",
                "question": "Evaluate {symbol} ESG profile. How does the company score on environmental, social, and governance factors?"
            },
            "11": {
                "name": "📅 Earnings Forecast",
                "description": "Upcoming earnings analysis and price impact prediction.",
                "question": "Analyze {symbol} upcoming earnings. What are the expectations, potential surprises, and likely price impact?"
            },
            "12": {
                "name": "💎 Dividend Analysis",
                "description": "Dividend yield, sustainability, and income potential.",
                "question": "Analyze {symbol} dividend prospects. What is the yield, sustainability, growth potential, and income strategy?"
            },
            "13": {
                "name": "📊 Technical Analysis",
                "description": "Chart patterns, support/resistance, and technical indicators.",
                "question": "Provide technical analysis for {symbol}. What do the charts, patterns, and indicators suggest for price movement?"
            },
            "14": {
                "name": "🏃‍♂️ Momentum & Trends",
                "description": "Price momentum, trend analysis, and momentum indicators.",
                "question": "Analyze price momentum and trends for {symbol}. What do momentum indicators and trend analysis suggest?"
            }
        }

    def display_welcome(self):
        print("🎉 Welcome to Fast 6-Agent Trading Analysis!")
        print("============================================================")
        print("🚀 Enhanced speed with 6 essential agents")
        print("📊 Real-time stock analysis with proven AI workflow")
        print("============================================================")

    def select_company(self):
        print("\n🔄 STEP 1: Company Selection")
        print("\n============================================================")
        print("🏢 SELECT COMPANY FOR ANALYSIS")
        print("============================================================")
        
        print("\n📈 Popular Companies:")
        for key, company in self.company_choices.items():
            print(f"   {key:>2}.  {company['symbol']:>5} - {company['name']}")
        
        print("\n🔍 Custom Option:")
        print("  custom. Enter your own stock symbol")
        print("-" * 60)
        
        while True:
            choice = input("\n👉 Enter your choice (1-30 or 'custom'): ").strip()
            
            if choice in self.company_choices:
                selected = self.company_choices[choice]
                return selected['symbol'], selected['name']
            elif choice.lower() == 'custom':
                symbol = input("📝 Enter stock symbol (e.g., AAPL): ").strip().upper()
                if symbol:
                    name = input(f"📝 Enter company name for {symbol} (optional): ").strip()
                    return symbol, name if name else f"{symbol} Corporation"
            
            print("❌ Invalid choice. Please try again.")

    def select_analysis_type(self, symbol: str, name: str):
        print(f"\n🔄 STEP 2: Analysis Focus")
        print(f"\n🏢 Selected Company: {symbol} - {name}")
        
        print("\n============================================================")
        print("🎯 SELECT YOUR INVESTMENT QUESTION")
        print("============================================================")
        
        for key, analysis in self.investment_choices.items():
            print(f"\n{key}. {analysis['name']}")
            print(f"   {analysis['description']}")
        
        print("-" * 60)
        
        while True:
            choice = input("\n👉 Enter your choice (1-14): ").strip()
            
            if choice in self.investment_choices:
                selected = self.investment_choices[choice]
                question = selected['question'].format(symbol=symbol)
                return selected['name'], question
            
            print("❌ Invalid choice. Please try again.")

    def confirm_analysis(self, symbol: str, name: str, analysis_name: str, question: str):
        print("\n" + "=" * 80)
        print("📋 ANALYSIS REQUEST SUMMARY")
        print("=" * 80)
        print(f"🏢 Company: {symbol} - {name}")
        print(f"🎯 Analysis: {analysis_name}")
        print(f"❓ Question: {question}")
        print("=" * 80)
        
        while True:
            confirm = input("\n✅ Proceed with fast 6-agent analysis? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return True
            elif confirm in ['n', 'no']:
                return False
            print("❌ Please enter 'y' for yes or 'n' for no.")

async def main():
    """Main fast 6-agent workflow execution"""
    selector = FastSelection()
    
    # Welcome
    selector.display_welcome()
    
    # Step 1: Select company
    symbol, name = selector.select_company()
    
    # Step 2: Select analysis type  
    analysis_name, question = selector.select_analysis_type(symbol, name)
    
    # Step 3: Confirm and run
    if selector.confirm_analysis(symbol, name, analysis_name, question):
        print("\n🚀 Starting Fast 6-Agent Analysis...")
        await run_fast_6agent_analysis(symbol, question)
    else:
        print("\n❌ Analysis cancelled.")
    
    print("\n" + "=" * 80)
    print("📊 ANALYSIS COMPLETE")
    print("=" * 80)
    print("✅ Fast 6-agent workflow finished!")
    print("📈 Review the agent analysis above for insights")

if __name__ == "__main__":
    asyncio.run(main())