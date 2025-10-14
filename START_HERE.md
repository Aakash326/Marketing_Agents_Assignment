# 🚀 START HERE - Setup in 5 Minutes

## Current Issue: Python 3.13 Compatibility

You're using **Python 3.13**, which has compatibility issues with PyTorch/sentence-transformers.

**Solution**: Create a Python 3.11 environment.

---

## ⚡ Quick Setup (5 Commands)

Open your terminal and run these commands:

```bash
# 1. Create Python 3.11 environment
conda create -n portfolio-intel python=3.11 -y

# 2. Activate it
conda activate portfolio-intel

# 3. Navigate to project
cd /Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents

# 4. Install dependencies (takes 3-5 minutes)
pip install -r requirements.txt

# 5. Run the app
streamlit run app.py
```

**That's it!** Your browser should open with the app.

---

## ✅ Verification

After running the commands, verify:

```bash
# Check Python version (should be 3.11.x)
python --version

# Test imports
python -c "import streamlit; print('✅ Ready to go!')"
```

---

## 🎯 First Test

Once the app opens:

1. **Select client**: CLT-001
2. **Ask**: "What stocks do I own?"
3. **See results**: Should show portfolio holdings

If this works, you're all set! ✅

---

## 📚 What Next?

### Option A: Use immediately
- Start testing with different queries
- See `QUICK_REFERENCE.md` for example queries

### Option B: Enable all features
- Run knowledge base ingestion: `python ingest_knowledge.py CLT-001`
- Update app.py: See `APP_UPDATE_GUIDE.md`

---

## 📖 Documentation Quick Links

| If you want to... | Read this file |
|-------------------|----------------|
| **Get started NOW** | `START_HERE.md` ← You are here |
| **Fix installation issues** | `SETUP_STEPS.md` |
| **Understand all features** | `FINAL_SUMMARY.md` |
| **Daily usage reference** | `QUICK_REFERENCE.md` |
| **Update the UI** | `APP_UPDATE_GUIDE.md` |

---

## 🆘 Troubleshooting

### Command not working?

**Check 1**: Is conda initialized?
```bash
which conda
# If nothing shows, run: conda init bash
```

**Check 2**: Are you in the right directory?
```bash
pwd
# Should show: /Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents
```

**Check 3**: Is environment activated?
```bash
conda env list
# Should show * next to portfolio-intel
```

### Still having issues?

See `INSTALLATION_GUIDE.md` for detailed troubleshooting.

---

## 💡 Pro Tip

**Bookmark this command** for daily use:

```bash
conda activate portfolio-intel && cd /Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents && streamlit run app.py
```

This activates environment, navigates to project, and starts the app in one command!

---

## 🎉 You're Ready!

After running the 5 commands above, you'll have:

- ✅ Python 3.11 environment
- ✅ All dependencies installed
- ✅ App running in browser
- ✅ Ready to test all features

**Time to complete**: ~5 minutes (mostly waiting for installation)

---

**Let's get started!** Open your terminal and run the 5 commands above. 🚀
