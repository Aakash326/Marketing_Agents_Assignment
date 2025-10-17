"""
6-Agent Trading Analysis Workflow

This module orchestrates the 6-agent trading analysis system using AutoGen's
RoundRobinGroupChat for sequential communication and collaborative decision-making.
"""

import os
import sys
import logging
import asyncio
import re
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path for imports to work
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from src.agents.autogen import (
    create_organiser_agent,
    create_risk_manager,
    create_data_analyst,
    create_quantitative_analyst,
    create_strategy_developer,
    create_report_agent
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class TradingWorkflowResult:
    """Result container for 6-agent trading analysis."""
    symbol: str
    recommendation: str  # BUY, HOLD, or SELL
    confidence: int  # 1-100
    summary: str
    execution_plan: Dict[str, Any]
    agent_outputs: Dict[str, str]
    timestamp: str
    full_conversation: str


def extract_recommendation_from_output(output: str) -> Dict[str, Any]:
    """
    Extract structured recommendation from ReportAgent output.

    Args:
        output: Full conversation output

    Returns:
        dict: Extracted recommendation details
    """
    result = {
        'recommendation': 'HOLD',
        'confidence': 50,
        'entry_price': None,
        'target_price': None,
        'stop_loss': None,
        'position_size': None,
        'timeline': 'MEDIUM-TERM'
    }

    try:
        # Extract recommendation
        match = re.search(r'📊 DECISION:\s*(BUY|HOLD|SELL)', output)
        if match:
            result['recommendation'] = match.group(1)

        # Extract confidence
        match = re.search(r'🎯 CONFIDENCE:\s*(\d+)%', output)
        if match:
            result['confidence'] = int(match.group(1))

        # Extract execution parameters
        match = re.search(r'Entry Price:\s*\$(\d+\.?\d*)', output)
        if match:
            result['entry_price'] = float(match.group(1))

        match = re.search(r'Target Price:\s*\$(\d+\.?\d*)', output)
        if match:
            result['target_price'] = float(match.group(1))

        match = re.search(r'Stop-Loss:\s*\$(\d+\.?\d*)', output)
        if match:
            result['stop_loss'] = float(match.group(1))

        match = re.search(r'Position Size:\s*(\d+\.?\d*)%', output)
        if match:
            result['position_size'] = float(match.group(1))

        match = re.search(r'Timeline:\s*(SHORT-TERM|MEDIUM-TERM|LONG-TERM)', output)
        if match:
            result['timeline'] = match.group(1)

    except Exception as e:
        logger.error(f"Error extracting recommendation: {str(e)}")

    return result


def parse_agent_outputs(conversation: str) -> Dict[str, str]:
    """
    Parse individual agent outputs from conversation.

    Args:
        conversation: Full conversation text

    Returns:
        dict: Agent name -> output mapping
    """
    agent_outputs = {}

    # Define agent markers
    agents = [
        'OrganiserAgent',
        'RiskManager',
        'DataAnalyst',
        'QuantitativeAnalyst',
        'StrategyDeveloper',
        'ReportAgent'
    ]

    for agent in agents:
        # Find agent's output in conversation
        pattern = f"{agent}.*?━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━.*?━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        match = re.search(pattern, conversation, re.DOTALL)
        if match:
            agent_outputs[agent] = match.group(0)
        else:
            agent_outputs[agent] = f"{agent}: No output captured"

    return agent_outputs


async def run_6agent_analysis(
    stock_symbol: str,
    question: str = "Should I buy this stock?",
    portfolio_value: float = 100000.0,
    risk_per_trade: float = 2.0,
    model_name: str = "gpt-4o-mini",
    max_turns: int = 20
) -> TradingWorkflowResult:
    """
    Run comprehensive 6-agent trading analysis workflow.

    This function orchestrates 6 specialized agents in a round-robin communication pattern:
    1. OrganiserAgent - Fetches market data and technical indicators
    2. RiskManager - Calculates position sizing and risk metrics
    3. DataAnalyst - Analyzes fundamentals and recent news
    4. QuantitativeAnalyst - Generates technical trading signals
    5. StrategyDeveloper - Creates execution strategy with entry/exit
    6. ReportAgent - Synthesizes insights and provides final recommendation

    Args:
        stock_symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
        question: Analysis question (default: "Should I buy this stock?")
        portfolio_value: Total portfolio value in dollars (default: $100,000)
        risk_per_trade: Risk percentage per trade (default: 2%)
        model_name: OpenAI model to use (default: "gpt-4o-mini")
        max_turns: Maximum number of conversation turns (default: 20)

    Returns:
        TradingWorkflowResult: Comprehensive analysis results

    Raises:
        ValueError: If stock_symbol is invalid or API keys are missing
        RuntimeError: If workflow execution fails

    Example:
        >>> result = await run_6agent_analysis("AAPL")
        >>> print(f"Recommendation: {result.recommendation}")
        >>> print(f"Confidence: {result.confidence}%")
    """
    logger.info(f"Starting 6-agent analysis for {stock_symbol}")
    start_time = datetime.now()

    # Validate inputs
    if not stock_symbol or not isinstance(stock_symbol, str):
        raise ValueError("Invalid stock symbol provided")

    stock_symbol = stock_symbol.upper().strip()

    # Check for required API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    try:
        # Create shared model client for all agents
        model_client = OpenAIChatCompletionClient(
            model=model_name,
            api_key=openai_key
        )

        logger.info("Initializing 6 specialized agents...")

        # Create all 6 agents with shared model client
        organiser = create_organiser_agent(model_client)
        risk_manager = create_risk_manager(model_client)
        data_analyst = create_data_analyst(model_client)
        quant_analyst = create_quantitative_analyst(model_client)
        strategy_dev = create_strategy_developer(model_client)
        report = create_report_agent(model_client)

        logger.info("Setting up RoundRobinGroupChat team...")

        # Create team with round-robin communication
        # Agents will speak in order: Organiser -> Risk -> Data -> Quant -> Strategy -> Report
        # Each agent gets one turn, so 6 agents + 1 initial message = 7 max messages
        team = RoundRobinGroupChat(
            participants=[
                organiser,
                risk_manager,
                data_analyst,
                quant_analyst,
                strategy_dev,
                report
            ],
            # Terminate after all 6 agents have spoken (6 agent messages + 1 user message = 7 total)
            termination_condition=MaxMessageTermination(max_messages=7),
            max_turns=max_turns
        )

        # Construct enhanced question with context and instructions
        enhanced_question = f"""
{question} for stock symbol: {stock_symbol}

PORTFOLIO CONTEXT:
• Portfolio Value: ${portfolio_value:,.2f}
• Risk Per Trade: {risk_per_trade}%
• Analysis Date: {datetime.now().strftime('%Y-%m-%d')}

INSTRUCTIONS FOR ALL AGENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. OrganiserAgent: Start by fetching comprehensive market data and technical indicators for {stock_symbol}
2. RiskManager: Calculate position sizing and risk metrics based on portfolio value
3. DataAnalyst: Analyze fundamentals, news, and analyst opinions
4. QuantitativeAnalyst: Generate trading signals from technical indicators
5. StrategyDeveloper: Create detailed execution strategy with entry/exit/timeline
6. ReportAgent: Synthesize ALL inputs and provide final BUY/SELL/HOLD recommendation

CRITICAL RULES:
• Each agent MUST use their specialized tools to gather REAL data
• Provide detailed, structured analysis with specific numbers and dates
• Include actual prices, percentages, and concrete metrics in your analysis
• Wait for ALL agents before ReportAgent makes final decision
• Be specific and actionable, not generic
• Format your response clearly with headers and bullet points

Begin analysis now for {stock_symbol}!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        logger.info(f"Starting team analysis for {stock_symbol}...")
        logger.info("This may take 30-90 seconds depending on API response times...")

        # Run the analysis
        result = await team.run(task=TextMessage(content=enhanced_question, source="user"))

        logger.info("Team analysis completed successfully")

        # Extract conversation text
        full_conversation = ""
        for message in result.messages:
            if hasattr(message, 'content'):
                full_conversation += f"\n{message.source}: {message.content}\n"

        # Parse outputs
        agent_outputs = parse_agent_outputs(full_conversation)

        # Extract recommendation
        recommendation_data = extract_recommendation_from_output(full_conversation)

        # Create execution plan
        execution_plan = {
            'entry_price': recommendation_data.get('entry_price'),
            'target_price': recommendation_data.get('target_price'),
            'stop_loss': recommendation_data.get('stop_loss'),
            'position_size_pct': recommendation_data.get('position_size'),
            'timeline': recommendation_data.get('timeline'),
            'portfolio_value': portfolio_value,
            'risk_per_trade_pct': risk_per_trade
        }

        # Extract summary from ReportAgent output
        summary = "Analysis completed successfully."
        if 'ReportAgent' in agent_outputs:
            # Try to extract executive summary
            match = re.search(r'📋 EXECUTIVE SUMMARY:\n(.*?)(?:\n\n|✅)', agent_outputs['ReportAgent'], re.DOTALL)
            if match:
                summary = match.group(1).strip()

        # Create result object
        workflow_result = TradingWorkflowResult(
            symbol=stock_symbol,
            recommendation=recommendation_data['recommendation'],
            confidence=recommendation_data['confidence'],
            summary=summary,
            execution_plan=execution_plan,
            agent_outputs=agent_outputs,
            timestamp=datetime.now().isoformat(),
            full_conversation=full_conversation
        )

        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Analysis completed in {elapsed_time:.1f} seconds")
        logger.info(f"Final recommendation: {workflow_result.recommendation} ({workflow_result.confidence}% confidence)")

        return workflow_result

    except Exception as e:
        logger.error(f"Error running 6-agent analysis: {str(e)}", exc_info=True)
        raise RuntimeError(f"Workflow execution failed: {str(e)}") from e


async def run_batch_analysis(
    stock_symbols: list,
    portfolio_value: float = 100000.0,
    risk_per_trade: float = 2.0
) -> Dict[str, TradingWorkflowResult]:
    """
    Run 6-agent analysis for multiple stocks in batch.

    Args:
        stock_symbols: List of stock ticker symbols
        portfolio_value: Total portfolio value
        risk_per_trade: Risk percentage per trade

    Returns:
        dict: Symbol -> TradingWorkflowResult mapping
    """
    logger.info(f"Starting batch analysis for {len(stock_symbols)} stocks")

    results = {}

    for symbol in stock_symbols:
        try:
            logger.info(f"Analyzing {symbol}...")
            result = await run_6agent_analysis(
                stock_symbol=symbol,
                portfolio_value=portfolio_value,
                risk_per_trade=risk_per_trade
            )
            results[symbol] = result
            logger.info(f"✅ {symbol}: {result.recommendation} ({result.confidence}%)")

        except Exception as e:
            logger.error(f"❌ Failed to analyze {symbol}: {str(e)}")
            results[symbol] = None

    logger.info(f"Batch analysis completed: {len(results)}/{len(stock_symbols)} successful")

    return results


def format_result_for_display(result: TradingWorkflowResult) -> str:
    """
    Format workflow result for console display.

    Args:
        result: TradingWorkflowResult object

    Returns:
        str: Formatted display text
    """
    output = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     6-AGENT TRADING ANALYSIS RESULTS                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 STOCK: {result.symbol}
📅 TIMESTAMP: {result.timestamp}

🎯 FINAL RECOMMENDATION: {result.recommendation}
💯 CONFIDENCE: {result.confidence}%

📋 EXECUTIVE SUMMARY:
{result.summary}

💼 EXECUTION PLAN:
• Entry Price: ${result.execution_plan.get('entry_price', 'N/A')}
• Target Price: ${result.execution_plan.get('target_price', 'N/A')}
• Stop-Loss: ${result.execution_plan.get('stop_loss', 'N/A')}
• Position Size: {result.execution_plan.get('position_size_pct', 'N/A')}% of portfolio
• Timeline: {result.execution_plan.get('timeline', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For full analysis details, see the full_conversation attribute.

╚══════════════════════════════════════════════════════════════════════════════╝
"""
    return output


if __name__ == "__main__":
    # Test the workflow
    async def test():
        print("Testing 6-Agent Trading Analysis Workflow")
        print("=" * 80)

        result = await run_6agent_analysis(
            stock_symbol="AAPL",
            question="Should I buy this stock?",
            portfolio_value=100000.0,
            risk_per_trade=2.0
        )

        print(format_result_for_display(result))

        # Print individual agent outputs
        print("\n📊 INDIVIDUAL AGENT OUTPUTS:")
        print("=" * 80)
        for agent_name, output in result.agent_outputs.items():
            print(f"\n{agent_name}:")
            print("-" * 80)
            print(output[:500] + "..." if len(output) > 500 else output)

    # Run test
    asyncio.run(test())
