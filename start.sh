#!/bin/bash

# Portfolio Intelligence System Startup Script
# This script activates the conda environment and starts both backend and frontend

echo "🚀 Starting Portfolio Intelligence System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to check if conda is available
check_conda() {
    if ! command -v conda &> /dev/null; then
        echo -e "${RED}❌ Conda is not installed or not in PATH${NC}"
        echo "Please install Anaconda or Miniconda first"
        exit 1
    fi
}

# Function to activate conda environment
activate_env() {
    echo -e "${BLUE}🔧 Activating conda environment 'portfolio-intel'...${NC}"

    # Initialize conda for bash
    eval "$(conda shell.bash hook)"

    # Activate environment
    conda activate portfolio-intel

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Conda environment activated${NC}"
        echo ""
    else
        echo -e "${RED}❌ Failed to activate conda environment${NC}"
        echo "Make sure 'portfolio-intel' environment exists"
        echo "Create it with: conda create -n portfolio-intel python=3.11"
        exit 1
    fi
}

# Function to start backend
start_backend() {
    echo -e "${BLUE}🔷 Starting Backend Server...${NC}"
    cd "$DIR/backend"

    # Check if uvicorn is installed
    if ! python -c "import uvicorn" 2>/dev/null; then
        echo -e "${RED}❌ Uvicorn not installed${NC}"
        echo "Installing backend dependencies..."
        pip install -r requirements.txt
    fi

    # Start backend in background
    nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
    BACKEND_PID=$!

    echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
    echo "   Backend URL: http://localhost:8000"
    echo "   Backend logs: backend.log"
    echo ""

    # Wait a moment for backend to start
    sleep 2
}

# Function to start frontend
start_frontend() {
    echo -e "${BLUE}🔶 Starting Frontend Server...${NC}"
    cd "$DIR/frontend"

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
        npm install
    fi

    # Start frontend in background
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!

    echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
    echo "   Frontend URL: http://localhost:3000"
    echo "   Frontend logs: frontend.log"
    echo ""
}

# Function to check if services are running
check_services() {
    echo -e "${BLUE}🔍 Checking services...${NC}"
    sleep 3

    # Check backend
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend is running${NC}"
    else
        echo -e "${YELLOW}⚠️  Backend might still be starting...${NC}"
    fi

    # Check frontend
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend is running${NC}"
    else
        echo -e "${YELLOW}⚠️  Frontend might still be starting...${NC}"
    fi

    echo ""
}

# Main execution
main() {
    # Check if conda is available
    check_conda

    # Activate conda environment
    activate_env

    # Start backend
    start_backend

    # Start frontend
    start_frontend

    # Check if services are running
    check_services

    # Success message
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🎉 Portfolio Intelligence System is now running!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}📱 Access the application:${NC}"
    echo "   🌐 Frontend: http://localhost:3000"
    echo "   🔧 Backend:  http://localhost:8000"
    echo "   📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo -e "${BLUE}📋 Logs:${NC}"
    echo "   Backend:  tail -f $DIR/backend.log"
    echo "   Frontend: tail -f $DIR/frontend.log"
    echo ""
    echo -e "${BLUE}🛑 To stop:${NC}"
    echo "   Run: $DIR/stop.sh"
    echo ""
    echo -e "${YELLOW}💡 Tip: Keep this terminal open or run in background${NC}"
    echo ""
}

# Run main function
main
