# Portfolio Intelligence System

A production-ready AI-powered portfolio analysis system with a **multi-agent FastAPI backend** and **modern React frontend**. The system uses specialized AI agents that collaborate to provide intelligent portfolio and market analysis.

## 🎉 Complete System - Backend + Frontend

This repository contains both:
- ✅ **FastAPI Backend** with multi-agent AI system
- ✅ **React Frontend** with modern UI/UX

## 🚀 Quick Start

### One-Command Start (Recommended)

```bash
# Make scripts executable (first time only)
chmod +x start.sh stop.sh

# Start everything (activates conda env + starts both servers)
./start.sh
```

This automatically:
1. ✅ Activates conda environment `portfolio-intel`
2. ✅ Starts backend server (http://localhost:8000)
3. ✅ Starts frontend server (http://localhost:3000)

### Stop Everything

```bash
./stop.sh
```

## 📖 Documentation

- **[START_HERE.md](START_HERE.md)** - Quick start guide
- **[frontend/README.md](frontend/README.md)** - Frontend documentation
- **[frontend/QUICKSTART.md](frontend/QUICKSTART.md)** - Frontend 5-min setup
- **[backend/TEST_RESULTS.md](backend/TEST_RESULTS.md)** - Backend API tests
- **[FRONTEND_CHECKLIST.md](FRONTEND_CHECKLIST.md)** - Feature checklist

## 🌟 Features

### Frontend (React + Tailwind CSS)
- ✅ Modern UI with dark/light theme
- ✅ Real-time agent activity visualization
- ✅ Interactive portfolio dashboards
- ✅ Data visualization with charts
- ✅ Session management with history
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Keyboard shortcuts and accessibility

### Backend (FastAPI + Multi-Agent AI)
- ✅ Natural language query processing
- ✅ Multi-agent collaboration (Planner, Portfolio, Market, SEC, Validator)
- ✅ Real-time market data integration
- ✅ SEC filings integration
- ✅ Session and conversation management
- ✅ Comprehensive error handling

## 🎯 Access Points

Once started:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Overview

This system enables clients to ask natural language questions about their investments and receive accurate, data-driven responses through a beautiful web interface.

### Example Queries

- "What stocks do I own?"
- "What's the current price of Apple stock?"
- "Which of my holdings has the best return?"
- "How is Tesla doing in my portfolio?"
- "What's my total portfolio value?"

## Architecture

### Multi-Agent System

The system uses **LangGraph** to orchestrate four specialized agents:

#### 1. 🎯 Planner Agent
- Analyzes incoming queries
- Determines which agents need to be activated
- Routes queries to appropriate agents

#### 2. 💼 Portfolio Agent
- Loads client portfolio data from Excel
- Analyzes holdings, asset allocation, and composition
- Answers questions about what stocks the client owns

#### 3. 📈 Market Agent
- Fetches real-time stock prices using yfinance
- Retrieves recent news for relevant stocks
- Analyzes market performance and trends

#### 4. ✅ Validator Agent
- Validates responses for accuracy
- Checks for hallucinations or unsupported claims
- Ensures responses are grounded in actual data

### Workflow

```
User Query → Planner → [Portfolio &/or Market Agents] → Validator → Response
```

The workflow adapts based on the query:
- **Portfolio-only queries** → Planner → Portfolio Agent → Validator
- **Market-only queries** → Planner → Market Agent → Validator
- **Combined queries** → Planner → Portfolio Agent → Market Agent → Validator

## Technology Stack

- **LangGraph 0.6.10**: Multi-agent orchestration
- **LangChain**: LLM integration framework
- **OpenAI GPT-4o-mini**: Language model for analysis
- **yfinance**: Real-time stock market data
- **Streamlit**: Interactive web interface
- **Pandas & openpyxl**: Excel data processing

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Portfolio data in `portfolios.xlsx` (already included)

### Installation

1. **Clone or navigate to the project directory**

```bash
cd Assignment-marketing-agents
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Verify portfolio data**

Ensure `portfolios.xlsx` is in the project root directory.

### Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

1. **Select a client** from the sidebar dropdown (CLT-001 through CLT-010)
2. **Enter your query** in the text input field
3. **Click Submit** to get your answer
4. **View agent activity** in the expandable sections to see which agents were activated
5. **Explore raw data** to see the underlying portfolio and market information

## Sample Queries to Test

### Portfolio-Only Queries
- "What stocks do I own?"
- "List all my holdings"
- "What sectors am I invested in?"

### Market-Only Queries
- "What's the current price of AAPL?"
- "How is NVDA performing today?"
- "What's the latest news on Microsoft?"

### Combined Queries
- "How is Tesla doing in my portfolio?"
- "Which of my holdings has the best YTD return?"
- "What's the current value of my Microsoft position?"
- "Show me how my tech stocks are performing"

## Project Structure

```
Assignment-marketing-agents/
├── src/
│   ├── llm/
│   │   └── client.py              # OpenAI client setup
│   ├── state/
│   │   └── graph_state.py         # LangGraph state schema
│   ├── tools/
│   │   ├── portfolio_tools.py     # Portfolio data processing
│   │   ├── market_tools.py        # Market data fetching
│   │   └── validator_tools.py     # Response validation
│   ├── nodes/
│   │   ├── planner_node.py        # Planner agent
│   │   ├── portfolio_node.py      # Portfolio agent
│   │   ├── market_node.py         # Market agent
│   │   └── validator_node.py      # Validator agent
│   └── graph/
│       └── workflow.py            # LangGraph orchestration
├── app.py                         # Streamlit UI
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── portfolios.xlsx                # Client portfolio data
└── README.md                      # This file
```

## How It Works

### LangGraph Orchestration

The system uses LangGraph's `StateGraph` to manage the flow between agents:

1. **State Management**: A shared state (`GraphState`) is passed between all agents, containing:
   - User query and client ID
   - Portfolio and market data
   - Planning decisions
   - Generated responses

2. **Conditional Routing**: The planner determines which agents to activate based on the query type:
   - Uses conditional edges to route to portfolio and/or market agents
   - Ensures efficient execution by skipping unnecessary agents

3. **Data Flow**: Each agent enriches the state with new information:
   - Portfolio agent adds holdings data
   - Market agent adds prices and news
   - Validator ensures response quality

### Portfolio Data

Portfolio data is stored in `portfolios.xlsx` with the following structure:

- `client_id`: Client identifier (CLT-001, CLT-002, etc.)
- `symbol`: Stock ticker symbol
- `security_name`: Full name of the security
- `asset_class`: Type of asset (Stocks, Bonds, ETF, etc.)
- `quantity`: Number of shares
- `purchase_date`: Date of purchase
- `Purchase Price`: Price per share at purchase
- `sector`: Market sector

### Market Data

Market data is fetched in real-time using yfinance:

- Current stock prices
- Day change and percentage change
- Year-to-date (YTD) returns
- 52-week high/low
- Recent news articles

## Features

- ✅ **Real-time market data** from yfinance
- ✅ **Multi-agent collaboration** using LangGraph
- ✅ **Intelligent query routing** based on content
- ✅ **Response validation** to prevent hallucinations
- ✅ **Clean Streamlit UI** for easy interaction
- ✅ **Detailed agent activity tracking** for transparency
- ✅ **Support for 8 different clients** with unique portfolios

## Limitations

This is a prototype system with the following limitations:

- No user authentication
- No database persistence (data loaded from Excel each time)
- Simple news search (no advanced RAG)
- Rate limits on yfinance API calls
- Basic validation logic

## Future Enhancements

Potential improvements for production deployment:

- Add user authentication and authorization
- Implement database storage for portfolios
- Add advanced RAG for SEC filings and financial documents
- Implement caching for market data
- Add more sophisticated validation with fact-checking
- Support for multiple languages
- Historical portfolio performance analysis
- Automated portfolio rebalancing recommendations

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- Ensure you created a `.env` file with your API key
- Check that the `.env` file is in the project root directory

**"No module named 'langgraph'"**
- Run `pip install -r requirements.txt` to install all dependencies

**"Error loading portfolio"**
- Verify `portfolios.xlsx` is in the project root
- Check that the Excel file has the correct column structure

**Rate limit errors from yfinance**
- Reduce the number of stocks being queried
- Add delays between API calls if needed

## Contributing

This is a prototype system. For questions or issues, please contact the development team.

## License

Internal use only - Investment firm proprietary system.

---

**Powered by LangGraph, OpenAI GPT-4o-mini, and yfinance**
