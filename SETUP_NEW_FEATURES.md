# Quick Setup Guide - New Features

## 🚀 Get Started with SEC Filings & RAG in 3 Steps

### Step 1: Install New Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `sec-edgar-downloader` - SEC filing fetcher
- `chromadb` - Vector database
- `sentence-transformers` - Embedding models (no API key needed!)

### Step 2: Populate Knowledge Base (Optional but Recommended)

```bash
# Ingest SEC filings for one client (takes ~5-10 minutes)
python ingest_knowledge.py CLT-001
```

**What this does:**
1. Reads CLT-001 portfolio holdings
2. Downloads 10-K SEC filings for each stock
3. Chunks and stores in vector database
4. Creates embeddings for semantic search

**Note**: This step is optional. The system will still work without it, but won't have RAG-powered context.

### Step 3: Run the Application

```bash
streamlit run app.py
```

**That's it!** The new features are automatically integrated.

---

## 🧪 Test the New Features

### Test SEC Filings

Ask questions that would benefit from SEC filing data:

```
"What are the risk factors for Microsoft?"
"Tell me about the risks in my tech holdings"
"What does the 10-K say about NVDA's business?"
```

The system will:
- ✅ Automatically fetch 10-K filings
- ✅ Extract risk factors section
- ✅ Include in analysis

### Test RAG (Requires Step 2)

After ingesting data, try semantic search:

```
"What are the main business risks in my portfolio?"
"Tell me about semiconductor supply chain issues"
"What regulatory concerns do my holdings have?"
```

The system will:
- ✅ Search knowledge base semantically
- ✅ Find relevant SEC filing sections
- ✅ Provide context-aware answers

---

## 📊 What You'll See

### Before (Old System):
```
User: "What are the risks with Microsoft?"

Response:
"Microsoft (MSFT) is currently trading at $415.50 (+2.3% today).
Recent news: Microsoft announces AI partnership..."
```

### After (With New Features):
```
User: "What are the risks with Microsoft?"

Response:
"Microsoft (MSFT) is currently trading at $415.50 (+2.3% today).

SEC Filing Risk Factors (10-K):
- Competition from cloud providers including Amazon and Google
- Cybersecurity threats and data privacy regulations
- Dependence on enterprise customers...

Recent news: Microsoft announces AI partnership...

Relevant context from knowledge base:
[Cloud computing market analysis...]
[AI regulation considerations...]
```

---

## 🎯 Which Features Are Active?

### Always Active (No Setup Required):
- ✅ SEC filing fetching (on-demand)
- ✅ Risk factor extraction
- ✅ Basic market data
- ✅ News fetching

### Active After Ingestion:
- ✅ RAG semantic search
- ✅ Knowledge base context
- ✅ Historical filing analysis

---

## ⚡ Quick Tips

### Speed Up Queries
First query with SEC fetching takes ~10 seconds. Subsequent queries are faster (cached).

### Manage Storage
```bash
# Check knowledge base size
du -sh knowledge_base/

# Check SEC filings size
du -sh sec_filings/
```

### Re-ingest Data
When new SEC filings are released:
```bash
python ingest_knowledge.py CLT-001
```

### Clear Everything
Start fresh:
```bash
rm -rf knowledge_base/
rm -rf sec_filings/
python ingest_knowledge.py CLT-001
```

---

## 🔍 Verify Installation

### Check Dependencies
```python
# Test SEC tools
from src.tools.sec_tools import fetch_latest_filing
print("✅ SEC tools imported")

# Test RAG
from src.tools.rag_tools import SimpleKnowledgeBase
kb = SimpleKnowledgeBase()
stats = kb.get_stats()
print(f"✅ RAG active. Documents: {stats['total_documents']}")
```

### Check Knowledge Base
```bash
# After ingestion, check stats
python -c "from src.tools.knowledge_ingestion import get_knowledge_base_stats; get_knowledge_base_stats()"
```

Expected output:
```
============================================================
Knowledge Base Statistics
============================================================
Collection: portfolio_knowledge
Total Documents: [number of chunks]
============================================================
```

---

## 🆘 Common Issues

### "No module named 'chromadb'"
**Solution**: Run `pip install -r requirements.txt`

### "SEC filing not found"
**Cause**: Some ETFs/bonds don't file 10-Ks
**Solution**: Normal - system will skip and continue

### "Knowledge base empty"
**Cause**: Didn't run ingestion script
**Solution**: Run `python ingest_knowledge.py CLT-001`

### Slow first query
**Cause**: First SEC fetch takes time
**Solution**: Normal - subsequent queries faster

---

## 📈 Next Steps

Once setup is complete:

1. **Test basic queries** - Verify SEC data appears
2. **Test RAG queries** - Verify semantic search works
3. **Ingest more clients** - `python ingest_knowledge.py CLT-002 CLT-003`
4. **Explore advanced features** - See [NEW_FEATURES.md](NEW_FEATURES.md)

---

## ✅ Setup Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run ingestion (optional): `python ingest_knowledge.py CLT-001`
- [ ] Start app: `streamlit run app.py`
- [ ] Test SEC query: "What are Microsoft's risk factors?"
- [ ] Test RAG query: "What are the main risks in my portfolio?"
- [ ] Verify responses include SEC filing data
- [ ] Check knowledge base stats

---

**You're all set!** 🎉

The system now has:
- ✅ SEC filings integration
- ✅ Vector database / RAG
- ✅ Semantic search
- ✅ Automatic context augmentation

See [NEW_FEATURES.md](NEW_FEATURES.md) for detailed documentation.
