# Python 3.11 Setup Steps

## Follow these steps exactly:

### Step 1: Create Python 3.11 Environment

Open your terminal and run:

```bash
conda create -n portfolio-intel python=3.11 -y
```

Wait for it to complete (~1-2 minutes).

### Step 2: Activate the Environment

```bash
conda activate portfolio-intel
```

You should see `(portfolio-intel)` appear in your terminal prompt.

### Step 3: Verify Python Version

```bash
python --version
```

Should show: `Python 3.11.x`

### Step 4: Install Dependencies

```bash
cd /Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents
pip install -r requirements.txt
```

This will take **3-5 minutes** as it downloads:
- sentence-transformers models (~500MB)
- PyTorch
- ChromaDB
- All other dependencies

### Step 5: Verify Installation

Test each component:

```bash
# Test Streamlit
python -c "import streamlit; print('✅ Streamlit:', streamlit.__version__)"

# Test LangGraph
python -c "import langgraph; print('✅ LangGraph:', langgraph.__version__)"

# Test SEC tools
python -c "from sec_edgar_downloader import Downloader; print('✅ SEC tools: OK')"

# Test ChromaDB
python -c "import chromadb; print('✅ ChromaDB:', chromadb.__version__)"

# Test Sentence Transformers (this will download model on first run)
python -c "from sentence_transformers import SentenceTransformer; print('✅ Transformers: OK')"
```

All should print ✅ without errors.

### Step 6: Run the Application

```bash
streamlit run app.py
```

The app should open in your browser at `http://localhost:8501`

---

## Quick Test

Once the app is running, try:

1. Select client: `CLT-001`
2. Query: `What stocks do I own?`
3. Should show portfolio holdings without errors

---

## Optional: Populate Knowledge Base

After the app works, you can populate the knowledge base:

```bash
# Make sure you're in the portfolio-intel environment
conda activate portfolio-intel

# Run ingestion (takes ~5-10 minutes)
python ingest_knowledge.py CLT-001
```

This downloads SEC filings and stores them in the vector database.

---

## Troubleshooting

### "conda: command not found"

Make sure Anaconda/Miniconda is installed and initialized:

```bash
# Check if conda is installed
which conda

# If not found, initialize conda
conda init bash  # or 'conda init zsh' if using zsh
```

Then restart your terminal.

### "Environment already exists"

If you get an error that the environment already exists:

```bash
# Remove old environment
conda env remove -n portfolio-intel -y

# Create fresh environment
conda create -n portfolio-intel python=3.11 -y
```

### Dependencies fail to install

If pip install fails:

```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing in stages
pip install streamlit langgraph langchain-openai pandas openpyxl yfinance
pip install sec-edgar-downloader chromadb sentence-transformers
```

### Still getting PyTorch errors

If you still see PyTorch-related errors:

```bash
# Check Python version INSIDE the environment
conda activate portfolio-intel
python --version  # MUST show 3.11.x

# If it shows 3.13, environment wasn't activated
# Make sure to run: conda activate portfolio-intel
```

---

## Environment Management

### Deactivate environment

```bash
conda deactivate
```

### Reactivate for future use

```bash
conda activate portfolio-intel
```

### List all conda environments

```bash
conda env list
```

### Delete environment (if needed)

```bash
conda env remove -n portfolio-intel
```

---

## Summary

**Commands to run:**

```bash
# 1. Create environment
conda create -n portfolio-intel python=3.11 -y

# 2. Activate it
conda activate portfolio-intel

# 3. Verify Python version
python --version

# 4. Install dependencies
cd /Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents
pip install -r requirements.txt

# 5. Run application
streamlit run app.py
```

**That's it!** 🎉

Once you see the Streamlit app open in your browser, you're all set!
