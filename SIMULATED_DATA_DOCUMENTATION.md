# 🎭 Simulated & Demo Data Documentation

## 📋 Overview

This document explains **all simulated, mock, demo, and fallback data** used in the Portfolio Intelligence System. Understanding what's real vs. simulated helps in testing, debugging, and future production deployment.

---

## 🗂️ Types of Simulated Data

### 1. 📊 Portfolio Data (Real from Excel)
**Location:** `portfolios.xlsx`  
**Status:** ✅ **REAL DATA** (Not Simulated)

**Description:**
- Portfolio holdings are loaded from an Excel file
- Contains real client portfolio data (CLT-001 through CLT-010)
- Includes: Symbol, Quantity, Purchase Price, Security Name, Asset Class, Sector

**Files Using This:**
- `src/tools/portfolio_tools.py` → `load_portfolio_data()`
- `src/nodes/portfolio_node.py`
- `backends/langgraph_backend/app/api/routes/portfolio.py` → `load_portfolio_from_excel()`

**Data Structure:**
```python
{
    "client_id": "CLT-001",
    "holdings": [
        {
            "symbol": "AAPL",
            "quantity": 150,
            "purchase_price": 145.30,
            "security_name": "Apple Inc.",
            "asset_class": "Equity",
            "sector": "Technology"
        },
        # ... more holdings
    ],
    "last_updated": "2024-10-15"
}
```

---

### 2. 💰 Current Stock Prices (Simulated for Display)
**Location:** `backends/langgraph_backend/app/api/routes/portfolio.py` (Line 90)  
**Status:** ⚠️ **SIMULATED** (Hash-based price changes)

**Code:**
```python
# Line 90 in portfolio.py
current_price = purchase_price * (1 + (hash(str(row['symbol'])) % 20 - 10) / 100)
# Simulated price change: -10% to +10% based on symbol hash
```

**Purpose:**
- Generate "current prices" for portfolio value calculations
- Uses deterministic hash function (same symbol = same price change)
- Range: -10% to +10% from purchase price

**Why Simulated:**
- Quick portfolio value display without API calls
- Demonstrates portfolio returns/gains
- Fallback when market data APIs fail

**Affected Features:**
- Portfolio total value display
- Individual holding gains/losses
- Return percentage calculations in `collaboration_node.py`

**To Use Real Prices:** Replace with `get_stock_price()` from `market_tools.py`

---

### 3. 📈 Market Data (Real + Demo Fallback)
**Location:** `src/tools/market_tools.py`  
**Status:** ✅ **REAL** (yfinance) with ⚠️ **DEMO FALLBACK**

**Primary Source:** yfinance API (Yahoo Finance)
- Real-time stock prices
- Historical data
- Market indicators (52-week high/low, market cap, etc.)

**Demo Fallback Data (Lines 22-33):**
```python
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
```

**Fallback Trigger (Lines 95-148):**
1. **Primary:** Try yfinance historical data (5 days)
2. **Secondary:** Try yfinance info API
3. **Tertiary:** Use demo_prices dictionary
4. **Final:** Return error message

**Detection:**
```python
if "data_source" in result and result["data_source"] == "demo":
    print("⚠️ Using demo data")
```

**Files Using This:**
- `src/tools/market_tools.py` → `get_stock_price(ticker)`
- `src/nodes/market_node.py`
- `src/agents/autogen/data_analyst.py` (Alpha Vantage primary)

---

### 4. 🔍 Alpha Vantage API (Real Market Data)
**Location:** AutoGen agents (6-Agent Stock Analysis)  
**Status:** ✅ **REAL DATA**

**Primary Use:**
- `src/agents/autogen/data_analyst.py` → `get_comprehensive_stock_data()`
- 6-Agent Stock Analysis feature

**Data Provided:**
- Real-time price and volume
- Fundamental metrics (P/E ratio, analyst targets)
- Earnings dates
- 52-week high/low
- Technical indicators (RSI, MACD)

**Environment Variable:** `ALPHA_VANTAGE_API_KEY`

**Rate Limits:**
- Free tier: 25 requests/day
- Premium: 75+ requests/day

---

### 5. 🌐 Web Search Data (Real via Tavily)
**Location:** `src/agents/autogen/data_analyst.py`  
**Status:** ✅ **REAL DATA**

**Tool:** `search_company_web_info(symbol, query)`
- Uses Tavily API for real-time web search
- Searches news, SEC filings, analyst reports
- Returns actual web results

**Environment Variable:** `TAVILY_API_KEY`

---

## 📍 Where Simulation Happens

### Portfolio Intelligence (`/portfolio`)

| Component | Data Type | Source | Status |
|-----------|-----------|--------|--------|
| Holdings List | Portfolio data | `portfolios.xlsx` | ✅ Real |
| Purchase Prices | Historical data | Excel file | ✅ Real |
| **Current Prices** | Market data | **Hash function** | ⚠️ **Simulated** |
| Quantities | Portfolio data | Excel file | ✅ Real |
| Asset Classes | Portfolio data | Excel file | ✅ Real |
| Sectors | Portfolio data | Excel file | ✅ Real |

**Impact:**
- Total portfolio value is **simulated** (hash-based current prices)
- Individual holding gains/losses are **simulated**
- Return percentages in collaboration_node are **based on simulated prices**

**To Fix:**
```python
# In backends/langgraph_backend/app/api/routes/portfolio.py line 90
# Replace:
current_price = purchase_price * (1 + (hash(str(row['symbol'])) % 20 - 10) / 100)

# With:
from src.tools.market_tools import get_stock_price
market_data = get_stock_price(row['symbol'])
current_price = market_data.get('current_price', purchase_price)
```

---

### Stock Analysis (`/stock-analysis`)

| Component | Data Type | Source | Status |
|-----------|-----------|--------|--------|
| Market Data | Stock prices | Alpha Vantage API | ✅ Real |
| Technical Indicators | Calculated | Alpha Vantage | ✅ Real |
| Fundamental Data | Company metrics | Alpha Vantage | ✅ Real |
| Web Research | News & reports | Tavily API | ✅ Real |
| Agent Analysis | LLM inference | OpenAI GPT-4o-mini | ✅ Real |

**Impact:** ✅ **Fully Real Data** (No simulation)

---

### Enhanced Chat (`/chat`)

| Component | Data Type | Source | Status |
|-----------|-----------|--------|--------|
| Portfolio Questions | Portfolio + market | Excel + yfinance/demo | ✅ Real / ⚠️ Fallback |
| Market Questions | General knowledge | RAG vector store | ✅ Real |
| LLM Responses | AI inference | OpenAI GPT-4o-mini | ✅ Real |

**Impact:**
- Portfolio questions may use simulated current prices (see Portfolio Intelligence)
- Market questions use real RAG knowledge base
- Return calculations in `collaboration_node.py` use simulated prices from market_node

---

## 🔧 How to Identify Simulated Data

### 1. Check Response Fields

**Portfolio API Response:**
```python
# If you see this pattern, prices are simulated:
current_price = purchase_price * (1 + small_percentage)

# Look for these indicators:
- Prices ending in .00 (e.g., 145.00)
- Consistent percentage changes across symbols
- No "data_source" field in response
```

**Market API Response:**
```python
# Real data from yfinance:
{
    "symbol": "AAPL",
    "current_price": 178.72,
    "data_source": "yfinance"  # Not present = real
}

# Demo fallback data:
{
    "symbol": "AAPL",
    "current_price": 178.72,
    "data_source": "demo",  # ⚠️ Indicates simulated
    "note": "Using demo data due to API limitations"
}
```

### 2. Check Log Messages

**Real Data:**
```
✅ Fetched market data for AAPL from yfinance
✅ Alpha Vantage API response received
✅ Tavily search returned 5 results
```

**Simulated/Fallback Data:**
```
⚠️ Using demo data for AAPL (yfinance failed)
⚠️ portfolios.xlsx not found, returning demo data
⚠️ Alpha Vantage rate limit exceeded
```

### 3. Test File Analysis

**Test Files:**
- `test_system.py` - Tests real portfolio loading from Excel
- `test_rag.py` - Tests RAG system with real vector store
- `test_6agent_workflow.py` - Tests AutoGen with real Alpha Vantage
- `test_rag_query.py` - Tests RAG queries

**No simulation in test files** - they use real API calls and data sources

---

## 🎯 Production Readiness Checklist

### To Remove All Simulation:

#### 1. Fix Portfolio Current Prices
**File:** `backends/langgraph_backend/app/api/routes/portfolio.py`

**Current (Line 90):**
```python
current_price = purchase_price * (1 + (hash(str(row['symbol'])) % 20 - 10) / 100)
```

**Replace With:**
```python
from src.tools.market_tools import get_stock_price

# Add at the top of the function
price_cache = {}

# Replace line 90:
if row['symbol'] not in price_cache:
    market_data = get_stock_price(row['symbol'])
    price_cache[row['symbol']] = market_data.get('current_price')

current_price = price_cache.get(row['symbol'], purchase_price)
```

#### 2. Monitor API Rate Limits
- **yfinance:** Generally unlimited for basic requests
- **Alpha Vantage:** 25 requests/day (free tier)
- **Tavily:** Check your plan limits
- **OpenAI:** Token-based pricing

**Add Rate Limit Handling:**
```python
import time
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_get_stock_price(ticker: str):
    """Cache stock prices for 5 minutes"""
    return get_stock_price(ticker)
```

#### 3. Add Real-Time Price Updates
**Options:**
- WebSocket streaming from Polygon.io
- Real-time quotes from Interactive Brokers API
- Alpha Vantage real-time endpoint (premium)

#### 4. Database Migration
**Current:** Excel file (`portfolios.xlsx`)  
**Production:** PostgreSQL database

**Migration Steps:**
1. Create portfolio schema
2. Import Excel data to PostgreSQL
3. Update `load_portfolio_data()` to query database
4. Add authentication for multi-user support

---

## 📊 Data Source Summary

| Data Type | Primary Source | Fallback | Simulation Level |
|-----------|----------------|----------|------------------|
| Portfolio Holdings | `portfolios.xlsx` | None | None - 100% Real |
| Portfolio Current Prices | Hash function | None | **100% Simulated** |
| Market Prices (Chat) | yfinance | demo_prices dict | Real with fallback |
| Market Prices (Stock Analysis) | Alpha Vantage | None | 100% Real |
| Company News | Tavily API | None | 100% Real |
| Technical Indicators | Alpha Vantage | None | 100% Real |
| RAG Knowledge Base | Vector store | None | 100% Real |
| LLM Responses | OpenAI API | None | 100% Real |

---

## 🚨 Critical Simulation Points

### ⚠️ WARNING: Portfolio Values Are Simulated!

**Issue:**
```python
# backends/langgraph_backend/app/api/routes/portfolio.py line 90
current_price = purchase_price * (1 + (hash(str(row['symbol'])) % 20 - 10) / 100)
```

**Impact:**
- Total portfolio value displayed is **NOT real**
- Gains/losses shown are **deterministic but fake**
- Return percentages in Enhanced Chat are **based on fake prices**

**User Sees:**
```
Portfolio Value: $9,948,702.26  ⚠️ SIMULATED
AAPL: +5.23% return  ⚠️ SIMULATED
Total Gain: +$124,532.12  ⚠️ SIMULATED
```

**Fix Priority:** 🔴 **HIGH** - Users may make decisions based on this

---

## 🧪 Testing With Real Data

### Test Real API Connections

```bash
# Test yfinance (Enhanced Chat market data)
python -c "from src.tools.market_tools import get_stock_price; print(get_stock_price('AAPL'))"

# Test Alpha Vantage (Stock Analysis)
python -c "from src.agents.autogen.data_analyst import get_comprehensive_stock_data; print(get_comprehensive_stock_data('AAPL'))"

# Test Tavily (Web search)
python -c "from src.agents.autogen.data_analyst import search_company_web_info; print(search_company_web_info('AAPL', 'latest news'))"

# Test portfolio loading
python test_system.py
```

### Force Real Data Usage

**Disable demo fallback temporarily:**
```python
# In src/tools/market_tools.py
# Comment out lines 95-148 (fallback to demo_prices)
# This will raise errors instead of using demo data
```

---

## 📈 Future Enhancements

### Short-term (Remove Simulation)
1. ✅ Replace hash-based portfolio prices with yfinance API calls
2. ✅ Add price caching (5-15 min TTL)
3. ✅ Add "Last Updated" timestamp to portfolio display

### Medium-term (Improve Data Quality)
1. Use Alpha Vantage for all market data (more reliable than yfinance)
2. Add WebSocket for real-time price updates
3. Migrate from Excel to PostgreSQL database

### Long-term (Production Ready)
1. Multiple data source fallback chain
2. Historical price database (reduce API calls)
3. Market data subscription (Polygon.io, IEX Cloud)
4. Real-time streaming quotes

---

## 📞 Quick Reference

**Question:** "Are portfolio values real?"  
**Answer:** ⚠️ **No** - Current prices are hash-based simulations. Holdings and purchase prices are real from Excel.

**Question:** "Is stock analysis data real?"  
**Answer:** ✅ **Yes** - All data from Alpha Vantage API and Tavily web search.

**Question:** "What about Enhanced Chat?"  
**Answer:** 🟡 **Mixed** - Portfolio questions use simulated prices. Market questions use real RAG knowledge.

**Question:** "How do I get 100% real data?"  
**Answer:** Fix line 90 in `backends/langgraph_backend/app/api/routes/portfolio.py` (see section above).

---

## 🔍 Code Locations Reference

| Feature | File | Line | What's Simulated |
|---------|------|------|------------------|
| Portfolio Prices | `backends/langgraph_backend/app/api/routes/portfolio.py` | 90 | Current prices (hash-based) |
| Market Fallback | `src/tools/market_tools.py` | 22-33, 95-148 | Demo prices for 12 tickers |
| Alpha Vantage | `src/agents/autogen/data_analyst.py` | - | ✅ Real (no simulation) |
| Tavily Search | `src/agents/autogen/data_analyst.py` | - | ✅ Real (no simulation) |
| Return Calculations | `src/nodes/collaboration_node.py` | 48-64 | Uses simulated prices |

---

## 📝 Summary

**What's Real:**
- ✅ Portfolio holdings from Excel
- ✅ Stock Analysis (6-agent system)
- ✅ Alpha Vantage market data
- ✅ Tavily web search
- ✅ RAG knowledge base
- ✅ All LLM responses

**What's Simulated:**
- ⚠️ Portfolio current prices (hash-based)
- ⚠️ Portfolio total value
- ⚠️ Gains/losses in Portfolio Intelligence
- ⚠️ Return percentages in Enhanced Chat
- ⚠️ Demo fallback prices in market_tools.py (only when APIs fail)

**Priority Fix:**
Replace the hash-based price simulation in `portfolio.py` line 90 with real API calls to yfinance or Alpha Vantage.

---

**Last Updated:** October 29, 2025  
**Status:** Simulation identified and documented  
**Action Required:** Fix portfolio price simulation for production use
