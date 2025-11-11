# 🏗️ Portfolio Intelligence System Architecture

## 📋 Overview

This is a comprehensive AI-powered investment analysis platform with **4 main features** and **RAG integration** for market knowledge.

---

## 🎯 Four Core Features

### 1. 📊 Portfolio Intelligence
**Route:** `/portfolio`  
**Backend:** LangGraph Multi-Agent System  
**Purpose:** Real-time portfolio analysis with 5 specialized agents

**Agent Workflow:**
```
1. 🎯 Planner Agent → Query analysis & routing
2. 💼 Portfolio Agent → Retrieve holdings data
3. 📈 Market Agent → Get live market prices
4. 🤝 Synthesis Agent → Combine data & insights
5. ✅ Validator Agent → Verify accuracy
```

**Capabilities:**
- Show complete portfolio holdings
- Calculate total portfolio value
- Asset allocation analysis
- Sector exposure analysis
- Performance tracking
- Risk assessment

**API Endpoints:**
- `POST /api/query` - Main portfolio query endpoint
- `POST /api/sessions` - Session management
- `WebSocket /ws/{session_id}` - Real-time agent status updates

---

### 2. 📈 Stock Analysis (6-Agent AutoGen)
**Route:** `/stock-analysis`  
**Backend:** AutoGen Framework with 6 specialized agents  
**Purpose:** Deep stock analysis for trading decisions

**Agent Workflow:**
```
1. 🗂️ OrganiserAgent → Collect market data (Alpha Vantage)
2. ⚠️ RiskManager → Assess risk & position sizing
3. 📊 DataAnalyst → Fundamental analysis & web research (Tavily)
4. 📈 QuantitativeAnalyst → Technical indicators (RSI, MACD, etc.)
5. 🎯 StrategyDeveloper → Entry/exit strategy
6. 📋 ReportAgent → Final recommendation with confidence score
```

**Features:**
- Select from 24+ companies (AAPL, GOOGL, MSFT, etc.)
- 8 predefined trading questions
- Comprehensive analysis reports with:
  - BUY/SELL/HOLD recommendation
  - Confidence level (0-10)
  - Target price & stop loss
  - Technical & fundamental analysis
  - Risk assessment
  - Position sizing
  - Timeline recommendation

**API Endpoints:**
- `POST /api/analyze-stock` - Stock analysis endpoint

---

### 3. 💬 Enhanced Chat (with RAG Integration)
**Route:** `/chat`  
**Backend:** LangGraph + RAG Vector Store  
**Purpose:** Conversational interface with intelligent routing

**Smart Routing Logic:**
```javascript
// Detects question type and routes accordingly
const isGeneralMarket = !/CLT-00\d|my portfolio|holdings|position|client/i.test(query);

if (isGeneralMarket) {
  // General market questions → RAG System
  ragQuery(query, k=4);
} else {
  // Portfolio-specific questions → LangGraph Agents
  langgraphQuery(clientId, query);
}
```

**Capabilities:**

**A) Portfolio Questions (via LangGraph Agents):**
- "Show me my complete portfolio"
- "What's my total portfolio value?"
- "Which stocks do I own?"
- "What's my asset allocation?"
- "How is my tech sector performing?"

**B) General Market Questions (via RAG):**
- "What is a stock?"
- "Explain P/E ratio"
- "What is technical analysis?"
- "How does the stock market work?"
- Any educational question about stocks/investing

**RAG System Details:**
- **Vector Store:** FAISS (`vectorstore/db_faiss/`)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **LLM:** OpenAI GPT-4o-mini via LangChain RetrievalQA
- **Current Knowledge Base:** 2 documents
  1. `basics_stocks__what_they_are__main_types__and_how_they_di.txt`
  2. `valuation_price-to-earnings__p_e__ratio__definition__formula.txt`
- **Recommended Expansion:** 40-60 documents (see RAG_QUICK_START.md)

**API Endpoints:**
- `POST /api/query` - Portfolio questions (LangGraph)
- `POST /api/rag/query` - General market questions (RAG)
- `WebSocket /ws/{session_id}` - Real-time updates

---

### 4. 🤖 ML Stock Prediction
**Route:** `/stock-prediction` (future frontend integration)
**Backend:** Random Forest Machine Learning Model
**Purpose:** AI-powered stock buy/sell predictions based on technical indicators

**Model Details:**
- **Algorithm:** Random Forest Classifier
- **Model Storage:** `saved_models/` directory
- **Training:** Pre-trained on historical stock data
- **Scaling:** StandardScaler for feature normalization

**Input Features (9 technical indicators):**
```
1. Open         - Opening price
2. High         - High price
3. Low          - Low price
4. Close        - Closing price
5. Volume       - Trading volume
6. Return       - Return percentage
7. SMA_10       - 10-day Simple Moving Average
8. SMA_50       - 50-day Simple Moving Average
9. Volatility_10 - 10-day historical volatility
```

**Output Format:**
```json
{
  "prediction": "Buy" | "Don't Buy",
  "probability": 0.85,
  "confidence": "High" | "Medium" | "Low",
  "recommendation": "Strong buy signal with 85% probability"
}
```

**Confidence Levels:**
- **High:** probability ≥0.8 or ≤0.2
- **Medium:** probability ≥0.6 or ≤0.4
- **Low:** probability between 0.4-0.6

**API Endpoints:**
- `POST /api/predict-stock` - Stock prediction with ML model
- `GET /api/predict-stock/health` - Model health check

**Use Cases:**
- Quick buy/sell predictions based on technical data
- Complement to 6-agent AutoGen analysis
- Automated trading signal generation
- Backtesting strategy validation

---

## 🔄 System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                   FRONTEND (React + Vite)                         │
│                         Port: 3000                                │
└──────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┬──────────────┐
                │               │               │              │
                ▼               ▼               ▼              ▼
        ┌───────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Portfolio │   │  Stock   │   │ Enhanced │   │    ML    │
        │   Intel   │   │ Analysis │   │   Chat   │   │Prediction│
        └───────────┘   └──────────┘   └──────────┘   └──────────┘
                │               │         │      │            │
                │               │         │      │            │
                ▼               ▼         ▼      ▼            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 BACKEND (FastAPI on Port 8000)                      │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │LangGraph │  │ AutoGen  │  │   RAG    │  │   ML Model        │  │
│  │5 Agents  │  │6 Agents  │  │FAISS+LLM │  │Random Forest      │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                │         │          │              │
                ▼         ▼          ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────┐
        │PostgreSQL│  │  Alpha   │  │   OpenAI     │  │  Saved   │
        │Portfolio │  │ Vantage  │  │  GPT-4o-mini │  │  Models  │
        │   Data   │  │   API    │  │   + Tavily   │  │  (ML)    │
        └──────────┘  └──────────┘  └──────────────┘  └──────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework:** React 18.3.1 + Vite
- **Routing:** React Router DOM
- **Animations:** Framer Motion
- **Styling:** Tailwind CSS
- **Icons:** Lucide React

### Backend
- **Framework:** FastAPI (Python)
- **Agent Frameworks:**
  - LangGraph (Portfolio Intelligence)
  - AutoGen (Stock Analysis)
- **RAG:** LangChain + FAISS
- **Database:** PostgreSQL (portfolio data)

### AI/ML
- **LLM:** OpenAI GPT-4o-mini
- **Embeddings:** sentence-transformers
- **Web Search:** Tavily API (for DataAnalyst)
- **Market Data:** Alpha Vantage API
- **ML Model:** scikit-learn (Random Forest)
- **ML Persistence:** joblib (model serialization)
- **Data Processing:** pandas, numpy

---

## 📡 API Endpoints Summary

### Health & Root
- `GET /` - Root endpoint
- `GET /api/health` - Health check

### Portfolio Intelligence (LangGraph)
- `POST /api/query` - Portfolio analysis queries
- `POST /api/sessions` - Create new session
- `GET /api/sessions/{session_id}` - Get session status
- `WebSocket /ws/{session_id}` - Real-time agent updates

### Stock Analysis (AutoGen)
- `POST /api/analyze-stock` - Stock analysis with 6 agents

### RAG System
- `POST /api/rag/query` - General market knowledge queries

### ML Prediction
- `POST /api/predict-stock` - ML-based stock buy/sell prediction
- `GET /api/predict-stock/health` - Model health check

### Portfolio Data
- `GET /api/portfolio/{client_id}` - Get client portfolio
- `GET /api/portfolio/{client_id}/holdings` - Get holdings

---

## 🔐 Environment Variables

```bash
# Required API Keys
OPENAI_API_KEY=sk-...                    # OpenAI GPT-4o-mini
ALPHA_VANTAGE_API_KEY=...                # Market data
TAVILY_API_KEY=tvly-...                  # Web search (DataAnalyst)

# Database
DATABASE_URL=postgresql://...            # PostgreSQL connection

# Server Settings
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

---

## 🚀 Running the System

### Backend (Port 8000)
```bash
cd backends/langgraph_backend
conda activate portfolio-intel
uvicorn app.main:app --reload --port 8000
```

### Frontend (Port 3000)
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📊 Feature Comparison

| Feature | Portfolio Intelligence | Stock Analysis | Enhanced Chat | ML Prediction |
|---------|----------------------|----------------|---------------|---------------|
| **Backend** | LangGraph | AutoGen | LangGraph + RAG | Random Forest ML |
| **Agents** | 5 agents | 6 agents | 5 agents + RAG | ML Model |
| **Purpose** | Portfolio analysis | Trading decisions | Conversational Q&A | Buy/Sell signals |
| **Data Source** | PostgreSQL + Market | Alpha Vantage + Web | Portfolio DB + Knowledge Base | Technical indicators |
| **Output** | Structured insights | Trading recommendation | Natural language answers | Prediction + probability |
| **Real-time** | Yes (WebSocket) | No | Yes (WebSocket) | Yes (API) |
| **RAG** | No | No | Yes (for general questions) | No |

---

## 🎯 RAG Integration Details

### Current Status
✅ **Fully Integrated** into Enhanced Chat  
✅ **Smart Routing** between portfolio and market questions  
✅ **Source Citations** included in responses  
✅ **Backend Endpoint** operational at `/api/rag/query`

### Knowledge Base Location
```
rag_system/data_sources/raw_documents/
├── basics_stocks__what_they_are__main_types__and_how_they_di.txt
└── valuation_price-to-earnings__p_e__ratio__definition__formula.txt
```

### Expansion Recommendations
- **Current:** 2 documents (minimal coverage)
- **Target:** 40-60 documents (comprehensive coverage)
- **Topics to Add:**
  - Technical indicators (RSI, MACD, Moving Averages)
  - Fundamental analysis (EPS, P/E, PEG, ROE)
  - Investment strategies (Value, Growth, Momentum)
  - Risk management (Diversification, Position sizing)
  - Market concepts (Bull/Bear, Support/Resistance)

**See:** `RAG_QUICK_START.md` and `RAG_ENHANCEMENT_GUIDE.md` for expansion instructions

---

## 🎨 User Interface Navigation

```
Home (/)
├─ 📊 Portfolio Intelligence (/portfolio)
│   └─ Select Client → Ask Questions → View Agent Analysis
│
├─ 📈 Stock Analysis (/stock-analysis)
│   └─ Select Company → Choose Question → Get Trading Recommendation
│
├─ 💬 Enhanced Chat (/chat)
│   ├─ Portfolio Questions → LangGraph Agents
│   └─ Market Questions → RAG System
│
└─ 🤖 ML Stock Prediction (/stock-prediction) [Future Frontend]
    └─ Input Technical Indicators → Get ML Buy/Sell Signal
```

---

## 🔧 Maintenance & Troubleshooting

### Common Issues

1. **Model Client Initialization Error**
   - **Fixed:** All 6 AutoGen agents have error handling
   - **Location:** `src/agents/autogen/*.py`

2. **Port Conflicts**
   - **Backend:** Port 8000
   - **Frontend:** Port 3000
   - **Solution:** Change in `app.config` or `vite.config.js`

3. **Missing Dependencies**
   - **Required:** `tavily-python` for DataAnalyst
   - **Install:** `pip install tavily-python`

4. **RAG Returns No Results**
   - **Cause:** Limited knowledge base (only 2 documents)
   - **Solution:** Expand knowledge base using `add_documents.py`

5. **ML Model Not Found**
   - **Error:** "Model file not found in saved_models/"
   - **Solution:** Ensure Random Forest model files exist in `saved_models/` directory
   - **Files Required:** `random_forest_model.pkl`, `scaler.pkl`

---

## 📈 Future Enhancements

### Short-term (1-2 weeks)
- [ ] Expand RAG knowledge base to 40-60 documents
- [ ] Add source citation UI in ChatMessages component
- [ ] Improve error handling in agent workflows
- [ ] Build frontend UI for ML Stock Prediction feature
- [ ] Integrate ML predictions with AutoGen stock analysis

### Medium-term (1-2 months)
- [ ] Add portfolio performance charts
- [ ] Historical backtesting for strategies
- [ ] Multi-portfolio comparison
- [ ] Export analysis reports (PDF)

### Long-term (3+ months)
- [ ] Real-time price alerts
- [ ] Paper trading integration
- [ ] Mobile app (React Native)
- [ ] Advanced technical analysis tools
- [ ] ML model retraining pipeline with latest market data
- [ ] Ensemble ML models (Random Forest + XGBoost + LSTM)

---

## 📚 Documentation Files

- `README.md` - Project overview
- `QUICK_START.md` - Quick setup guide
- `RAG_QUICK_START.md` - RAG knowledge base expansion
- `RAG_ENHANCEMENT_GUIDE.md` - Detailed RAG improvement strategy
- `SYSTEM_ARCHITECTURE.md` (this file) - Complete system documentation

---

## 👥 Contributors

Built with ❤️ using AI-powered multi-agent systems

**Frameworks Used:**
- LangGraph (Portfolio Intelligence)
- AutoGen (Stock Analysis)
- LangChain (RAG System)

---

## 📄 License

[Your License Here]

---

**Last Updated:** October 28, 2025
