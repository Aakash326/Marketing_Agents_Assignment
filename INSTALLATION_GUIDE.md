# Installation Guide - New Features

## ⚠️ Important: Install New Dependencies First!

Before running the updated system, you **must** install the new dependencies.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `sec-edgar-downloader==5.0.2` - For SEC filings
- `chromadb==0.4.22` - For vector database
- `sentence-transformers==2.3.1` - For embeddings

**Installation may take 2-3 minutes** as sentence-transformers downloads ML models.

## Step 2: Verify Installation

```bash
python -c "from sec_edgar_downloader import Downloader; print('✅ SEC tools OK')"
python -c "import chromadb; print('✅ ChromaDB OK')"
python -c "from sentence_transformers import SentenceTransformer; print('✅ Transformers OK')"
```

All three commands should print "✅ OK" without errors.

## Step 3: Test Basic Functionality

```bash
# Test SEC tools
python -c "from src.tools.sec_tools import fetch_latest_filing; print('✅ SEC module imports')"

# Test RAG tools
python -c "from src.tools.rag_tools import SimpleKnowledgeBase; print('✅ RAG module imports')"

# Test collaboration
python -c "from src.nodes.collaboration_node import collaboration_node; print('✅ Collaboration imports')"
```

## Step 4: Optional - Populate Knowledge Base

```bash
# This step is OPTIONAL but recommended
# Takes ~5-10 minutes for one client
python ingest_knowledge.py CLT-001
```

**Note**: You can skip this step and still use the system. SEC filings will be fetched on-demand, and RAG search will simply return no results if knowledge base is empty.

## Step 5: Run the Application

```bash
streamlit run app.py
```

## Troubleshooting

### "No module named 'sec_edgar_downloader'"

**Solution**: Run `pip install -r requirements.txt`

### "No module named 'chromadb'"

**Solution**: Run `pip install -r requirements.txt`

### ChromaDB SQLite errors

**Solution**: Delete and recreate knowledge base:
```bash
rm -rf knowledge_base/
python ingest_knowledge.py CLT-001
```

### Slow first query

**Cause**: Sentence transformers loading model for first time

**Solution**: Normal behavior - subsequent queries will be faster

### SEC filing download fails

**Possible causes**:
1. No internet connection
2. SEC website down
3. Ticker doesn't file 10-Ks (e.g., some ETFs)

**Solution**: System will gracefully skip SEC data and continue

## What Works Without Installation

If you **don't** install new dependencies:

- ✅ Basic portfolio queries still work
- ✅ Market data still works
- ✅ Original 2 features work fine

**But these won't work**:
- ❌ SEC filings integration
- ❌ Knowledge base / RAG
- ❌ Enhanced features using these tools

## Quick Start (Minimum Setup)

If you just want to test quickly:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run app (skip knowledge base ingestion for now)
streamlit run app.py

# 3. Try a basic query
# "What stocks do I own?" - Should work immediately

# 4. Try a market query
# "What's the price of AAPL?" - Should work immediately

# 5. SEC will fetch on-demand (takes a few seconds first time)
```

## Full Setup (Recommended)

For best experience with all features:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Populate knowledge base for one client
python ingest_knowledge.py CLT-001

# 3. Check knowledge base stats
python -c "from src.tools.knowledge_ingestion import get_knowledge_base_stats; get_knowledge_base_stats()"

# 4. Run application
streamlit run app.py

# 5. Test features:
#    - Basic: "What stocks do I own?"
#    - Market: "What's AAPL price?"
#    - Collaboration: "How does Microsoft news affect my portfolio?"
#    - Session: Ask follow-up "Tell me more"
#    - Clarification: "How's that stock?"
```

## Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] All import tests pass
- [ ] App starts without errors (`streamlit run app.py`)
- [ ] Basic query works ("What stocks do I own?")
- [ ] Market query works ("What's AAPL price?")
- [ ] Optional: Knowledge base populated
- [ ] Optional: SEC filings fetch successfully

---

**Ready to go!** 🎉

If you encounter any issues, check the Troubleshooting section above.
