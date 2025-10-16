#!/bin/bash

# Backend Startup Script
# This script starts just the backend server

echo "🔷 Starting Backend Server..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if in conda environment
if [[ "$CONDA_DEFAULT_ENV" != "portfolio-intel" ]]; then
    echo -e "${YELLOW}⚠️  Warning: portfolio-intel environment is not activated${NC}"
    echo "Activating environment..."
    eval "$(conda shell.bash hook)"
    conda activate portfolio-intel
fi

# Check if uvicorn is installed
if ! python -c "import uvicorn" 2>/dev/null; then
    echo -e "${YELLOW}Installing backend dependencies...${NC}"
    pip install -r requirements.txt
fi

echo -e "${GREEN}✅ Environment ready${NC}"
echo ""
echo -e "${BLUE}Starting FastAPI server...${NC}"
echo "Backend URL: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
