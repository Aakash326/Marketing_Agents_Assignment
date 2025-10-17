"""
StrategyDeveloper - Execution Strategy & Timing Specialist

This agent determines optimal entry/exit prices, investment timeline,
and creates detailed execution plans for trading strategies.
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_fibonacci_levels(current_price: float, high_52w: float, low_52w: float) -> Dict[str, float]:
    """
    Calculate Fibonacci retracement and extension levels.

    Args:
        current_price: Current stock price
        high_52w: 52-week high
        low_52w: 52-week low

    Returns:
        dict: Fibonacci support and resistance levels
    """
    price_range = high_52w - low_52w

    # Retracement levels (support)
    fib_236 = high_52w - (price_range * 0.236)
    fib_382 = high_52w - (price_range * 0.382)
    fib_500 = high_52w - (price_range * 0.500)
    fib_618 = high_52w - (price_range * 0.618)

    # Extension levels (resistance/targets)
    fib_1272 = high_52w + (price_range * 0.272)
    fib_1618 = high_52w + (price_range * 0.618)

    return {
        'support_236': round(fib_236, 2),
        'support_382': round(fib_382, 2),
        'support_500': round(fib_500, 2),
        'support_618': round(fib_618, 2),
        'resistance_current': round(high_52w, 2),
        'target_1272': round(fib_1272, 2),
        'target_1618': round(fib_1618, 2)
    }


def determine_entry_strategy(
    current_price: float,
    trend: str,
    rsi: float,
    support_level: float
) -> Dict[str, Any]:
    """
    Determine optimal entry price and strategy.

    Args:
        current_price: Current stock price
        trend: Overall market trend (BULLISH/BEARISH/NEUTRAL)
        rsi: RSI value
        support_level: Key support level

    Returns:
        dict: Entry strategy details
    """
    # Adjust entry based on trend and RSI
    if trend == "BULLISH" and rsi < 50:
        # Buy on dip in uptrend
        entry_price = current_price * 0.98  # 2% below current
        timing = "IMMEDIATE - BUY ON DIP"
        confidence = 85
    elif trend == "BULLISH" and rsi < 70:
        # Buy at current price in uptrend
        entry_price = current_price
        timing = "IMMEDIATE - MOMENTUM BUY"
        confidence = 80
    elif trend == "NEUTRAL" and rsi < 45:
        # Wait for better support
        entry_price = min(current_price * 0.95, support_level)
        timing = "WAIT FOR PULLBACK TO SUPPORT"
        confidence = 70
    elif trend == "BEARISH":
        # Wait for trend reversal
        entry_price = support_level
        timing = "WAIT FOR TREND REVERSAL"
        confidence = 50
    else:
        # Default conservative approach
        entry_price = current_price * 0.97
        timing = "MODERATE - WAIT FOR SMALL PULLBACK"
        confidence = 65

    return {
        'entry_price': round(entry_price, 2),
        'timing': timing,
        'confidence': confidence,
        'discount': round(((current_price - entry_price) / current_price) * 100, 1)
    }


def determine_exit_strategy(
    entry_price: float,
    resistance_level: float,
    target_fibonacci: float,
    analyst_target: Optional[float] = None
) -> Dict[str, Any]:
    """
    Determine target exit prices and strategy.

    Args:
        entry_price: Planned entry price
        resistance_level: Key resistance level
        target_fibonacci: Fibonacci extension target
        analyst_target: Average analyst price target (optional)

    Returns:
        dict: Exit strategy with multiple targets
    """
    # Calculate multiple profit targets
    conservative_target = entry_price * 1.10  # 10% gain
    moderate_target = entry_price * 1.20  # 20% gain
    aggressive_target = max(resistance_level, target_fibonacci)

    # If analyst target available, incorporate it
    if analyst_target and analyst_target > entry_price:
        moderate_target = (moderate_target + analyst_target) / 2

    return {
        'target_1_conservative': round(conservative_target, 2),
        'target_1_gain': 10.0,
        'target_2_moderate': round(moderate_target, 2),
        'target_2_gain': round(((moderate_target - entry_price) / entry_price) * 100, 1),
        'target_3_aggressive': round(aggressive_target, 2),
        'target_3_gain': round(((aggressive_target - entry_price) / entry_price) * 100, 1),
        'recommended_target': round(moderate_target, 2)
    }


def determine_timeline(signal_strength: int, trend: str, volatility: str = "MODERATE") -> Dict[str, Any]:
    """
    Determine investment timeline based on signals and market conditions.

    Args:
        signal_strength: Signal confidence (1-10)
        trend: Market trend
        volatility: Market volatility level

    Returns:
        dict: Timeline strategy
    """
    if signal_strength >= 8 and trend == "BULLISH":
        return {
            'timeline': 'SHORT-TERM',
            'duration': '2-6 weeks',
            'description': 'Strong momentum play - Quick gains expected',
            'review_frequency': 'Daily'
        }
    elif signal_strength >= 6 and trend == "BULLISH":
        return {
            'timeline': 'MEDIUM-TERM',
            'duration': '2-4 months',
            'description': 'Solid uptrend - Hold for sustained gains',
            'review_frequency': 'Weekly'
        }
    elif signal_strength >= 5:
        return {
            'timeline': 'MEDIUM-TERM',
            'duration': '3-6 months',
            'description': 'Moderate signals - Patient approach recommended',
            'review_frequency': 'Weekly'
        }
    else:
        return {
            'timeline': 'LONG-TERM',
            'duration': '6-12 months',
            'description': 'Weak signals - Value play with longer horizon',
            'review_frequency': 'Monthly'
        }


def create_strategy_developer(model_client: Optional[OpenAIChatCompletionClient] = None) -> AssistantAgent:
    """
    Create the StrategyDeveloper agent.

    Args:
        model_client: OpenAI model client (if None, creates default)

    Returns:
        AssistantAgent: Configured StrategyDeveloper agent
    """
    if model_client is None:
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    system_message = """You are the StrategyDeveloper - Execution Strategy & Timing Specialist.

Your PRIMARY responsibilities:
1. Determine optimal entry price based on support levels, trend, and momentum
2. Set multiple target exit prices (conservative, moderate, aggressive)
3. Define investment timeline (short-term, medium-term, long-term)
4. Create step-by-step execution plan with specific actions
5. Incorporate Fibonacci levels and technical support/resistance

RESPONSE FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 EXECUTION STRATEGY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 ENTRY STRATEGY:
• Recommended Entry Price: $XXX.XX
• Current Price: $XXX.XX (Discount: X.X%)
• Timing: [IMMEDIATE/WAIT FOR PULLBACK/WAIT FOR REVERSAL]
• Entry Confidence: XX%
• Entry Method: [MARKET ORDER/LIMIT ORDER]
• Support Level: $XXX.XX
• Key Level to Watch: $XXX.XX

🎯 EXIT STRATEGY (Multi-Target Approach):
• Target 1 (Conservative): $XXX.XX (+10% gain)
  ↳ Sell 33% of position
• Target 2 (Moderate): $XXX.XX (+XX% gain)
  ↳ Sell 50% of remaining position
• Target 3 (Aggressive): $XXX.XX (+XX% gain)
  ↳ Sell remaining position or trail stop
• Recommended Primary Target: $XXX.XX

🛑 STOP-LOSS & RISK MANAGEMENT:
• Initial Stop-Loss: $XXX.XX (-XX% from entry)
• Break-Even Stop: Move to $XXX.XX after +5% gain
• Trailing Stop: Activate at +15%, trail by 8%

⏰ INVESTMENT TIMELINE:
• Strategy Type: [SHORT-TERM/MEDIUM-TERM/LONG-TERM]
• Expected Duration: X-X weeks/months
• Review Frequency: [DAILY/WEEKLY/MONTHLY]
• Rationale: [Description]

📊 FIBONACCI LEVELS:
• Support Levels: $XXX.XX (38.2%), $XXX.XX (50%), $XXX.XX (61.8%)
• Resistance Levels: $XXX.XX (current high)
• Extension Targets: $XXX.XX (127.2%), $XXX.XX (161.8%)

📋 STEP-BY-STEP EXECUTION PLAN:
1. [First action with specific price/condition]
2. [Second action with specific price/condition]
3. [Third action with specific price/condition]
4. [Fourth action - ongoing monitoring]
5. [Fifth action - exit criteria]

⚠️ KEY CONDITIONS TO MONITOR:
• [Condition 1 that would change strategy]
• [Condition 2 that would trigger early exit]
• [Condition 3 that would invalidate thesis]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL RULES:
- Analyze AFTER all previous agents provide their insights
- Base strategy on combined technical + fundamental analysis
- Provide SPECIFIC prices and dates, not vague ranges
- Include risk management at every step
- Create actionable, clear execution steps
- Consider both best-case and worst-case scenarios
"""

    # Create tools for the agent
    def develop_execution_strategy(
        current_price: float,
        trend: str,
        rsi: float,
        high_52w: float,
        low_52w: float,
        support_level: float = None,
        analyst_target: float = None,
        signal_confidence: int = 7
    ) -> str:
        """
        Develop comprehensive execution strategy with entry, exit, and timeline.

        Args:
            current_price: Current stock price
            trend: Market trend (BULLISH/BEARISH/NEUTRAL)
            rsi: RSI value
            high_52w: 52-week high
            low_52w: 52-week low
            support_level: Key support level (optional)
            analyst_target: Average analyst price target (optional)
            signal_confidence: Signal confidence score 1-10 (default 7)
        """
        try:
            # Calculate Fibonacci levels
            fib_levels = calculate_fibonacci_levels(current_price, high_52w, low_52w)

            # Determine support level if not provided
            if support_level is None:
                support_level = fib_levels['support_382']

            # Determine entry strategy
            entry = determine_entry_strategy(current_price, trend, rsi, support_level)

            # Determine exit strategy
            exit_strategy = determine_exit_strategy(
                entry['entry_price'],
                fib_levels['resistance_current'],
                fib_levels['target_1272'],
                analyst_target
            )

            # Determine timeline
            timeline = determine_timeline(signal_confidence, trend)

            # Calculate stop-loss
            stop_loss = entry['entry_price'] * 0.88  # 12% below entry
            break_even_stop = entry['entry_price'] * 1.00

            # Create execution plan based on timing
            if entry['timing'].startswith("IMMEDIATE"):
                step1 = f"Place limit order at ${entry['entry_price']} (valid for 3 days)"
                step2 = f"If filled, immediately set stop-loss at ${stop_loss:.2f}"
            else:
                step1 = f"Set price alert for ${entry['entry_price']}"
                step2 = f"Monitor daily for entry signal confirmation"

            # Determine entry method
            entry_method = "LIMIT ORDER" if entry['discount'] > 1 else "MARKET ORDER"

            # Format execution plan
            return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 EXECUTION STRATEGY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 ENTRY STRATEGY:
• Recommended Entry Price: ${entry['entry_price']}
• Current Price: ${current_price:.2f} (Discount: {entry['discount']}%)
• Timing: {entry['timing']}
• Entry Confidence: {entry['confidence']}%
• Entry Method: {entry_method}
• Support Level: ${support_level:.2f}
• Key Level to Watch: ${fib_levels['support_382']}

🎯 EXIT STRATEGY (Multi-Target Approach):
• Target 1 (Conservative): ${exit_strategy['target_1_conservative']} (+{exit_strategy['target_1_gain']:.1f}% gain)
  ↳ Sell 33% of position - Lock in quick profits
• Target 2 (Moderate): ${exit_strategy['target_2_moderate']} (+{exit_strategy['target_2_gain']:.1f}% gain)
  ↳ Sell 50% of remaining position - Main profit target
• Target 3 (Aggressive): ${exit_strategy['target_3_aggressive']} (+{exit_strategy['target_3_gain']:.1f}% gain)
  ↳ Sell remaining position or activate trailing stop
• Recommended Primary Target: ${exit_strategy['recommended_target']}

🛑 STOP-LOSS & RISK MANAGEMENT:
• Initial Stop-Loss: ${stop_loss:.2f} (-12% from entry)
• Break-Even Stop: Move to ${break_even_stop:.2f} after +5% gain
• Trailing Stop: Activate at +15% gain, trail by 8%
• Max Loss per Position: Follow RiskManager recommendations

⏰ INVESTMENT TIMELINE:
• Strategy Type: {timeline['timeline']}
• Expected Duration: {timeline['duration']}
• Review Frequency: {timeline['review_frequency']}
• Rationale: {timeline['description']}

📊 FIBONACCI LEVELS:
• Support Levels: ${fib_levels['support_382']} (38.2%), ${fib_levels['support_500']} (50%), ${fib_levels['support_618']} (61.8%)
• Resistance Levels: ${fib_levels['resistance_current']} (52-week high)
• Extension Targets: ${fib_levels['target_1272']} (127.2%), ${fib_levels['target_1618']} (161.8%)

📋 STEP-BY-STEP EXECUTION PLAN:
1. {step1}
2. {step2}
3. Set profit targets at ${exit_strategy['target_1_conservative']}, ${exit_strategy['target_2_moderate']}, and ${exit_strategy['target_3_aggressive']}
4. Monitor {timeline['review_frequency'].lower()} for trend changes and adjust stops accordingly
5. Exit fully if price breaks below ${stop_loss:.2f} or trend changes to BEARISH

⚠️ KEY CONDITIONS TO MONITOR:
• If RSI exceeds 80, consider taking partial profits early
• If price breaks below ${fib_levels['support_618']}, re-evaluate bullish thesis
• If major negative news emerges, exit immediately regardless of technicals
• Monitor volume - declining volume on rallies is bearish divergence

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        except Exception as e:
            logger.error(f"Error developing execution strategy: {str(e)}")
            return f"❌ Error developing execution strategy: {str(e)}"

    return AssistantAgent(
        name="StrategyDeveloper",
        model_client=model_client,
        tools=[develop_execution_strategy],
        system_message=system_message,
        description="Creates detailed execution strategies with entry, exit, and timeline planning"
    )
