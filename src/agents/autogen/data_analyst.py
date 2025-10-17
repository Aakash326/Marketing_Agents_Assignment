"""
DataAnalyst - Fundamental Analysis & Research Specialist

This agent fetches fundamental data, performs web research for recent news,
and analyzes company financials and analyst opinions.
"""

import os
import logging
from typing import Optional
import yfinance as yf
import requests
from datetime import datetime, timedelta
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_fundamental_data(symbol: str) -> dict:
    """
    Fetch fundamental data for a stock using yfinance with Alpha Vantage backup.

    Args:
        symbol: Stock ticker symbol

    Returns:
        dict: Fundamental data including P/E, EPS, revenue, etc.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        return {
            'symbol': symbol,
            'company_name': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'forward_pe': info.get('forwardPE', 'N/A'),
            'peg_ratio': info.get('pegRatio', 'N/A'),
            'price_to_book': info.get('priceToBook', 'N/A'),
            'eps': info.get('trailingEps', 'N/A'),
            'revenue': info.get('totalRevenue', 'N/A'),
            'revenue_growth': info.get('revenueGrowth', 'N/A'),
            'profit_margin': info.get('profitMargins', 'N/A'),
            'operating_margin': info.get('operatingMargins', 'N/A'),
            'roe': info.get('returnOnEquity', 'N/A'),
            'debt_to_equity': info.get('debtToEquity', 'N/A'),
            'current_ratio': info.get('currentRatio', 'N/A'),
            'dividend_yield': info.get('dividendYield', 'N/A'),
            'analyst_target': info.get('targetMeanPrice', 'N/A'),
            'analyst_recommendation': info.get('recommendationKey', 'N/A'),
            'num_analyst_opinions': info.get('numberOfAnalystOpinions', 'N/A'),
            'earnings_date': info.get('earningsTimestamp', 'N/A'),
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Error fetching fundamental data for {symbol}: {str(e)}")
        
        # Try Alpha Vantage as backup
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if api_key:
            try:
                logger.info(f"Trying Alpha Vantage backup for {symbol}")
                base_url = "https://www.alphavantage.co/query"
                
                # Get company overview
                params = {
                    'function': 'OVERVIEW',
                    'symbol': symbol,
                    'apikey': api_key
                }
                response = requests.get(base_url, params=params, timeout=10)
                data = response.json()
                
                if 'Symbol' in data:
                    return {
                        'symbol': symbol,
                        'company_name': data.get('Name', 'N/A'),
                        'sector': data.get('Sector', 'N/A'),
                        'industry': data.get('Industry', 'N/A'),
                        'pe_ratio': float(data.get('PERatio', 0)) if data.get('PERatio') != 'None' else 'N/A',
                        'forward_pe': 'N/A',
                        'peg_ratio': float(data.get('PEGRatio', 0)) if data.get('PEGRatio') != 'None' else 'N/A',
                        'price_to_book': float(data.get('PriceToBookRatio', 0)) if data.get('PriceToBookRatio') != 'None' else 'N/A',
                        'eps': float(data.get('EPS', 0)) if data.get('EPS') != 'None' else 'N/A',
                        'revenue': 'N/A',
                        'revenue_growth': 'N/A',
                        'profit_margin': float(data.get('ProfitMargin', 0)) if data.get('ProfitMargin') != 'None' else 'N/A',
                        'operating_margin': float(data.get('OperatingMarginTTM', 0)) if data.get('OperatingMarginTTM') != 'None' else 'N/A',
                        'roe': float(data.get('ReturnOnEquityTTM', 0)) if data.get('ReturnOnEquityTTM') != 'None' else 'N/A',
                        'debt_to_equity': 'N/A',
                        'current_ratio': 'N/A',
                        'dividend_yield': float(data.get('DividendYield', 0)) if data.get('DividendYield') != 'None' else 'N/A',
                        'analyst_target': float(data.get('AnalystTargetPrice', 0)) if data.get('AnalystTargetPrice') != 'None' else 'N/A',
                        'analyst_recommendation': 'N/A',
                        'num_analyst_opinions': 'N/A',
                        'earnings_date': 'N/A',
                        'status': 'success',
                        'source': 'alpha_vantage'
                    }
            except Exception as av_error:
                logger.error(f"Alpha Vantage backup also failed: {str(av_error)}")
        
        return {'status': 'error', 'message': str(e), 'symbol': symbol}


def search_stock_news(symbol: str, company_name: str, tavily_api_key: Optional[str] = None) -> dict:
    """
    Search for recent news about a stock using Tavily API or fallback.

    Args:
        symbol: Stock ticker symbol
        company_name: Company name for search
        tavily_api_key: Tavily API key (optional)

    Returns:
        dict: News articles and sentiment
    """
    try:
        if tavily_api_key:
            # Use Tavily API for comprehensive search
            url = "https://api.tavily.com/search"
            headers = {"Content-Type": "application/json"}
            query = f"{company_name} {symbol} stock news latest"

            payload = {
                "api_key": tavily_api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": 5,
                "days": 7
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()

            articles = []
            for result in data.get('results', [])[:5]:
                articles.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'snippet': result.get('content', '')[:200],
                    'published': result.get('published_date', 'N/A')
                })

            return {
                'symbol': symbol,
                'articles': articles,
                'num_articles': len(articles),
                'status': 'success'
            }
        else:
            # Fallback: Use yfinance news
            ticker = yf.Ticker(symbol)
            news = ticker.news[:5] if hasattr(ticker, 'news') else []

            articles = []
            for article in news:
                articles.append({
                    'title': article.get('title', ''),
                    'url': article.get('link', ''),
                    'snippet': article.get('summary', '')[:200] if 'summary' in article else '',
                    'published': datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d') if 'providerPublishTime' in article else 'N/A'
                })

            return {
                'symbol': symbol,
                'articles': articles,
                'num_articles': len(articles),
                'status': 'success'
            }

    except Exception as e:
        logger.error(f"Error fetching news for {symbol}: {str(e)}")
        return {'status': 'error', 'message': str(e), 'symbol': symbol, 'articles': []}


def create_data_analyst(model_client: Optional[OpenAIChatCompletionClient] = None) -> AssistantAgent:
    """
    Create the DataAnalyst agent.

    Args:
        model_client: OpenAI model client (if None, creates default)

    Returns:
        AssistantAgent: Configured DataAnalyst agent
    """
    if model_client is None:
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    system_message = """You are the DataAnalyst - Fundamental Analysis & Research Specialist.

Your PRIMARY responsibilities:
1. Analyze fundamental data (P/E ratio, EPS, revenue growth, margins)
2. Research recent news and events affecting the stock
3. Evaluate analyst opinions and price targets
4. Identify upcoming catalysts (earnings dates, product launches)
5. Assess company financial health and competitive position

RESPONSE FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 FUNDAMENTAL ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 COMPANY OVERVIEW:
• Company: [NAME]
• Sector: [SECTOR] | Industry: [INDUSTRY]

💰 VALUATION METRICS:
• P/E Ratio: XX.X (vs Industry Avg: XX)
• Forward P/E: XX.X
• PEG Ratio: X.XX (< 1 is good)
• Price-to-Book: X.XX
• Assessment: [UNDERVALUED/FAIRLY VALUED/OVERVALUED]

📈 PROFITABILITY & GROWTH:
• EPS: $X.XX
• Revenue: $XXB (Growth: +X.X% YoY)
• Profit Margin: XX.X%
• Operating Margin: XX.X%
• ROE: XX.X%

💪 FINANCIAL HEALTH:
• Debt-to-Equity: X.XX (Lower is better)
• Current Ratio: X.XX (> 1.5 is healthy)
• Dividend Yield: X.X%
• Financial Strength: [STRONG/MODERATE/WEAK]

👨‍💼 ANALYST CONSENSUS:
• Recommendation: [STRONG BUY/BUY/HOLD/SELL/STRONG SELL]
• Target Price: $XXX (Upside: +XX%)
• Number of Analysts: XX

📰 RECENT NEWS & CATALYSTS:
• [Most significant recent news point 1]
• [Most significant recent news point 2]
• [Most significant recent news point 3]
• Upcoming Earnings: [DATE]
• News Sentiment: [POSITIVE/NEUTRAL/NEGATIVE]

🎯 FUNDAMENTAL SCORE: X/10
[Brief 2-3 sentence assessment of fundamental strength]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL RULES:
- Analyze AFTER OrganiserAgent and RiskManager
- Focus on company fundamentals and qualitative factors
- Provide context for metrics (industry comparisons)
- Highlight both strengths and weaknesses
- Cite recent news that could impact stock price
"""

    # Create tools for the agent
    def analyze_fundamentals(symbol: str) -> str:
        """
        Perform comprehensive fundamental analysis on a stock.

        Args:
            symbol: Stock ticker symbol
        """
        # Get fundamental data
        fundamentals = get_fundamental_data(symbol)

        if fundamentals['status'] == 'error':
            return f"❌ Error fetching fundamental data for {symbol}: {fundamentals.get('message', 'Unknown error')}"

        # Get news data
        tavily_key = os.getenv("TAVILY_API_KEY")
        news_data = search_stock_news(symbol, fundamentals.get('company_name', symbol), tavily_key)

        # Format PE ratio analysis
        pe_ratio = fundamentals.get('pe_ratio', 'N/A')
        pe_analysis = "N/A"
        if pe_ratio != 'N/A' and isinstance(pe_ratio, (int, float)):
            if pe_ratio < 15:
                pe_analysis = "POTENTIALLY UNDERVALUED"
            elif pe_ratio < 25:
                pe_analysis = "FAIRLY VALUED"
            else:
                pe_analysis = "POTENTIALLY OVERVALUED"

        # Format revenue
        revenue = fundamentals.get('revenue', 'N/A')
        if revenue != 'N/A' and isinstance(revenue, (int, float)):
            revenue_str = f"${revenue / 1e9:.2f}B" if revenue > 1e9 else f"${revenue / 1e6:.2f}M"
        else:
            revenue_str = "N/A"

        # Format revenue growth
        rev_growth = fundamentals.get('revenue_growth', 'N/A')
        rev_growth_str = f"+{rev_growth * 100:.1f}%" if rev_growth != 'N/A' and isinstance(rev_growth, (int, float)) else "N/A"

        # Format margins
        profit_margin = fundamentals.get('profit_margin', 'N/A')
        profit_margin_str = f"{profit_margin * 100:.1f}%" if profit_margin != 'N/A' and isinstance(profit_margin, (int, float)) else "N/A"

        operating_margin = fundamentals.get('operating_margin', 'N/A')
        operating_margin_str = f"{operating_margin * 100:.1f}%" if operating_margin != 'N/A' and isinstance(operating_margin, (int, float)) else "N/A"

        roe = fundamentals.get('roe', 'N/A')
        roe_str = f"{roe * 100:.1f}%" if roe != 'N/A' and isinstance(roe, (int, float)) else "N/A"

        # Financial health assessment
        debt_to_equity = fundamentals.get('debt_to_equity', 'N/A')
        current_ratio = fundamentals.get('current_ratio', 'N/A')

        if debt_to_equity != 'N/A' and current_ratio != 'N/A':
            if debt_to_equity < 0.5 and current_ratio > 1.5:
                fin_health = "STRONG 💪"
            elif debt_to_equity < 1.0 and current_ratio > 1.0:
                fin_health = "MODERATE ⚖️"
            else:
                fin_health = "WEAK ⚠️"
        else:
            fin_health = "INSUFFICIENT DATA"

        # Analyst consensus
        recommendation = fundamentals.get('analyst_recommendation', 'N/A')
        target_price = fundamentals.get('analyst_target', 'N/A')

        # Format news
        news_items = news_data.get('articles', [])[:3]
        news_bullets = "\n".join([f"• {article['title'][:80]}..." for article in news_items]) if news_items else "• No recent news available"

        # Calculate fundamental score (simplified)
        score = 5  # Start at neutral
        if pe_ratio != 'N/A' and isinstance(pe_ratio, (int, float)):
            if pe_ratio < 15:
                score += 1
            elif pe_ratio > 30:
                score -= 1

        if rev_growth != 'N/A' and isinstance(rev_growth, (int, float)) and rev_growth > 0.1:
            score += 1

        if profit_margin != 'N/A' and isinstance(profit_margin, (int, float)) and profit_margin > 0.15:
            score += 1

        if fin_health == "STRONG 💪":
            score += 2
        elif fin_health == "WEAK ⚠️":
            score -= 2

        score = max(1, min(10, score))  # Clamp between 1-10

        # Format dividend yield
        div_yield = fundamentals.get('dividend_yield', 'N/A')
        div_yield_str = f"{div_yield * 100:.2f}%" if div_yield != 'N/A' and isinstance(div_yield, (int, float)) else "N/A"

        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 FUNDAMENTAL ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 COMPANY OVERVIEW:
• Company: {fundamentals.get('company_name', 'N/A')}
• Sector: {fundamentals.get('sector', 'N/A')} | Industry: {fundamentals.get('industry', 'N/A')}

💰 VALUATION METRICS:
• P/E Ratio: {pe_ratio if pe_ratio != 'N/A' else 'N/A'}
• Forward P/E: {fundamentals.get('forward_pe', 'N/A')}
• PEG Ratio: {fundamentals.get('peg_ratio', 'N/A')}
• Price-to-Book: {fundamentals.get('price_to_book', 'N/A')}
• Assessment: {pe_analysis}

📈 PROFITABILITY & GROWTH:
• EPS: ${fundamentals.get('eps', 'N/A')}
• Revenue: {revenue_str} (Growth: {rev_growth_str} YoY)
• Profit Margin: {profit_margin_str}
• Operating Margin: {operating_margin_str}
• ROE: {roe_str}

💪 FINANCIAL HEALTH:
• Debt-to-Equity: {debt_to_equity if debt_to_equity != 'N/A' else 'N/A'}
• Current Ratio: {current_ratio if current_ratio != 'N/A' else 'N/A'}
• Dividend Yield: {div_yield_str}
• Financial Strength: {fin_health}

👨‍💼 ANALYST CONSENSUS:
• Recommendation: {recommendation.upper() if recommendation != 'N/A' else 'N/A'}
• Target Price: ${target_price if target_price != 'N/A' else 'N/A'}
• Number of Analysts: {fundamentals.get('num_analyst_opinions', 'N/A')}

📰 RECENT NEWS & CATALYSTS:
{news_bullets}
• News Sentiment: {'POSITIVE ✅' if news_items else 'NEUTRAL'}

🎯 FUNDAMENTAL SCORE: {score}/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return AssistantAgent(
        name="DataAnalyst",
        model_client=model_client,
        tools=[analyze_fundamentals],
        system_message=system_message,
        description="Performs fundamental analysis, researches news, and evaluates analyst opinions"
    )
