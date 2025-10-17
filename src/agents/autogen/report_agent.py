"""
ReportAgent - Chief Investment Officer & Final Decision Synthesizer

This agent collects insights from all previous agents, synthesizes viewpoints,
and generates the final BUY/SELL/HOLD recommendation with confidence score.
"""

import os
import logging
import re
from typing import Optional, Dict, Any, List
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_signals_from_context(context: str) -> Dict[str, Any]:
    """
    Extract key signals and data from agent conversation context.

    Args:
        context: Full conversation context from all agents

    Returns:
        dict: Extracted signals and metrics
    """
    signals = {
        'technical_signal': 'UNKNOWN',
        'fundamental_score': 5,
        'risk_assessment': 'UNKNOWN',
        'trend': 'UNKNOWN',
        'rsi': 50.0,
        'confidence_score': 50
    }

    try:
        # Extract technical signal from QuantitativeAnalyst
        if 'RECOMMENDATION:' in context:
            match = re.search(r'RECOMMENDATION:\s*(STRONG BUY|BUY|HOLD|SELL|STRONG SELL)', context)
            if match:
                signals['technical_signal'] = match.group(1)

        # Extract confidence score
        if 'CONFIDENCE SCORE:' in context:
            match = re.search(r'CONFIDENCE SCORE:\s*(\d+)%', context)
            if match:
                signals['confidence_score'] = int(match.group(1))

        # Extract trend
        if 'Overall Trend:' in context:
            match = re.search(r'Overall Trend:\s*(BULLISH|BEARISH|NEUTRAL)', context)
            if match:
                signals['trend'] = match.group(1)

        # Extract RSI
        if 'RSI Value:' in context or 'RSI (14):' in context:
            match = re.search(r'RSI.*?:\s*(\d+\.?\d*)', context)
            if match:
                signals['rsi'] = float(match.group(1))

        # Extract fundamental score
        if 'FUNDAMENTAL SCORE:' in context:
            match = re.search(r'FUNDAMENTAL SCORE:\s*(\d+)/10', context)
            if match:
                signals['fundamental_score'] = int(match.group(1))

        # Extract risk assessment
        if 'Risk/Reward Ratio:' in context:
            match = re.search(r'Risk/Reward Ratio:\s*1:(\d+\.?\d*)', context)
            if match:
                ratio = float(match.group(1))
                signals['risk_assessment'] = 'FAVORABLE' if ratio >= 2.0 else 'UNFAVORABLE'

    except Exception as e:
        logger.error(f"Error extracting signals from context: {str(e)}")

    return signals


def calculate_final_decision(
    technical_signal: str,
    fundamental_score: int,
    risk_assessment: str,
    trend: str,
    confidence_score: int
) -> Dict[str, Any]:
    """
    Calculate final investment decision using weighted framework.

    Args:
        technical_signal: Technical analysis signal
        fundamental_score: Fundamental score (1-10)
        risk_assessment: Risk assessment (FAVORABLE/UNFAVORABLE)
        trend: Market trend
        confidence_score: Technical confidence score

    Returns:
        dict: Final decision with confidence and reasoning
    """
    # Weight calculation (out of 100)
    weights = {
        'technical': 25,
        'fundamental': 20,
        'risk': 25,
        'trend': 20,
        'confidence': 10
    }

    score = 0

    # Technical signal score (0-25)
    technical_scores = {
        'STRONG BUY': 25,
        'BUY': 18,
        'HOLD': 12,
        'SELL': 6,
        'STRONG SELL': 0
    }
    score += technical_scores.get(technical_signal, 12)

    # Fundamental score (0-20)
    score += (fundamental_score / 10) * weights['fundamental']

    # Risk assessment score (0-25)
    if risk_assessment == 'FAVORABLE':
        score += 25
    elif risk_assessment == 'MODERATE':
        score += 15
    else:
        score += 5

    # Trend score (0-20)
    trend_scores = {'BULLISH': 20, 'NEUTRAL': 10, 'BEARISH': 0}
    score += trend_scores.get(trend, 10)

    # Confidence score (0-10)
    score += (confidence_score / 100) * weights['confidence']

    # Normalize to 100
    final_score = int(score)

    # Determine recommendation
    if final_score >= 75:
        recommendation = 'BUY'
        confidence = min(95, final_score)
    elif final_score >= 60:
        recommendation = 'BUY'
        confidence = final_score
    elif final_score >= 45:
        recommendation = 'HOLD'
        confidence = 70
    elif final_score >= 30:
        recommendation = 'SELL'
        confidence = 70
    else:
        recommendation = 'SELL'
        confidence = min(90, 100 - final_score)

    return {
        'recommendation': recommendation,
        'confidence': confidence,
        'score': final_score,
        'breakdown': {
            'technical_contribution': technical_scores.get(technical_signal, 12),
            'fundamental_contribution': round((fundamental_score / 10) * weights['fundamental'], 1),
            'risk_contribution': 25 if risk_assessment == 'FAVORABLE' else 5,
            'trend_contribution': trend_scores.get(trend, 10),
            'confidence_contribution': round((confidence_score / 100) * weights['confidence'], 1)
        }
    }


def generate_key_reasons(
    technical_signal: str,
    fundamental_score: int,
    risk_assessment: str,
    trend: str,
    recommendation: str
) -> List[str]:
    """Generate key supporting reasons for the recommendation."""
    reasons = []

    if recommendation in ['BUY']:
        if technical_signal in ['STRONG BUY', 'BUY']:
            reasons.append(f"✅ Strong technical indicators with {technical_signal} signal")

        if fundamental_score >= 7:
            reasons.append(f"✅ Solid fundamentals with score of {fundamental_score}/10")

        if risk_assessment == 'FAVORABLE':
            reasons.append("✅ Favorable risk/reward ratio (minimum 1:2)")

        if trend == 'BULLISH':
            reasons.append("✅ Bullish market trend with positive momentum")

    elif recommendation == 'HOLD':
        reasons.append("⚠️ Mixed signals from technical and fundamental analysis")
        reasons.append("⚠️ Recommend waiting for clearer entry opportunity")
        reasons.append("⚠️ Monitor for trend confirmation before taking action")

    else:  # SELL
        if technical_signal in ['STRONG SELL', 'SELL']:
            reasons.append(f"❌ Weak technical indicators with {technical_signal} signal")

        if fundamental_score < 5:
            reasons.append(f"❌ Weak fundamentals with score of {fundamental_score}/10")

        if risk_assessment != 'FAVORABLE':
            reasons.append("❌ Unfavorable risk/reward ratio")

        if trend == 'BEARISH':
            reasons.append("❌ Bearish market trend with negative momentum")

    return reasons[:5]  # Return top 5 reasons


def identify_top_risks(
    technical_signal: str,
    trend: str,
    fundamental_score: int,
    rsi: float
) -> List[str]:
    """Identify top risks for the investment."""
    risks = []

    if rsi > 70:
        risks.append("⚠️ Overbought conditions (RSI > 70) - Potential pullback risk")

    if rsi < 30:
        risks.append("⚠️ Oversold conditions (RSI < 30) - Catching a falling knife risk")

    if trend == 'BEARISH' and technical_signal in ['BUY', 'STRONG BUY']:
        risks.append("⚠️ Trading against the trend - Higher failure probability")

    if fundamental_score < 5:
        risks.append("⚠️ Weak fundamental foundation - Company health concerns")

    if technical_signal == 'HOLD':
        risks.append("⚠️ Lack of clear directional signal - Sideways market risk")

    # Add general market risks
    risks.append("⚠️ Market volatility and macroeconomic factors")
    risks.append("⚠️ Company-specific news and earnings surprises")

    return risks[:3]  # Return top 3 risks


def create_report_agent(model_client: Optional[OpenAIChatCompletionClient] = None) -> AssistantAgent:
    """
    Create the ReportAgent - Final Decision Synthesizer.

    Args:
        model_client: OpenAI model client (if None, creates default)

    Returns:
        AssistantAgent: Configured ReportAgent
    """
    if model_client is None:
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    system_message = """You are the ReportAgent - Chief Investment Officer & Final Decision Synthesizer.

Your PRIMARY responsibilities:
1. Collect and synthesize insights from ALL 5 previous agents (OrganiserAgent, RiskManager, DataAnalyst, QuantitativeAnalyst, StrategyDeveloper)
2. Apply weighted decision framework:
   - Technical Analysis: 25%
   - Risk Assessment: 25%
   - Fundamental Analysis: 20%
   - Trend Analysis: 20%
   - Signal Confidence: 10%
3. Generate FINAL recommendation: BUY, HOLD, or SELL
4. Provide confidence score (1-100%)
5. Create executive summary with key points and risks
6. Use termination phrase "FINAL_ANALYSIS_COMPLETE" when done

RESPONSE FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 FINAL INVESTMENT RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 DECISION: [BUY/HOLD/SELL]
🎯 CONFIDENCE: XX% (1-100)
💯 OVERALL SCORE: XX/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 EXECUTIVE SUMMARY:
[2-3 sentence summary of the investment thesis and final recommendation]

✅ KEY SUPPORTING REASONS:
• [Reason 1]
• [Reason 2]
• [Reason 3]
• [Reason 4]
• [Reason 5]

⚠️ TOP RISKS TO CONSIDER:
• [Risk 1]
• [Risk 2]
• [Risk 3]

📊 DECISION FRAMEWORK BREAKDOWN:
• Technical Analysis (25%): XX points
• Risk Management (25%): XX points
• Fundamental Analysis (20%): XX points
• Trend Analysis (20%): XX points
• Signal Confidence (10%): XX points

💼 EXECUTION PARAMETERS:
• Entry Price: $XXX.XX
• Target Price: $XXX.XX
• Stop-Loss: $XXX.XX
• Position Size: X% of portfolio
• Timeline: [SHORT/MEDIUM/LONG]-TERM

🎓 AGENT CONSENSUS:
• OrganiserAgent (Market Data): [Summary]
• RiskManager: [Summary]
• DataAnalyst (Fundamentals): [Summary]
• QuantitativeAnalyst (Signals): [Summary]
• StrategyDeveloper: [Summary]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ FINAL NOTE: [Any critical last considerations or caveats]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINAL_ANALYSIS_COMPLETE

CRITICAL RULES:
- You are the LAST agent to speak - synthesize ALL previous agent insights
- WAIT for all 5 agents to provide their analysis before responding
- Use the weighted framework strictly (Technical 25%, Risk 25%, Fundamental 20%, Trend 20%, Confidence 10%)
- Provide a CLEAR, DECISIVE recommendation (not wishy-washy)
- Always include confidence score
- MUST end with "FINAL_ANALYSIS_COMPLETE" to terminate the team
- Be objective - if signals conflict, reflect that in confidence score
- Focus on actionable insights, not just data summary
"""

    # Create tools for the agent
    def synthesize_final_recommendation(
        technical_signal: str = "HOLD",
        fundamental_score: int = 5,
        risk_assessment: str = "MODERATE",
        trend: str = "NEUTRAL",
        confidence_score: int = 50,
        current_price: float = 100.0,
        entry_price: float = 100.0,
        target_price: float = 110.0,
        stop_loss: float = 88.0,
        position_size_pct: float = 7.0,
        timeline: str = "MEDIUM-TERM",
        rsi: float = 50.0
    ) -> str:
        """
        Synthesize all agent inputs and generate final investment recommendation.

        Args:
            technical_signal: Signal from QuantitativeAnalyst
            fundamental_score: Score from DataAnalyst (1-10)
            risk_assessment: Assessment from RiskManager
            trend: Trend from OrganiserAgent
            confidence_score: Technical confidence (1-100)
            current_price: Current stock price
            entry_price: Recommended entry price
            target_price: Target exit price
            stop_loss: Stop-loss price
            position_size_pct: Position size as % of portfolio
            timeline: Investment timeline
            rsi: RSI value
        """
        try:
            # Calculate final decision
            decision = calculate_final_decision(
                technical_signal,
                fundamental_score,
                risk_assessment,
                trend,
                confidence_score
            )

            # Generate key reasons
            reasons = generate_key_reasons(
                technical_signal,
                fundamental_score,
                risk_assessment,
                trend,
                decision['recommendation']
            )

            # Identify top risks
            risks = identify_top_risks(
                technical_signal,
                trend,
                fundamental_score,
                rsi
            )

            # Generate executive summary
            if decision['recommendation'] == 'BUY':
                exec_summary = f"Based on comprehensive multi-agent analysis with {decision['confidence']}% confidence, we recommend BUYING this stock. The combination of {technical_signal} technical signal, {trend.lower()} trend, and {risk_assessment.lower()} risk/reward profile supports this decision. Our weighted framework yields a score of {decision['score']}/100."
            elif decision['recommendation'] == 'HOLD':
                exec_summary = f"Based on mixed signals from our 6-agent analysis with {decision['confidence']}% confidence, we recommend HOLDING or waiting for better entry. The technical signal is {technical_signal}, trend is {trend}, with overall score of {decision['score']}/100. Consider waiting for clearer directional confirmation."
            else:
                exec_summary = f"Based on comprehensive analysis with {decision['confidence']}% confidence, we recommend SELLING or AVOIDING this stock. The {technical_signal} signal, {trend.lower()} trend, and fundamental score of {fundamental_score}/10 suggest limited upside potential. Overall score: {decision['score']}/100."

            # Generate agent consensus summaries
            organiser_summary = f"{trend} trend with RSI at {rsi:.1f}"
            risk_summary = f"{risk_assessment} risk/reward, {position_size_pct}% position size recommended"
            data_summary = f"Fundamental score {fundamental_score}/10"
            quant_summary = f"{technical_signal} signal with {confidence_score}% confidence"
            strategy_summary = f"{timeline} strategy, entry ${entry_price:.2f}, target ${target_price:.2f}"

            # Final note
            if decision['recommendation'] == 'BUY' and decision['confidence'] < 70:
                final_note = "⚠️ Moderate confidence - Consider smaller position size or wait for confirmation"
            elif decision['recommendation'] == 'BUY' and rsi > 70:
                final_note = "⚠️ Overbought conditions - Consider waiting for pullback before entry"
            elif decision['recommendation'] == 'HOLD':
                final_note = "⚠️ Mixed signals detected - Patience recommended until clearer trend emerges"
            elif decision['recommendation'] == 'SELL':
                final_note = "⚠️ Risk outweighs potential reward - Avoid or exit existing positions"
            else:
                final_note = "✅ All systems aligned - High-conviction trade setup"

            # Format the final report
            return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 FINAL INVESTMENT RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 DECISION: {decision['recommendation']}
🎯 CONFIDENCE: {decision['confidence']}% (1-100)
💯 OVERALL SCORE: {decision['score']}/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 EXECUTIVE SUMMARY:
{exec_summary}

✅ KEY SUPPORTING REASONS:
{chr(10).join(reasons)}

⚠️ TOP RISKS TO CONSIDER:
{chr(10).join(risks)}

📊 DECISION FRAMEWORK BREAKDOWN:
• Technical Analysis (25%): {decision['breakdown']['technical_contribution']} points
• Risk Management (25%): {decision['breakdown']['risk_contribution']} points
• Fundamental Analysis (20%): {decision['breakdown']['fundamental_contribution']} points
• Trend Analysis (20%): {decision['breakdown']['trend_contribution']} points
• Signal Confidence (10%): {decision['breakdown']['confidence_contribution']} points

💼 EXECUTION PARAMETERS:
• Entry Price: ${entry_price:.2f} (Current: ${current_price:.2f})
• Target Price: ${target_price:.2f} (+{((target_price - entry_price) / entry_price * 100):.1f}% potential)
• Stop-Loss: ${stop_loss:.2f} (-{((entry_price - stop_loss) / entry_price * 100):.1f}% max loss)
• Position Size: {position_size_pct:.1f}% of portfolio
• Timeline: {timeline}

🎓 AGENT CONSENSUS:
• OrganiserAgent (Market Data): {organiser_summary}
• RiskManager: {risk_summary}
• DataAnalyst (Fundamentals): {data_summary}
• QuantitativeAnalyst (Signals): {quant_summary}
• StrategyDeveloper: {strategy_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ FINAL NOTE: {final_note}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINAL_ANALYSIS_COMPLETE
"""

        except Exception as e:
            logger.error(f"Error synthesizing final recommendation: {str(e)}")
            return f"""❌ Error generating final recommendation: {str(e)}

FINAL_ANALYSIS_COMPLETE
"""

    return AssistantAgent(
        name="ReportAgent",
        model_client=model_client,
        tools=[synthesize_final_recommendation],
        system_message=system_message,
        description="Synthesizes all agent insights and provides final BUY/SELL/HOLD recommendation"
    )
