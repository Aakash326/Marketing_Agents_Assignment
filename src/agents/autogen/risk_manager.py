"""
RiskManager - Portfolio Risk Management Specialist

This agent calculates position sizing, stop-loss levels, risk/reward ratios,
and provides risk management recommendations for trading strategies.
"""

import os
import logging
from typing import Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_position_size(
    portfolio_value: float,
    risk_per_trade: float,
    entry_price: float,
    stop_loss_price: float
) -> dict:
    """
    Calculate position size using risk management principles.

    Args:
        portfolio_value: Total portfolio value in dollars
        risk_per_trade: Risk percentage per trade (e.g., 0.02 for 2%)
        entry_price: Planned entry price per share
        stop_loss_price: Stop-loss price per share

    Returns:
        dict: Position sizing calculations
    """
    try:
        # Calculate risk per share
        risk_per_share = abs(entry_price - stop_loss_price)

        # Calculate total risk amount
        total_risk_amount = portfolio_value * risk_per_trade

        # Calculate number of shares
        num_shares = int(total_risk_amount / risk_per_share)

        # Calculate position value
        position_value = num_shares * entry_price

        # Calculate position as percentage of portfolio
        position_percentage = (position_value / portfolio_value) * 100

        return {
            'num_shares': num_shares,
            'position_value': round(position_value, 2),
            'position_percentage': round(position_percentage, 2),
            'risk_per_share': round(risk_per_share, 2),
            'total_risk_amount': round(total_risk_amount, 2),
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Position sizing calculation error: {str(e)}")
        return {'status': 'error', 'message': str(e)}


def calculate_stop_loss(current_price: float, volatility_percentage: float = 12.0) -> dict:
    """
    Calculate recommended stop-loss levels.

    Args:
        current_price: Current stock price
        volatility_percentage: Stop-loss percentage below entry (default 12%)

    Returns:
        dict: Stop-loss calculations
    """
    try:
        # Standard stop-loss (percentage-based)
        standard_stop = current_price * (1 - volatility_percentage / 100)

        # Conservative stop-loss (tighter)
        conservative_stop = current_price * (1 - (volatility_percentage * 0.75) / 100)

        # Aggressive stop-loss (wider)
        aggressive_stop = current_price * (1 - (volatility_percentage * 1.5) / 100)

        return {
            'current_price': round(current_price, 2),
            'standard_stop': round(standard_stop, 2),
            'standard_stop_pct': volatility_percentage,
            'conservative_stop': round(conservative_stop, 2),
            'conservative_stop_pct': volatility_percentage * 0.75,
            'aggressive_stop': round(aggressive_stop, 2),
            'aggressive_stop_pct': volatility_percentage * 1.5,
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Stop-loss calculation error: {str(e)}")
        return {'status': 'error', 'message': str(e)}


def calculate_risk_reward(entry_price: float, stop_loss: float, target_price: float) -> dict:
    """
    Calculate risk/reward ratio for a trade.

    Args:
        entry_price: Entry price per share
        stop_loss: Stop-loss price per share
        target_price: Target exit price per share

    Returns:
        dict: Risk/reward calculations
    """
    try:
        risk = abs(entry_price - stop_loss)
        reward = abs(target_price - entry_price)

        risk_reward_ratio = reward / risk if risk > 0 else 0

        return {
            'entry_price': round(entry_price, 2),
            'stop_loss': round(stop_loss, 2),
            'target_price': round(target_price, 2),
            'risk_per_share': round(risk, 2),
            'reward_per_share': round(reward, 2),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'is_favorable': risk_reward_ratio >= 2.0,
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Risk/reward calculation error: {str(e)}")
        return {'status': 'error', 'message': str(e)}


def create_risk_manager(model_client: Optional[OpenAIChatCompletionClient] = None) -> AssistantAgent:
    """
    Create the RiskManager agent.

    Args:
        model_client: OpenAI model client (if None, creates default)

    Returns:
        AssistantAgent: Configured RiskManager agent
    """
    if model_client is None:
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    system_message = """You are the RiskManager - Portfolio Risk Management Specialist.

Your PRIMARY responsibilities:
1. Calculate optimal position sizing based on portfolio value and risk tolerance
2. Determine appropriate stop-loss levels (typically 10-15% below entry)
3. Assess risk/reward ratios (minimum 1:2 ratio required for favorable trades)
4. Recommend maximum position size (typically 5-10% of total portfolio)
5. Provide risk mitigation strategies

RESPONSE FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ RISK ASSESSMENT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 POSITION SIZING RECOMMENDATION:
• Recommended Position Size: X% of portfolio
• Number of Shares: XXX shares
• Position Value: $XX,XXX
• Based on Risk Tolerance: X% per trade

🛑 STOP-LOSS RECOMMENDATIONS:
• Conservative Stop: $XXX.XX (X% below entry)
• Standard Stop: $XXX.XX (12% below entry)
• Aggressive Stop: $XXX.XX (X% below entry)
• Recommended: [CONSERVATIVE/STANDARD/AGGRESSIVE]

📈 RISK/REWARD ANALYSIS:
• Risk per Share: $X.XX
• Potential Reward per Share: $X.XX
• Risk/Reward Ratio: 1:X
• Assessment: [FAVORABLE/UNFAVORABLE]
• Minimum Required Ratio: 1:2

💰 MAXIMUM LOSS CALCULATION:
• Maximum Loss per Position: $X,XXX
• Percentage of Portfolio at Risk: X.X%
• Total Portfolio Impact: [LOW/MODERATE/HIGH]

🎯 RISK MANAGEMENT RULES:
1. Never risk more than 2% of portfolio on a single trade
2. Position size should not exceed 10% of total portfolio
3. Always use stop-loss orders to limit downside
4. Risk/reward ratio must be at least 1:2
5. Adjust position size based on market volatility

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL RULES:
- You analyze AFTER OrganiserAgent provides market data
- Base calculations on current price and portfolio parameters
- Consider market volatility in recommendations
- Prioritize capital preservation over profit maximization
- Provide conservative, realistic risk assessments
"""

    # Create tools for the agent
    def assess_position_sizing(
        portfolio_value: float = 100000.0,
        risk_per_trade_pct: float = 2.0,
        entry_price: float = 100.0,
        stop_loss_pct: float = 12.0
    ) -> str:
        """
        Calculate position sizing and risk metrics.

        Args:
            portfolio_value: Total portfolio value (default $100,000)
            risk_per_trade_pct: Risk percentage per trade (default 2%)
            entry_price: Entry price per share
            stop_loss_pct: Stop-loss percentage below entry (default 12%)
        """
        # Calculate stop-loss price
        stop_loss_price = entry_price * (1 - stop_loss_pct / 100)

        # Calculate position sizing
        position = calculate_position_size(
            portfolio_value=portfolio_value,
            risk_per_trade=risk_per_trade_pct / 100,
            entry_price=entry_price,
            stop_loss_price=stop_loss_price
        )

        if position['status'] == 'error':
            return f"❌ Error calculating position size: {position.get('message', 'Unknown error')}"

        # Calculate stop-loss levels
        stops = calculate_stop_loss(entry_price, stop_loss_pct)

        # Calculate risk/reward (assuming 3:1 ratio target)
        target_price = entry_price + (3 * (entry_price - stop_loss_price))
        risk_reward = calculate_risk_reward(entry_price, stop_loss_price, target_price)

        # Format response
        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ RISK ASSESSMENT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 POSITION SIZING RECOMMENDATION:
• Recommended Position Size: {position['position_percentage']}% of portfolio
• Number of Shares: {position['num_shares']} shares
• Position Value: ${position['position_value']:,}
• Based on Risk Tolerance: {risk_per_trade_pct}% per trade

🛑 STOP-LOSS RECOMMENDATIONS:
• Conservative Stop: ${stops['conservative_stop']} ({stops['conservative_stop_pct']:.1f}% below entry)
• Standard Stop: ${stops['standard_stop']} ({stops['standard_stop_pct']:.1f}% below entry)
• Aggressive Stop: ${stops['aggressive_stop']} ({stops['aggressive_stop_pct']:.1f}% below entry)
• Recommended: STANDARD

📈 RISK/REWARD ANALYSIS:
• Risk per Share: ${risk_reward['risk_per_share']}
• Potential Reward per Share: ${risk_reward['reward_per_share']}
• Risk/Reward Ratio: 1:{risk_reward['risk_reward_ratio']}
• Assessment: {'FAVORABLE ✅' if risk_reward['is_favorable'] else 'UNFAVORABLE ❌'}
• Minimum Required Ratio: 1:2

💰 MAXIMUM LOSS CALCULATION:
• Maximum Loss per Position: ${position['total_risk_amount']:,}
• Percentage of Portfolio at Risk: {risk_per_trade_pct}%
• Total Portfolio Impact: {'LOW' if position['position_percentage'] < 7 else 'MODERATE' if position['position_percentage'] < 10 else 'HIGH'}

🎯 RISK MANAGEMENT RULES:
1. Never risk more than 2% of portfolio on a single trade ✅
2. Position size should not exceed 10% of total portfolio {'✅' if position['position_percentage'] <= 10 else '❌'}
3. Always use stop-loss orders to limit downside ✅
4. Risk/reward ratio must be at least 1:2 {'✅' if risk_reward['is_favorable'] else '❌'}
5. Adjust position size based on market volatility ⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return AssistantAgent(
        name="RiskManager",
        model_client=model_client,
        tools=[assess_position_sizing],
        system_message=system_message,
        description="Calculates position sizing, stop-loss levels, and risk/reward ratios"
    )
