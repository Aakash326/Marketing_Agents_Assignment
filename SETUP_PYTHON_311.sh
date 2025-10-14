#!/bin/bash
# Setup script for Python 3.11 environment
# Run this script: bash SETUP_PYTHON_311.sh

echo "================================================"
echo "Setting up Portfolio Intelligence System"
echo "================================================"
echo ""

# Step 1: Create conda environment with Python 3.11
echo "Step 1: Creating conda environment with Python 3.11..."
conda create -n portfolio-intel python=3.11 -y

if [ $? -ne 0 ]; then
    echo "❌ Failed to create conda environment"
    echo "Please make sure conda is installed and initialized"
    exit 1
fi

echo "✅ Environment created successfully"
echo ""

# Step 2: Activate environment (user needs to do this manually)
echo "Step 2: Activate the environment"
echo "Run this command:"
echo "    conda activate portfolio-intel"
echo ""
echo "Press Enter after you've activated the environment..."
read

# Step 3: Install dependencies
echo "Step 3: Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Step 4: Verify installation
echo "Step 4: Verifying installation..."
python -c "import streamlit; print('✅ Streamlit:', streamlit.__version__)"
python -c "import langgraph; print('✅ LangGraph:', langgraph.__version__)"
python -c "from sec_edgar_downloader import Downloader; print('✅ SEC Edgar Downloader: OK')"
python -c "import chromadb; print('✅ ChromaDB:', chromadb.__version__)"
python -c "from sentence_transformers import SentenceTransformer; print('✅ Sentence Transformers: OK')"

echo ""
echo "================================================"
echo "Setup Complete! 🎉"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Make sure you're in the portfolio-intel environment:"
echo "   conda activate portfolio-intel"
echo ""
echo "2. Optional - Populate knowledge base (takes ~5-10 min):"
echo "   python ingest_knowledge.py CLT-001"
echo ""
echo "3. Run the application:"
echo "   streamlit run app.py"
echo ""
