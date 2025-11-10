"""
ML Stock Prediction endpoint using the saved Random Forest model.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import logging
import os
import joblib
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

router = APIRouter()


class StockPredictionRequest(BaseModel):
    """Request model for stock prediction."""
    open: float = Field(..., description="Opening price")
    high: float = Field(..., description="High price")
    low: float = Field(..., description="Low price")
    close: float = Field(..., description="Closing price")
    volume: int = Field(..., description="Trading volume")
    return_val: float = Field(..., description="Return percentage", alias="return_val")
    sma_10: float = Field(..., description="10-day Simple Moving Average")
    sma_50: float = Field(..., description="50-day Simple Moving Average")
    volatility_10: float = Field(..., description="10-day volatility")

    class Config:
        populate_by_name = True


class StockPredictionResponse(BaseModel):
    """Response model for stock prediction."""
    prediction: str
    probability: float
    confidence: str
    recommendation: str


# Global variables to cache loaded model
_model = None
_scaler = None
_model_loaded = False


def load_model():
    """Load the saved Random Forest model and scaler."""
    global _model, _scaler, _model_loaded
    
    if _model_loaded:
        return _model, _scaler
    
    try:
        # Try to find model in multiple possible locations
        possible_paths = [
            "/Users/saiaakash/Desktop/All_proj/Assignment-marketing-agents/saved_models",
            "../../saved_models",
            "../../../saved_models",
            "saved_models"
        ]
        
        model_dir = None
        for path in possible_paths:
            if os.path.exists(path):
                model_dir = path
                break
        
        if not model_dir:
            raise FileNotFoundError("saved_models directory not found")
        
        # Load model and scaler
        model_path = os.path.join(model_dir, "best_stock_model_model.pkl")
        scaler_path = os.path.join(model_dir, "best_stock_model_scaler.pkl")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
        
        _model = joblib.load(model_path)
        _scaler = joblib.load(scaler_path)
        _model_loaded = True
        
        logger.info(f"✅ ML model loaded successfully from {model_dir}")
        return _model, _scaler
        
    except Exception as e:
        logger.error(f"❌ Failed to load ML model: {str(e)}")
        raise


@router.post("/predict-stock", response_model=StockPredictionResponse)
async def predict_stock(request: StockPredictionRequest) -> StockPredictionResponse:
    """
    Predict whether to buy a stock based on input features.
    
    Uses the saved Random Forest model trained on historical stock data.
    """
    try:
        logger.info("Received stock prediction request")
        
        # Load model if not already loaded
        model, scaler = load_model()
        
        # Prepare input data in the correct order
        # Features: ['Open', 'High', 'Low', 'Close', 'Volume', 'Return', 'SMA_10', 'SMA_50', 'Volatility_10']
        input_data = pd.DataFrame({
            'Open': [request.open],
            'High': [request.high],
            'Low': [request.low],
            'Close': [request.close],
            'Volume': [request.volume],
            'Return': [request.return_val],
            'SMA_10': [request.sma_10],
            'SMA_50': [request.sma_50],
            'Volatility_10': [request.volatility_10]
        })
        
        # Scale the features
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]  # Probability of "Buy"
        
        # Determine prediction label
        prediction_label = "Buy" if prediction == 1 else "Don't Buy"
        
        # Determine confidence level
        if probability >= 0.8 or probability <= 0.2:
            confidence = "High"
        elif probability >= 0.6 or probability <= 0.4:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        # Generate recommendation
        if prediction_label == "Buy":
            if probability >= 0.9:
                recommendation = "Strong buy signal. High confidence in positive returns."
            elif probability >= 0.7:
                recommendation = "Good buy opportunity. Model shows positive indicators."
            else:
                recommendation = "Moderate buy signal. Consider other factors before investing."
        else:
            if probability <= 0.1:
                recommendation = "Strong sell/avoid signal. High risk of negative returns."
            elif probability <= 0.3:
                recommendation = "Avoid buying. Model indicates unfavorable conditions."
            else:
                recommendation = "Weak signal. Market conditions are uncertain."
        
        logger.info(f"Prediction: {prediction_label}, Probability: {probability:.3f}, Confidence: {confidence}")
        
        return StockPredictionResponse(
            prediction=prediction_label,
            probability=round(probability, 3),
            confidence=confidence,
            recommendation=recommendation
        )
        
    except FileNotFoundError as e:
        logger.error(f"Model files not found: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"ML model not found. Please ensure the model files are in the saved_models directory. Error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/predict-stock/health")
async def model_health() -> Dict[str, Any]:
    """
    Check if the ML model is loaded and ready.
    """
    try:
        model, scaler = load_model()
        return {
            "status": "healthy",
            "model_loaded": True,
            "model_type": str(type(model).__name__),
            "message": "ML model is ready for predictions"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "error": str(e),
            "message": "ML model failed to load"
        }
