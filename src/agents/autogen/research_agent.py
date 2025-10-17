"""
OrganiserAgent - Market Data Coordinator & Technical Analysis Specialist

This agent fetches real-time stock data, calculates technical indicators,
and provides the foundation data for other agents in the analysis workflow.
"""

import os
import logging
from typing import Optional
import yfinance as yf
import requests
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_stock_data(symbol: str) -> dict:
    """
    Fetch real-time stock data using yfinance and Alpha Vantage as backup.

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL")

    Returns:
        dict: Stock data including price, volume, and technical indicators
    """
    try:
        # Primary source: yfinance
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="6mo")

        if hist.empty:
            raise ValueError("No historical data available")

        current_price = info.get('currentPrice', hist['Close'].iloc[-1])

        # Calculate technical indicators
        close_prices = hist['Close']

        # RSI Calculation (14-period)
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1] if not rsi.empty else 50

        # Moving Averages
        sma_50 = close_prices.rolling(window=50).mean().iloc[-1] if len(close_prices) >= 50 else current_price
        sma_200 = close_prices.rolling(window=200).mean().iloc[-1] if len(close_prices) >= 200 else current_price

        # MACD (12, 26, 9)
        exp1 = close_prices.ewm(span=12, adjust=False).mean()
        exp2 = close_prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()
        current_macd = macd.iloc[-1]
        current_signal = signal_line.iloc[-1]

        # Trend Analysis
        if current_price > sma_50 > sma_200:
            trend = "BULLISH"
        elif current_price < sma_50 < sma_200:
            trend = "BEARISH"
        else:
            trend = "NEUTRAL"

        return {
            'symbol': symbol,
            'current_price': round(current_price, 2),
            'volume': info.get('volume', hist['Volume'].iloc[-1]),
            'market_cap': info.get('marketCap', 'N/A'),
            '52_week_high': info.get('fiftyTwoWeekHigh', hist['High'].max()),
            '52_week_low': info.get('fiftyTwoWeekLow', hist['Low'].min()),
            'rsi': round(current_rsi, 2),
            'macd': round(current_macd, 2),
            'macd_signal': round(current_signal, 2),
            'sma_50': round(sma_50, 2),
            'sma_200': round(sma_200, 2),
            'trend': trend,
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
        return {
            'symbol': symbol,
            'status': 'error',
            'message': str(e)
        }


def get_alpha_vantage_data(symbol: str, api_key: str) -> dict:
    """
    Backup function to fetch data from Alpha Vantage API.

    Args:
        symbol: Stock ticker symbol
        api_key: Alpha Vantage API key

    Returns:
        dict: Stock data and technical indicators
    """
    try:
        base_url = "https://www.alphavantage.co/query"

        # Get quote
        quote_params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': api_key
        }
        quote_response = requests.get(base_url, params=quote_params, timeout=10)
        quote_data = quote_response.json().get('Global Quote', {})

        # Get RSI
        rsi_params = {
            'function': 'RSI',
            'symbol': symbol,
            'interval': 'daily',
            'time_period': 14,
            'series_type': 'close',
            'apikey': api_key
        }
        rsi_response = requests.get(base_url, params=rsi_params, timeout=10)
        rsi_data = rsi_response.json().get('Technical Analysis: RSI', {})
        latest_rsi = list(rsi_data.values())[0]['RSI'] if rsi_data else '50'

        return {
            'symbol': symbol,
            'current_price': float(quote_data.get('05. price', 0)),
            'volume': int(quote_data.get('06. volume', 0)),
            'rsi': float(latest_rsi),
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Alpha Vantage API error: {str(e)}")
        return {'status': 'error', 'message': str(e)}


def create_organiser_agent(model_client: Optional[OpenAIChatCompletionClient] = None) -> AssistantAgent:
    """
    Create the OrganiserAgent - Market Data Coordinator.

    Args:
        model_client: OpenAI model client (if None, creates default)

    Returns:
        AssistantAgent: Configured OrganiserAgent
    """
    if model_client is None:
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    system_message = """You are the OrganiserAgent - Market Data Coordinator & Technical Analysis Specialist.

Your PRIMARY responsibilities:
1. Fetch and present real-time stock market data (current price, volume, market cap, 52-week range)
2. Calculate and interpret technical indicators:
   - RSI (14-period): Oversold (<30), Neutral (30-70), Overbought (>70)
   - MACD (12,26,9): Bullish (MACD > Signal), Bearish (MACD < Signal)
   - Moving Averages: SMA 50 and SMA 200
3. Identify overall trend: BULLISH, BEARISH, or NEUTRAL
4. Provide factual data without making investment recommendations

RESPONSE FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MARKET DATA REPORT - [SYMBOL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 PRICE DATA:
• Current Price: $XXX.XX
• Volume: X,XXX,XXX shares
• Market Cap: $X.XXB
• 52-Week Range: $XXX.XX - $XXX.XX

📈 TECHNICAL INDICATORS:
• RSI (14): XX.XX [OVERSOLD/NEUTRAL/OVERBOUGHT]
• MACD: X.XX | Signal: X.XX [BULLISH/BEARISH]
• SMA 50: $XXX.XX
• SMA 200: $XXX.XX

🎯 TREND ANALYSIS:
Overall Trend: [BULLISH/BEARISH/NEUTRAL]
Price vs SMA 50: [ABOVE/BELOW] (X.X%)
Price vs SMA 200: [ABOVE/BELOW] (X.X%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL RULES:
- You are FIRST in the analysis chain
- Provide ONLY factual market data
- NO investment recommendations or predictions
- Use clear, structured formatting
- Be concise but comprehensive
"""

    # Create tools for the agent
    def fetch_market_data(symbol: str) -> str:
        """Fetch comprehensive market data and technical indicators for a stock."""
        data = get_stock_data(symbol)

        if data['status'] == 'error':
            # Try Alpha Vantage as backup
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            if api_key:
                data = get_alpha_vantage_data(symbol, api_key)

        if data['status'] == 'error':
            return f"❌ Error fetching data for {symbol}: {data.get('message', 'Unknown error')}"

        # Format the response
        price_change_50 = ((data['current_price'] - data['sma_50']) / data['sma_50'] * 100) if 'sma_50' in data else 0
        price_change_200 = ((data['current_price'] - data['sma_200']) / data['sma_200'] * 100) if 'sma_200' in data else 0

        rsi_status = "OVERSOLD" if data.get('rsi', 50) < 30 else "OVERBOUGHT" if data.get('rsi', 50) > 70 else "NEUTRAL"
        macd_status = "BULLISH" if data.get('macd', 0) > data.get('macd_signal', 0) else "BEARISH"

        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MARKET DATA REPORT - {data['symbol']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 PRICE DATA:
• Current Price: ${data['current_price']}
• Volume: {data['volume']:,} shares
• Market Cap: {data.get('market_cap', 'N/A')}
• 52-Week Range: ${data['52_week_low']} - ${data['52_week_high']}

📈 TECHNICAL INDICATORS:
• RSI (14): {data.get('rsi', 'N/A')} [{rsi_status}]
• MACD: {data.get('macd', 'N/A')} | Signal: {data.get('macd_signal', 'N/A')} [{macd_status}]
• SMA 50: ${data.get('sma_50', 'N/A')}
• SMA 200: ${data.get('sma_200', 'N/A')}

🎯 TREND ANALYSIS:
Overall Trend: {data['trend']}
Price vs SMA 50: {'ABOVE' if price_change_50 > 0 else 'BELOW'} ({price_change_50:+.1f}%)
Price vs SMA 200: {'ABOVE' if price_change_200 > 0 else 'BELOW'} ({price_change_200:+.1f}%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return AssistantAgent(
        name="OrganiserAgent",
        model_client=model_client,
        tools=[fetch_market_data],
        system_message=system_message,
        description="Fetches real-time market data and calculates technical indicators"
    )
