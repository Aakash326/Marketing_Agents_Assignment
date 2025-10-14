# Quick Reference Card

## 🚀 Daily Usage

### Start Working

```bash
# 1. Open terminal
# 2. Activate environment
conda activate portfolio-intel

# 3. Navigate to project
cd /Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents

# 4. Run application
streamlit run app.py
```

### Stop Application

Press `Ctrl+C` in terminal, or close the browser tab.

---

## 📝 Common Commands

| Task | Command |
|------|---------|
| **Start app** | `streamlit run app.py` |
| **Ingest data** | `python ingest_knowledge.py CLT-001` |
| **Check KB stats** | `python -c "from src.tools.knowledge_ingestion import get_knowledge_base_stats; get_knowledge_base_stats()"` |
| **Activate env** | `conda activate portfolio-intel` |
| **Deactivate env** | `conda deactivate` |
| **Check Python** | `python --version` (should be 3.11.x) |

---

## 🧪 Test Queries

| Query Type | Example |
|------------|---------|
| **Basic** | "What stocks do I own?" |
| **Market** | "What's the price of AAPL?" |
| **Collaboration** | "How does Microsoft news affect my portfolio?" |
| **Follow-up** | "Tell me more about the first one" |
| **Clarification** | "How's that stock doing?" |

---

## 📊 Available Clients

- CLT-001
- CLT-002
- CLT-003
- CLT-004
- CLT-005
- CLT-007
- CLT-009
- CLT-010

---

## 🗂️ Project Structure

```
Assignment-marketing-agents/
├── app.py                    # Main Streamlit app
├── portfolios.xlsx           # Portfolio data
├── requirements.txt          # Dependencies
├── ingest_knowledge.py       # KB ingestion
├── src/                      # Source code
│   ├── nodes/               # Agent nodes
│   ├── tools/               # Utilities
│   └── graph/               # Workflow
├── sec_filings/             # Downloaded filings
└── knowledge_base/          # Vector DB
```

---

## ⚠️ Important Notes

1. **Always activate environment first**: `conda activate portfolio-intel`
2. **Python must be 3.11.x** (not 3.13)
3. **First query may be slow** (loading models)
4. **SEC fetching takes ~10 seconds** (first time per ticker)
5. **Knowledge base is optional** (but recommended)

---

## 🔧 Quick Fixes

| Problem | Solution |
|---------|----------|
| "No module found" | `conda activate portfolio-intel` |
| "Wrong Python version" | Check: `python --version` (must be in env) |
| App won't start | `pip install -r requirements.txt` |
| PyTorch errors | Wrong Python version (need 3.11) |
| Slow queries | Normal first time (model loading) |

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `SETUP_STEPS.md` | Initial setup guide |
| `INSTALLATION_GUIDE.md` | Detailed installation |
| `APP_UPDATE_GUIDE.md` | How to update app.py |
| `FINAL_SUMMARY.md` | Complete feature overview |
| `QUICK_REFERENCE.md` | This file |

---

## 💡 Pro Tips

1. **Keep terminal open** while app is running
2. **Use browser refresh** if app seems stuck
3. **Check terminal** for error messages
4. **Clear history button** resets conversation
5. **Ingestion can run in background** while testing app

---

## 🎯 Feature Status

| Feature | Status | Requires |
|---------|--------|----------|
| Portfolio queries | ✅ Ready | Nothing |
| Market data | ✅ Ready | Nothing |
| SEC filings | ✅ Ready | On-demand download |
| Knowledge base/RAG | ⚠️ Optional | Run `ingest_knowledge.py` |
| Collaboration | ✅ Ready | Nothing |
| Session memory | ✅ Ready | Update app.py |
| Clarification | ✅ Ready | Update app.py |

---

## 🔄 Environment Quick Check

```bash
# Run this to verify everything is working
conda activate portfolio-intel
python --version  # Should show 3.11.x
python -c "import streamlit, langgraph, chromadb; print('✅ All OK')"
```

If all checks pass, you're ready to go!

---

## 📞 Getting Help

1. Check `FINAL_SUMMARY.md` for overview
2. Check `INSTALLATION_GUIDE.md` for setup issues
3. Check terminal output for error messages
4. Check `TROUBLESHOOTING.md` for common fixes

---

**Remember**: Always run `conda activate portfolio-intel` before working! 🎯
