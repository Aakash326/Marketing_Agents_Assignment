
# Best Stock Prediction Model - Loading Script
import joblib
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load the saved components
model = joblib.load("best_stock_model_model.pkl")
scaler = joblib.load("best_stock_model_scaler.pkl")

# Load feature information
with open("best_stock_model_features.json", "r") as f:
    feature_info = json.load(f)

# Load performance metrics
with open("best_stock_model_metrics.json", "r") as f:
    metrics = json.load(f)

print("📊 MODEL LOADED SUCCESSFULLY!")
print(f"Model Type: {{metrics['model_type']}}")
print(f"Test Accuracy: {{metrics['test_accuracy']:.4f}}")
print(f"Best Threshold: {{metrics['best_threshold']:.3f}}")
print(f"Precision: {{metrics['precision_at_threshold']:.3f}}")
print(f"Recall: {{metrics['recall_at_threshold']:.3f}}")

def predict_stock(data):
    """
    Make predictions on new stock data

    Parameters:
    data: pandas DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume', 'Return', 'SMA_10', 'SMA_50', 'Volatility_10']

    Returns:
    dict with predictions and probabilities
    """
    # Ensure correct column order
    required_features = ['Open', 'High', 'Low', 'Close', 'Volume', 'Return', 'SMA_10', 'SMA_50', 'Volatility_10']
    if not all(col in data.columns for col in required_features):
        missing = set(required_features) - set(data.columns)
        raise ValueError(f"Missing features: {{missing}}")

    # Select and order features correctly
    X = data['Open', 'High', 'Low', 'Close', 'Volume', 'Return', 'SMA_10', 'SMA_50', 'Volatility_10']

    # Scale the features
    X_scaled = scaler.transform(X)

    # Get predictions and probabilities
    predictions = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)[:, 1]

    # Apply optimal threshold
    threshold_predictions = (probabilities >= 0.02).astype(int)

    return {
        'binary_predictions': predictions,
        'probabilities': probabilities,
        'threshold_predictions': threshold_predictions,
        'buy_signals': threshold_predictions == 1,
        'confidence_scores': probabilities
    }

# Example usage:
# new_data = pd.DataFrame({...})  # Your new stock data
# results = predict_stock(new_data)
# print(f"Buy signals: {results['buy_signals']}")
