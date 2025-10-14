# New Features Documentation

This document describes the 5 critical features added to the Portfolio & Market Intelligence System.

---

## ✅ FEATURE 1: SEC Filings Integration

### What It Does
Automatically fetches and analyzes SEC filings (10-K, 10-Q, 8-K) for stocks in client portfolios, with special focus on risk factors.

### Implementation

**Files Created:**
- [src/tools/sec_tools.py](src/tools/sec_tools.py) - SEC filing fetcher and parser

**Key Functions:**
- `fetch_latest_filing(ticker, filing_type)` - Downloads SEC filings
- `extract_risk_factors(filing_text)` - Extracts risk factors section
- `format_sec_data_for_llm(sec_data)` - Formats for LLM consumption

**Integration:**
- Market node automatically fetches 10-K filings for top 2 holdings
- Risk factors are included in market analysis
- Cached locally to avoid repeated downloads

### Usage

SEC data is automatically fetched when market agent is activated:

```python
# User asks about a stock
User: "What are the risks with my Microsoft holdings?"

# System automatically:
# 1. Identifies MSFT in portfolio
# 2. Fetches latest 10-K filing
# 3. Extracts risk factors section
# 4. Includes in analysis
```

### Benefits
- **Regulatory insight**: Understand company-disclosed risks
- **Compliance**: Based on official SEC filings
- **Automatic**: No manual filing lookup needed

---

## ✅ FEATURE 2: Knowledge Base / RAG

### What It Does
Vector database for storing and semantically searching documents (SEC filings, news, notes) using RAG (Retrieval-Augmented Generation).

### Implementation

**Files Created:**
- [src/tools/rag_tools.py](src/tools/rag_tools.py) - ChromaDB knowledge base
- [src/tools/knowledge_ingestion.py](src/tools/knowledge_ingestion.py) - Data ingestion utilities
- [ingest_knowledge.py](ingest_knowledge.py) - Ingestion script

**Key Components:**
- `SimpleKnowledgeBase` class - Manages vector database
- Uses sentence-transformers for embeddings (no API key needed)
- ChromaDB for persistent storage
- Semantic search with configurable results

### Setup

**Step 1: Install dependencies** (already in requirements.txt):
```bash
pip install -r requirements.txt
```

**Step 2: Ingest data into knowledge base**:
```bash
# Ingest for one client
python ingest_knowledge.py CLT-001

# Ingest for multiple clients
python ingest_knowledge.py CLT-001 CLT-002 CLT-003
```

**Step 3: Use the system** (automatic):
```bash
streamlit run app.py
```

### How It Works

1. **Ingestion**: SEC filings are chunked and stored with embeddings
2. **Query**: User asks a question
3. **Search**: System searches knowledge base semantically
4. **Augment**: Relevant context is added to LLM prompt
5. **Generate**: LLM generates answer with context

### Usage Example

```python
# After ingestion
User: "What are the main business risks for companies in my portfolio?"

# System:
# 1. Searches knowledge base for "business risks"
# 2. Retrieves relevant SEC filing chunks
# 3. Provides answer based on actual filings
```

### Knowledge Base Stats

Check current status:
```python
from src.tools.rag_tools import SimpleKnowledgeBase

kb = SimpleKnowledgeBase()
stats = kb.get_stats()
print(stats)  # {'total_documents': 150, 'collection_name': 'portfolio_knowledge'}
```

### Benefits
- **Semantic search**: Find relevant info even with different wording
- **Persistent**: Data stored locally, no repeated fetching
- **Scalable**: Add news, notes, research reports, etc.
- **No API costs**: Uses local embedding models

---

## 🎯 How These Features Work Together

### Complete Analysis Flow

```
User Query
    ↓
Planner Agent (decides what's needed)
    ↓
Portfolio Agent (if needed)
    ↓
Market Agent
    ├── Fetch real-time prices (yfinance)
    ├── Fetch news (yfinance)
    ├── 🆕 Fetch SEC filings (SEC Edgar)
    └── 🆕 Search knowledge base (RAG)
    ↓
Validator Agent
    ↓
Response to User
```

### Example: Complete Analysis

**User**: "How are tech stocks performing in my portfolio?"

**System Response** (enriched with new features):

```
Your tech holdings analysis:

Current Holdings:
- MSFT: $415.50 (+2.3% today) ✓ From market data
- NVDA: $127.45 (-1.2% today) ✓ From market data

Performance:
- MSFT YTD: +15.2%
- NVDA YTD: +180.5%

Recent News:
- [MSFT news summary] ✓ From yfinance

🆕 SEC Filing Risk Factors (from knowledge base):
- MSFT 10-K: "Competition from cloud providers..."
- NVDA 10-K: "Semiconductor supply chain risks..."

🆕 Relevant Context:
[Semiconductor market analysis from previous ingestion]
```

---

## 📊 Data Storage Locations

```
project/
├── sec_filings/               # SEC Edgar downloads
│   └── sec-edgar-filings/
│       ├── MSFT/
│       ├── NVDA/
│       └── ...
│
├── knowledge_base/            # ChromaDB vector database
│   ├── chroma.sqlite3
│   └── [embedding data]
│
└── portfolios.xlsx            # Client portfolio data
```

---

## 🔧 Configuration Options

### SEC Filings

Customize in [src/tools/sec_tools.py](src/tools/sec_tools.py):

```python
# Change filing type
filing = fetch_latest_filing(ticker, "10-Q")  # Quarterly instead of annual

# Adjust text length
"text": text[:100000]  # More text (default: 50k chars)
```

### RAG Search

Customize in [src/nodes/market_node.py](src/nodes/market_node.py):

```python
# More search results
kb_results = kb.search(query, n_results=5)  # Default: 3

# Different chunk size in rag_tools.py
max_chunk_size = 2000  # Default: 1000
```

---

## 🧪 Testing New Features

### Test SEC Filings

```python
from src.tools.sec_tools import fetch_latest_filing, extract_risk_factors

# Fetch filing
filing = fetch_latest_filing("MSFT", "10-K")
print(filing.get("success"))

# Extract risks
if filing.get("success"):
    risks = extract_risk_factors(filing["text"])
    print(risks[:500])
```

### Test RAG

```python
from src.tools.rag_tools import SimpleKnowledgeBase

# Search
kb = SimpleKnowledgeBase()
results = kb.search("What are the main risks?", n_results=3)

for result in results:
    print(f"Ticker: {result['metadata'].get('ticker')}")
    print(f"Text: {result['text'][:200]}\n")
```

### Test End-to-End

```bash
streamlit run app.py
```

Try these queries:
- "What are the risk factors for companies in my portfolio?"
- "How do SEC filings describe business risks?"
- "What compliance issues are mentioned in my holdings?"

---

## 🚨 Important Notes

### SEC Filing Rate Limits
- SEC has rate limits (10 requests/second)
- Script adds 2-second delays between requests
- First ingestion takes ~5-10 minutes per client
- Subsequent runs are faster (cached locally)

### Knowledge Base Storage
- ChromaDB stores data in `./knowledge_base/`
- Can grow large with many filings (~100MB per client)
- Clear with: `kb.clear()` if needed

### Performance
- SEC fetching adds ~5-10 seconds to first query
- RAG search adds ~1-2 seconds per query
- Consider: Only fetch for key holdings (current: top 2)

---

## 🔄 Updating Data

### Re-ingest SEC Filings

When new filings are available:

```bash
# Re-run ingestion (will update existing data)
python ingest_knowledge.py CLT-001
```

### Clear Knowledge Base

Start fresh:

```python
from src.tools.rag_tools import SimpleKnowledgeBase

kb = SimpleKnowledgeBase()
kb.clear()  # Deletes all documents
```

Then re-ingest:
```bash
python ingest_knowledge.py CLT-001
```

---

## 📈 Future Enhancements

Potential additions (not implemented yet):

1. **More Document Types**
   - Analyst reports
   - News articles (full text, not just headlines)
   - Research notes

2. **Advanced Parsing**
   - Extract specific sections (Management Discussion, Financial Data)
   - Table extraction from filings

3. **Scheduled Updates**
   - Cron job to auto-fetch new filings
   - Webhook for new filing notifications

4. **Multi-modal**
   - Image/chart extraction from PDFs
   - Financial table analysis

---

## 🆘 Troubleshooting

### SEC Download Fails

**Error**: `Filing not found`

**Solution**:
- Check ticker symbol is correct
- Some ETFs don't file 10-Ks (use `filing_type="N-CSR"` for funds)
- Check internet connection

### ChromaDB Errors

**Error**: `No such table: collections`

**Solution**:
```bash
rm -rf knowledge_base/
python ingest_knowledge.py CLT-001
```

### Slow Performance

**Solution**:
- Reduce SEC filings fetched (currently: top 2)
- Reduce RAG search results (currently: 3)
- Consider caching SEC data more aggressively

---

## 📚 Additional Resources

- [SEC Edgar API](https://www.sec.gov/edgar/sec-api-documentation)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [SEC Edgar Downloader](https://github.com/jadchaar/sec-edgar-downloader)

---

**Features 1 & 2 Complete!** ✅

These features are now fully integrated into the system and ready to use.
