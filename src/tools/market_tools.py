"""
Market data tools for fetching stock prices and news using yfinance.
"""

import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta


def get_stock_price(ticker: str) -> Dict:
    """
    Get current stock price and performance metrics.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')

    Returns:
        Dictionary with price information and performance metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Get current price
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))

        # Get previous close
        previous_close = info.get('previousClose', 0)

        # Calculate day change
        if previous_close > 0:
            day_change = current_price - previous_close
            day_change_pct = (day_change / previous_close) * 100
        else:
            day_change = 0
            day_change_pct = 0

        # Try to get YTD return (52-week data)
        hist = stock.history(period="ytd")
        if not hist.empty:
            ytd_start_price = hist['Close'].iloc[0]
            ytd_return = ((current_price - ytd_start_price) / ytd_start_price) * 100
        else:
            ytd_return = None

        return {
            "symbol": ticker,
            "name": info.get('longName', ticker),
            "current_price": current_price,
            "previous_close": previous_close,
            "day_change": day_change,
            "day_change_pct": day_change_pct,
            "ytd_return": ytd_return,
            "52_week_high": info.get('fiftyTwoWeekHigh'),
            "52_week_low": info.get('fiftyTwoWeekLow'),
            "market_cap": info.get('marketCap'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A')
        }

    except Exception as e:
        return {
            "symbol": ticker,
            "error": f"Error fetching price for {ticker}: {str(e)}",
            "current_price": None
        }


def search_stock_news(ticker: str, query: Optional[str] = None) -> List[Dict]:
    """
    Search for recent news about a stock.

    Args:
        ticker: Stock ticker symbol
        query: Optional search query to filter news

    Returns:
        List of news articles with headlines and summaries
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news

        if not news:
            return []

        # Get up to 5 most recent news items
        news_items = []
        for item in news[:5]:
            news_item = {
                "title": item.get('title', 'No title'),
                "publisher": item.get('publisher', 'Unknown'),
                "link": item.get('link', ''),
                "published": datetime.fromtimestamp(
                    item.get('providerPublishTime', 0)
                ).strftime('%Y-%m-%d %H:%M:%S') if item.get('providerPublishTime') else 'Unknown'
            }

            # Apply query filter if provided
            if query:
                if query.lower() in news_item['title'].lower():
                    news_items.append(news_item)
            else:
                news_items.append(news_item)

        return news_items

    except Exception as e:
        return [{
            "error": f"Error fetching news for {ticker}: {str(e)}"
        }]


def get_multiple_stock_prices(tickers: List[str]) -> Dict[str, Dict]:
    """
    Batch fetch prices for multiple stocks.

    Args:
        tickers: List of stock ticker symbols

    Returns:
        Dictionary mapping ticker symbols to their price information
    """
    results = {}

    for ticker in tickers:
        if ticker.upper() == "CASH":
            # Handle cash holdings
            results[ticker] = {
                "symbol": ticker,
                "name": "Cash",
                "current_price": 1.0,
                "day_change": 0,
                "day_change_pct": 0
            }
        else:
            results[ticker] = get_stock_price(ticker)

    return results


def format_market_data_for_llm(market_data: Dict) -> str:
    """
    Format market data as a readable string for LLM consumption.

    Args:
        market_data: Dictionary of market data from get_multiple_stock_prices

    Returns:
        Formatted string representation of market data
    """
    if not market_data:
        return "No market data available."

    output = "Market Data:\n\n"

    for ticker, data in market_data.items():
        if "error" in data:
            output += f"{ticker}: {data['error']}\n\n"
            continue

        output += f"{data.get('name', ticker)} ({ticker}):\n"
        output += f"  - Current Price: ${data.get('current_price', 0):.2f}\n"
        output += f"  - Day Change: {data.get('day_change', 0):+.2f} ({data.get('day_change_pct', 0):+.2f}%)\n"

        if data.get('ytd_return') is not None:
            output += f"  - YTD Return: {data['ytd_return']:+.2f}%\n"

        if data.get('52_week_high'):
            output += f"  - 52-Week Range: ${data['52_week_low']:.2f} - ${data['52_week_high']:.2f}\n"

        output += f"  - Sector: {data.get('sector', 'N/A')}\n\n"

    return output


def format_news_for_llm(news_data: Dict[str, List[Dict]]) -> str:
    """
    Format news data as a readable string for LLM consumption.

    Args:
        news_data: Dictionary mapping ticker symbols to lists of news items

    Returns:
        Formatted string representation of news
    """
    if not news_data:
        return "No news data available."

    output = "Recent News:\n\n"

    for ticker, news_items in news_data.items():
        if not news_items:
            continue

        output += f"{ticker} News:\n"
        for i, item in enumerate(news_items, 1):
            if "error" in item:
                output += f"  {item['error']}\n"
                continue

            output += f"  {i}. {item['title']}\n"
            output += f"     Publisher: {item['publisher']} | {item['published']}\n"

        output += "\n"

    return output
