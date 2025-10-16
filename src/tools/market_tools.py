"""
Market data tools for fetching stock prices and news using yfinance.
"""

import yfinance as yf
import time
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
    # Fallback demo data for common tickers (used when yfinance fails)
    demo_prices = {
        "AAPL": {"price": 178.72, "change_pct": 1.23, "name": "Apple Inc."},
        "MSFT": {"price": 378.91, "change_pct": 0.85, "name": "Microsoft Corporation"},
        "GOOGL": {"price": 138.45, "change_pct": -0.42, "name": "Alphabet Inc."},
        "AMZN": {"price": 145.32, "change_pct": 1.12, "name": "Amazon.com Inc."},
        "TSLA": {"price": 242.84, "change_pct": 2.34, "name": "Tesla Inc."},
        "META": {"price": 312.56, "change_pct": 0.98, "name": "Meta Platforms Inc."},
        "NVDA": {"price": 495.22, "change_pct": 3.45, "name": "NVIDIA Corporation"},
        "VTI": {"price": 255.42, "change_pct": 0.67, "name": "Vanguard Total Stock Market ETF"},
        "BND": {"price": 74.85, "change_pct": -0.12, "name": "Vanguard Total Bond Market ETF"},
        "VXUS": {"price": 62.18, "change_pct": 0.45, "name": "Vanguard Total International Stock ETF"},
        "VYM": {"price": 115.30, "change_pct": 0.32, "name": "Vanguard High Dividend Yield ETF"},
        "VTEB": {"price": 50.95, "change_pct": -0.08, "name": "Vanguard Tax-Exempt Bond ETF"},
    }
    
    try:
        stock = yf.Ticker(ticker)
        
        # Try to get historical data first (more reliable than info)
        hist = stock.history(period="5d")
        
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            
            # Calculate day change
            if previous_close > 0:
                day_change = current_price - previous_close
                day_change_pct = (day_change / previous_close) * 100
            else:
                day_change = 0
                day_change_pct = 0
                
            # Get YTD return
            ytd_hist = stock.history(period="ytd")
            if not ytd_hist.empty:
                ytd_start_price = ytd_hist['Close'].iloc[0]
                ytd_return = ((current_price - ytd_start_price) / ytd_start_price) * 100
            else:
                ytd_return = None
            
            # Try to get additional info (may fail due to rate limiting)
            try:
                info = stock.info
                name = info.get('longName', ticker)
                sector = info.get('sector', 'N/A')
                industry = info.get('industry', 'N/A')
                market_cap = info.get('marketCap')
                week_high = info.get('fiftyTwoWeekHigh')
                week_low = info.get('fiftyTwoWeekLow')
            except:
                name = ticker
                sector = 'N/A'
                industry = 'N/A'
                market_cap = None
                week_high = None
                week_low = None
            
            return {
                "symbol": ticker,
                "name": name,
                "current_price": float(current_price),
                "previous_close": float(previous_close),
                "day_change": float(day_change),
                "day_change_pct": float(day_change_pct),
                "ytd_return": float(ytd_return) if ytd_return is not None else None,
                "52_week_high": week_high,
                "52_week_low": week_low,
                "market_cap": market_cap,
                "sector": sector,
                "industry": industry
            }
        else:
            # No historical data - try fallback demo data
            if ticker.upper() in demo_prices:
                demo = demo_prices[ticker.upper()]
                return {
                    "symbol": ticker,
                    "name": demo["name"],
                    "current_price": demo["price"],
                    "previous_close": demo["price"] * (1 - demo["change_pct"]/100),
                    "day_change": demo["price"] * demo["change_pct"]/100,
                    "day_change_pct": demo["change_pct"],
                    "ytd_return": None,
                    "52_week_high": None,
                    "52_week_low": None,
                    "market_cap": None,
                    "sector": "N/A",
                    "industry": "N/A",
                    "data_source": "demo"  # Indicate this is demo data
                }
            else:
                raise ValueError(f"No historical data available for {ticker}")

    except Exception as e:
        # Last resort: check demo data
        if ticker.upper() in demo_prices:
            demo = demo_prices[ticker.upper()]
            return {
                "symbol": ticker,
                "name": demo["name"],
                "current_price": demo["price"],
                "previous_close": demo["price"] * (1 - demo["change_pct"]/100),
                "day_change": demo["price"] * demo["change_pct"]/100,
                "day_change_pct": demo["change_pct"],
                "ytd_return": None,
                "52_week_high": None,
                "52_week_low": None,
                "market_cap": None,
                "sector": "N/A",
                "industry": "N/A",
                "data_source": "demo",  # Indicate this is demo data
                "note": "Using demo data due to API limitations"
            }
        else:
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
    Batch fetch prices for multiple stocks using parallel execution.

    Args:
        tickers: List of stock ticker symbols

    Returns:
        Dictionary mapping ticker symbols to their price information
    """
    import concurrent.futures
    
    results = {}

    def fetch_ticker_price(ticker):
        """Helper function to fetch a single ticker's price."""
        if ticker.upper() == "CASH":
            return ticker, {
                "symbol": ticker,
                "name": "Cash",
                "current_price": 1.0,
                "day_change": 0,
                "day_change_pct": 0
            }
        else:
            return ticker, get_stock_price(ticker)
    
    # Use ThreadPoolExecutor for parallel API calls
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks
        future_to_ticker = {executor.submit(fetch_ticker_price, ticker): ticker for ticker in tickers}
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_ticker):
            ticker, price_data = future.result()
            results[ticker] = price_data

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
