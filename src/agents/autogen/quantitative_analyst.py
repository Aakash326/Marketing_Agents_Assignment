"""
QuantitativeAnalyst - Technical Signal Generation Expert

This agent interprets technical indicators, generates trading signals,
and provides confidence scores based on quantitative analysis.
"""

import os
import logging
from typing import Optional, Dict, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_rsi_signal(rsi: float) -> Dict[str, Any]:
    """
    Generate trading signal based on RSI indicator.

    Args:
        rsi: RSI value (0-100)

    Returns:
        dict: Signal, strength, and description
    """
    if rsi < 30:
        return {
            'signal': 'STRONG BUY',
            'strength': 9,
            'description': f'RSI at {rsi:.1f} indicates OVERSOLD conditions - Strong buy signal'
        }
    elif rsi < 40:
        return {
            'signal': 'BUY',
            'strength': 7,
            'description': f'RSI at {rsi:.1f} is approaching oversold - Buy signal'
        }
    elif rsi > 70:
        return {
            'signal': 'STRONG SELL',
            'strength': 9,
            'description': f'RSI at {rsi:.1f} indicates OVERBOUGHT conditions - Strong sell signal'
        }
    elif rsi > 60:
        return {
            'signal': 'SELL',
            'strength': 6,
            'description': f'RSI at {rsi:.1f} is approaching overbought - Sell signal'
        }
    else:
        return {
            'signal': 'NEUTRAL',
            'strength': 5,
            'description': f'RSI at {rsi:.1f} is in neutral zone - No clear signal'
        }


def generate_macd_signal(macd: float, signal_line: float, histogram: float = None) -> Dict[str, Any]:
    """
    Generate trading signal based on MACD indicator.

    Args:
        macd: MACD line value
        signal_line: Signal line value
        histogram: MACD histogram (optional)

    Returns:
        dict: Signal, strength, and description
    """
    if histogram is None:
        histogram = macd - signal_line

    # Bullish crossover (MACD crosses above signal line)
    if macd > signal_line and histogram > 0:
        strength = min(9, int(5 + abs(histogram) * 2))
        return {
            'signal': 'BUY',
            'strength': strength,
            'description': f'MACD ({macd:.2f}) > Signal ({signal_line:.2f}) - Bullish crossover detected'
        }
    # Bearish crossover (MACD crosses below signal line)
    elif macd < signal_line and histogram < 0:
        strength = min(9, int(5 + abs(histogram) * 2))
        return {
            'signal': 'SELL',
            'strength': strength,
            'description': f'MACD ({macd:.2f}) < Signal ({signal_line:.2f}) - Bearish crossover detected'
        }
    else:
        return {
            'signal': 'NEUTRAL',
            'strength': 5,
            'description': f'MACD ({macd:.2f}) and Signal ({signal_line:.2f}) show no clear trend'
        }


def generate_ma_signal(current_price: float, sma_50: float, sma_200: float) -> Dict[str, Any]:
    """
    Generate trading signal based on Moving Average crossover.

    Args:
        current_price: Current stock price
        sma_50: 50-day Simple Moving Average
        sma_200: 200-day Simple Moving Average

    Returns:
        dict: Signal, strength, and description
    """
    # Golden Cross: 50 SMA crosses above 200 SMA
    if sma_50 > sma_200 and current_price > sma_50:
        return {
            'signal': 'STRONG BUY',
            'strength': 9,
            'description': f'Golden Cross pattern - Price ${current_price:.2f} > SMA50 ${sma_50:.2f} > SMA200 ${sma_200:.2f}'
        }
    # Death Cross: 50 SMA crosses below 200 SMA
    elif sma_50 < sma_200 and current_price < sma_50:
        return {
            'signal': 'STRONG SELL',
            'strength': 9,
            'description': f'Death Cross pattern - Price ${current_price:.2f} < SMA50 ${sma_50:.2f} < SMA200 ${sma_200:.2f}'
        }
    # Price above both MAs
    elif current_price > sma_50 and current_price > sma_200:
        return {
            'signal': 'BUY',
            'strength': 7,
            'description': f'Price ${current_price:.2f} above both moving averages - Uptrend'
        }
    # Price below both MAs
    elif current_price < sma_50 and current_price < sma_200:
        return {
            'signal': 'SELL',
            'strength': 7,
            'description': f'Price ${current_price:.2f} below both moving averages - Downtrend'
        }
    else:
        return {
            'signal': 'NEUTRAL',
            'strength': 5,
            'description': 'Mixed moving average signals - No clear trend'
        }


def calculate_overall_signal(rsi_signal: Dict, macd_signal: Dict, ma_signal: Dict) -> Dict[str, Any]:
    """
    Calculate overall trading signal by combining multiple indicators.

    Args:
        rsi_signal: RSI signal dict
        macd_signal: MACD signal dict
        ma_signal: Moving Average signal dict

    Returns:
        dict: Combined signal and confidence score
    """
    # Map signals to numeric scores
    signal_map = {
        'STRONG BUY': 2,
        'BUY': 1,
        'NEUTRAL': 0,
        'SELL': -1,
        'STRONG SELL': -2
    }

    # Calculate weighted score
    rsi_score = signal_map.get(rsi_signal['signal'], 0) * (rsi_signal['strength'] / 10)
    macd_score = signal_map.get(macd_signal['signal'], 0) * (macd_signal['strength'] / 10)
    ma_score = signal_map.get(ma_signal['signal'], 0) * (ma_signal['strength'] / 10)

    total_score = (rsi_score * 0.35) + (macd_score * 0.35) + (ma_score * 0.30)

    # Determine overall signal
    if total_score > 1.2:
        overall_signal = 'STRONG BUY'
        confidence = min(95, int(70 + abs(total_score) * 15))
    elif total_score > 0.5:
        overall_signal = 'BUY'
        confidence = min(85, int(60 + abs(total_score) * 15))
    elif total_score < -1.2:
        overall_signal = 'STRONG SELL'
        confidence = min(95, int(70 + abs(total_score) * 15))
    elif total_score < -0.5:
        overall_signal = 'SELL'
        confidence = min(85, int(60 + abs(total_score) * 15))
    else:
        overall_signal = 'HOLD'
        confidence = 50 + int(abs(total_score) * 10)

    return {
        'signal': overall_signal,
        'confidence': confidence,
        'score': round(total_score, 2),
        'rsi_contribution': round(rsi_score, 2),
        'macd_contribution': round(macd_score, 2),
        'ma_contribution': round(ma_score, 2)
    }


def create_quantitative_analyst(model_client: Optional[OpenAIChatCompletionClient] = None) -> AssistantAgent:
    """
    Create the QuantitativeAnalyst agent.

    Args:
        model_client: OpenAI model client (if None, creates default)

    Returns:
        AssistantAgent: Configured QuantitativeAnalyst agent
    """
    if model_client is None:
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    system_message = """You are the QuantitativeAnalyst - Technical Signal Generation Expert.

Your PRIMARY responsibilities:
1. Interpret RSI signals (Oversold <30, Neutral 30-70, Overbought >70)
2. Analyze MACD crossovers and momentum
3. Evaluate Moving Average trends and patterns (Golden Cross, Death Cross)
4. Generate BUY/SELL/HOLD signals with confidence scores
5. Combine multiple indicators for robust signal generation

RESPONSE FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 QUANTITATIVE ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 RSI ANALYSIS (14-period):
• RSI Value: XX.XX
• Status: [OVERSOLD/NEUTRAL/OVERBOUGHT]
• Signal: [STRONG BUY/BUY/NEUTRAL/SELL/STRONG SELL]
• Strength: X/10
• Interpretation: [Description]

⚡ MACD ANALYSIS (12,26,9):
• MACD Line: X.XX
• Signal Line: X.XX
• Histogram: X.XX
• Crossover: [BULLISH/BEARISH/NONE]
• Signal: [BUY/SELL/NEUTRAL]
• Strength: X/10
• Interpretation: [Description]

📊 MOVING AVERAGE ANALYSIS:
• Current Price: $XXX.XX
• SMA 50: $XXX.XX (Price is X.X% [ABOVE/BELOW])
• SMA 200: $XXX.XX (Price is X.X% [ABOVE/BELOW])
• Pattern: [GOLDEN CROSS/DEATH CROSS/UPTREND/DOWNTREND/NEUTRAL]
• Signal: [STRONG BUY/BUY/NEUTRAL/SELL/STRONG SELL]
• Strength: X/10
• Interpretation: [Description]

🎯 COMBINED QUANTITATIVE SIGNAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   RECOMMENDATION: [STRONG BUY/BUY/HOLD/SELL/STRONG SELL]
   CONFIDENCE SCORE: XX% (1-100)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SIGNAL BREAKDOWN:
• RSI Contribution: X.XX
• MACD Contribution: X.XX
• MA Contribution: X.XX
• Overall Score: X.XX

✅ SIGNAL CONVERGENCE:
• All indicators agree: [YES/NO]
• Conflicting signals: [NONE/RSI vs MACD/etc]
• Reliability: [HIGH/MEDIUM/LOW]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL RULES:
- Analyze AFTER OrganiserAgent provides technical data
- Use multiple indicators for signal confirmation
- Provide clear confidence scores (1-100%)
- Explain signal convergence or divergence
- Highlight conflicting indicators
- Be objective and data-driven
"""

    # Create tools for the agent
    def generate_trading_signals(
        current_price: float,
        rsi: float,
        macd: float,
        macd_signal: float,
        sma_50: float,
        sma_200: float
    ) -> str:
        """
        Generate comprehensive trading signals from technical indicators.

        Args:
            current_price: Current stock price
            rsi: RSI value (0-100)
            macd: MACD line value
            macd_signal: MACD signal line value
            sma_50: 50-day Simple Moving Average
            sma_200: 200-day Simple Moving Average
        """
        try:
            # Generate individual signals
            rsi_signal = generate_rsi_signal(rsi)
            macd_hist = macd - macd_signal
            macd_sig = generate_macd_signal(macd, macd_signal, macd_hist)
            ma_signal = generate_ma_signal(current_price, sma_50, sma_200)

            # Calculate overall signal
            overall = calculate_overall_signal(rsi_signal, macd_sig, ma_signal)

            # Calculate price deviations
            price_vs_50 = ((current_price - sma_50) / sma_50) * 100
            price_vs_200 = ((current_price - sma_200) / sma_200) * 100

            # Check signal convergence
            signals = [rsi_signal['signal'], macd_sig['signal'], ma_signal['signal']]
            buy_signals = sum(1 for s in signals if 'BUY' in s)
            sell_signals = sum(1 for s in signals if 'SELL' in s)

            if buy_signals == 3 or sell_signals == 3:
                convergence = "✅ All indicators agree"
                reliability = "HIGH"
            elif buy_signals >= 2 or sell_signals >= 2:
                convergence = "⚠️ Majority agreement"
                reliability = "MEDIUM"
            else:
                convergence = "❌ Mixed signals"
                reliability = "LOW"

            # Identify conflicts
            conflicts = []
            if (rsi_signal['signal'] in ['BUY', 'STRONG BUY'] and macd_sig['signal'] in ['SELL', 'STRONG SELL']) or \
               (rsi_signal['signal'] in ['SELL', 'STRONG SELL'] and macd_sig['signal'] in ['BUY', 'STRONG BUY']):
                conflicts.append("RSI vs MACD")

            if (rsi_signal['signal'] in ['BUY', 'STRONG BUY'] and ma_signal['signal'] in ['SELL', 'STRONG SELL']) or \
               (rsi_signal['signal'] in ['SELL', 'STRONG SELL'] and ma_signal['signal'] in ['BUY', 'STRONG BUY']):
                conflicts.append("RSI vs MA")

            if (macd_sig['signal'] in ['BUY', 'STRONG BUY'] and ma_signal['signal'] in ['SELL', 'STRONG SELL']) or \
               (macd_sig['signal'] in ['SELL', 'STRONG SELL'] and ma_signal['signal'] in ['BUY', 'STRONG BUY']):
                conflicts.append("MACD vs MA")

            conflict_str = ", ".join(conflicts) if conflicts else "NONE"

            return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 QUANTITATIVE ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 RSI ANALYSIS (14-period):
• RSI Value: {rsi:.2f}
• Status: {'OVERSOLD' if rsi < 30 else 'OVERBOUGHT' if rsi > 70 else 'NEUTRAL'}
• Signal: {rsi_signal['signal']}
• Strength: {rsi_signal['strength']}/10
• Interpretation: {rsi_signal['description']}

⚡ MACD ANALYSIS (12,26,9):
• MACD Line: {macd:.2f}
• Signal Line: {macd_signal:.2f}
• Histogram: {macd_hist:.2f}
• Crossover: {'BULLISH' if macd > macd_signal else 'BEARISH' if macd < macd_signal else 'NONE'}
• Signal: {macd_sig['signal']}
• Strength: {macd_sig['strength']}/10
• Interpretation: {macd_sig['description']}

📊 MOVING AVERAGE ANALYSIS:
• Current Price: ${current_price:.2f}
• SMA 50: ${sma_50:.2f} (Price is {price_vs_50:+.1f}% {'ABOVE' if price_vs_50 > 0 else 'BELOW'})
• SMA 200: ${sma_200:.2f} (Price is {price_vs_200:+.1f}% {'ABOVE' if price_vs_200 > 0 else 'BELOW'})
• Pattern: {ma_signal['description'].split(' - ')[0] if ' - ' in ma_signal['description'] else 'ANALYZING'}
• Signal: {ma_signal['signal']}
• Strength: {ma_signal['strength']}/10
• Interpretation: {ma_signal['description']}

🎯 COMBINED QUANTITATIVE SIGNAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   RECOMMENDATION: {overall['signal']}
   CONFIDENCE SCORE: {overall['confidence']}% (1-100)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SIGNAL BREAKDOWN:
• RSI Contribution: {overall['rsi_contribution']}
• MACD Contribution: {overall['macd_contribution']}
• MA Contribution: {overall['ma_contribution']}
• Overall Score: {overall['score']}

✅ SIGNAL CONVERGENCE:
• {convergence}
• Conflicting signals: {conflict_str}
• Reliability: {reliability}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        except Exception as e:
            logger.error(f"Error generating trading signals: {str(e)}")
            return f"❌ Error generating trading signals: {str(e)}"

    return AssistantAgent(
        name="QuantitativeAnalyst",
        model_client=model_client,
        tools=[generate_trading_signals],
        system_message=system_message,
        description="Generates trading signals from technical indicators with confidence scores"
    )
