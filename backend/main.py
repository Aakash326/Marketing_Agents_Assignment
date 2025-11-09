# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List, Optional
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = FastAPI(title="Stock Prediction & RAG API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML model and scaler
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saved_models", "best_stock_model_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saved_models", "best_stock_model_scaler.pkl")

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Stock prediction model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    scaler = None

# Load RAG system
try:
    from rag_system.src.retriever import create_qa_chain
    qa_chain = create_qa_chain()
    print("RAG system loaded successfully")
except Exception as e:
    print(f"Error loading RAG system: {e}")
    qa_chain = None

# Request model
class StockPredictionRequest(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: int
    return_val: float
    sma_10: float
    sma_50: float
    volatility_10: float

# Response model
class StockPredictionResponse(BaseModel):
    prediction: str
    confidence: float
    recommendation: str
    risk_level: str

# RAG Request model
class RAGQueryRequest(BaseModel):
    question: str
    k: Optional[int] = 3

# RAG Response model
class RAGQueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.get("/")
async def root():
    return {
        "message": "Stock Prediction API is running",
        "model_status": "loaded" if model else "not loaded"
    }

@app.post("/api/predict-stock", response_model=StockPredictionResponse)
async def predict_stock(request: StockPredictionRequest):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        # Prepare input data in the correct order
        features = np.array([[
            request.open,
            request.high,
            request.low,
            request.close,
            request.volume,
            request.return_val,
            request.sma_10,
            request.sma_50,
            request.volatility_10
        ]])

        # Scale the features
        features_scaled = scaler.transform(features)

        # Get prediction and probability
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]

        # Interpret results
        buy_signal = prediction == 1.0
        confidence = float(probability[1] if buy_signal else probability[0])

        # Generate recommendation
        if buy_signal and confidence > 0.8:
            recommendation = "Strong Buy - High confidence signal"
            risk_level = "Low"
        elif buy_signal and confidence > 0.6:
            recommendation = "Buy - Moderate confidence signal"
            risk_level = "Medium"
        elif buy_signal:
            recommendation = "Consider Buy - Lower confidence"
            risk_level = "High"
        else:
            if confidence > 0.8:
                recommendation = "Do Not Buy - High confidence"
                risk_level = "High if purchased"
            else:
                recommendation = "Hold/Wait - Market unclear"
                risk_level = "Medium"

        return StockPredictionResponse(
            prediction="Buy" if buy_signal else "Do Not Buy",
            confidence=confidence,
            recommendation=recommendation,
            risk_level=risk_level
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/api/rag/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    if qa_chain is None:
        raise HTTPException(status_code=500, detail="RAG system not loaded")

    try:
        result = qa_chain({"query": request.question})

        answer = result.get('result', 'No answer found.')
        sources = []

        if result.get('source_documents'):
            for doc in result['source_documents'][:request.k]:
                source = doc.metadata.get('source', 'Unknown source')
                sources.append(source)

        return RAGQueryResponse(
            answer=answer,
            sources=sources
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query error: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "rag_loaded": qa_chain is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
