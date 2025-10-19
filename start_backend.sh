#!/bin/bash
# Start LangGraph FastAPI Backend on port 8000

cd backends/langgraph_backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
