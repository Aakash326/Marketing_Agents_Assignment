#!/bin/bash
# Start AutoGen FastAPI Backend on port 8001

cd backends/autogen_backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
