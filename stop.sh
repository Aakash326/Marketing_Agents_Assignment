#!/bin/bash

# Portfolio Intelligence System Stop Script

echo "🛑 Stopping Portfolio Intelligence System..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to stop backend
stop_backend() {
    echo -e "${BLUE}Stopping Backend...${NC}"

    # Find and kill uvicorn processes
    BACKEND_PIDS=$(pgrep -f "uvicorn main:app")

    if [ -z "$BACKEND_PIDS" ]; then
        echo -e "${BLUE}Backend is not running${NC}"
    else
        for PID in $BACKEND_PIDS; do
            kill $PID 2>/dev/null
            echo -e "${GREEN}✅ Stopped backend (PID: $PID)${NC}"
        done
    fi
}

# Function to stop frontend
stop_frontend() {
    echo -e "${BLUE}Stopping Frontend...${NC}"

    # Find and kill vite/node processes running on port 3000
    FRONTEND_PIDS=$(lsof -ti:3000)

    if [ -z "$FRONTEND_PIDS" ]; then
        echo -e "${BLUE}Frontend is not running${NC}"
    else
        for PID in $FRONTEND_PIDS; do
            kill $PID 2>/dev/null
            echo -e "${GREEN}✅ Stopped frontend (PID: $PID)${NC}"
        done
    fi
}

# Function to clean up log files
cleanup_logs() {
    echo -e "${BLUE}Cleaning up logs...${NC}"

    if [ -f "$DIR/backend.log" ]; then
        rm "$DIR/backend.log"
        echo -e "${GREEN}✅ Removed backend.log${NC}"
    fi

    if [ -f "$DIR/frontend.log" ]; then
        rm "$DIR/frontend.log"
        echo -e "${GREEN}✅ Removed frontend.log${NC}"
    fi
}

# Main execution
main() {
    stop_backend
    stop_frontend
    cleanup_logs

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Portfolio Intelligence System stopped${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Run main function
main
