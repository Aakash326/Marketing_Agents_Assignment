import React, { useState } from 'react';
import { motion } from 'framer-motion';

export default function StockPredictor() {
  const [formData, setFormData] = useState({
    open: '100',
    high: '110',
    low: '95',
    close: '105',
    volume: '1000000',
    return_val: '2.5',
    sma_10: '102',
    sma_50: '100',
    volatility_10: '2.0'
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch('http://localhost:8000/api/predict-stock', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          open: parseFloat(formData.open),
          high: parseFloat(formData.high),
          low: parseFloat(formData.low),
          close: parseFloat(formData.close),
          volume: parseInt(formData.volume),
          return_val: parseFloat(formData.return_val),
          sma_10: parseFloat(formData.sma_10),
          sma_50: parseFloat(formData.sma_50),
          volatility_10: parseFloat(formData.volatility_10)
        })
      });

      if (!response.ok) {
        throw new Error('Prediction failed');
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError(err.message || 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      open: '100',
      high: '110',
      low: '95',
      close: '105',
      volume: '1000000',
      return_val: '2.5',
      sma_10: '102',
      sma_50: '100',
      volatility_10: '2.0'
    });
    setPrediction(null);
    setError(null);
  };

  const inputFields = [
    { name: 'open', label: 'Open Price', min: 1, max: 1000, step: 0.5, unit: '$' },
    { name: 'high', label: 'High Price', min: 1, max: 1000, step: 0.5, unit: '$' },
    { name: 'low', label: 'Low Price', min: 1, max: 1000, step: 0.5, unit: '$' },
    { name: 'close', label: 'Close Price', min: 1, max: 1000, step: 0.5, unit: '$' },
    { name: 'volume', label: 'Volume', min: 1000, max: 10000000, step: 1000, unit: '' },
    { name: 'return_val', label: 'Return', min: -20, max: 20, step: 0.1, unit: '%' },
    { name: 'sma_10', label: 'SMA 10', min: 1, max: 1000, step: 0.5, unit: '$' },
    { name: 'sma_50', label: 'SMA 50', min: 1, max: 1000, step: 0.5, unit: '$' },
    { name: 'volatility_10', label: 'Volatility (10-day)', min: 0, max: 10, step: 0.1, unit: '' }
  ];

  const getPredictionColor = (prediction) => {
    if (!prediction) return '';
    if (prediction.prediction === 'Buy') {
      return 'text-green-600 bg-green-50 border-green-200';
    }
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getRiskColor = (riskLevel) => {
    if (!riskLevel) return '';
    if (riskLevel === 'Low') return 'bg-green-100 text-green-800';
    if (riskLevel === 'Medium') return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const formatValue = (value, field) => {
    const num = parseFloat(value);
    if (field.name === 'volume') {
      return num.toLocaleString();
    }
    return num.toFixed(field.step < 1 ? 1 : 0);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.h1
            className="text-4xl font-bold text-gray-800 mb-2"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            📈 Stock Predictor
          </motion.h1>
          <p className="text-gray-600">
            Adjust stock parameters using sliders to predict whether you should buy or not
          </p>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Input Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-2 bg-white rounded-2xl shadow-lg p-6"
          >
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="mr-2">📊</span>
              Stock Data Input
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {inputFields.map((field, index) => (
                <motion.div
                  key={field.name}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 + index * 0.03 }}
                  className="bg-gray-50 p-4 rounded-xl"
                >
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-sm font-semibold text-gray-700">
                      {field.label}
                    </label>
                    <div className="flex items-center gap-2">
                      <input
                        type="number"
                        name={field.name}
                        value={formData[field.name]}
                        onChange={handleChange}
                        step={field.step}
                        min={field.min}
                        max={field.max}
                        required
                        className="w-28 px-3 py-1 text-right border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm font-bold"
                      />
                      {field.unit && (
                        <span className="text-sm font-medium text-gray-600 w-6">
                          {field.unit}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Slider */}
                  <div className="relative">
                    <input
                      type="range"
                      name={field.name}
                      value={formData[field.name]}
                      onChange={handleChange}
                      min={field.min}
                      max={field.max}
                      step={field.step}
                      className="w-full h-2 bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 rounded-lg appearance-none cursor-pointer slider"
                      style={{
                        background: `linear-gradient(to right,
                          rgb(147, 197, 253) 0%,
                          rgb(167, 139, 250) ${((formData[field.name] - field.min) / (field.max - field.min)) * 100}%,
                          rgb(229, 231, 235) ${((formData[field.name] - field.min) / (field.max - field.min)) * 100}%,
                          rgb(229, 231, 235) 100%)`
                      }}
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>{field.min}{field.unit}</span>
                      <span>{field.max}{field.unit}</span>
                    </div>
                  </div>
                </motion.div>
              ))}

              <div className="flex gap-3 pt-4">
                <motion.button
                  type="submit"
                  disabled={loading}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`flex-1 py-3 px-6 rounded-xl font-semibold text-white transition-all shadow-lg ${
                    loading
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 hover:shadow-xl'
                  }`}
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Analyzing...
                    </span>
                  ) : (
                    <span className="flex items-center justify-center">
                      <span className="text-xl mr-2">🎯</span>
                      Predict
                    </span>
                  )}
                </motion.button>

                <motion.button
                  type="button"
                  onClick={handleReset}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-6 py-3 rounded-xl font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 transition-all shadow-lg hover:shadow-xl"
                >
                  <span className="flex items-center justify-center">
                    <span className="text-xl mr-2">🔄</span>
                    Reset
                  </span>
                </motion.button>
              </div>
            </form>
          </motion.div>

          {/* Results Panel */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl shadow-lg p-6"
          >
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="mr-2">🎯</span>
              Results
            </h2>

            {error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-4"
              >
                <div className="flex items-center">
                  <span className="text-2xl mr-2">⚠️</span>
                  <div>
                    <p className="font-semibold">Error</p>
                    <p className="text-sm">{error}</p>
                  </div>
                </div>
              </motion.div>
            )}

            {!prediction && !error && (
              <div className="flex flex-col items-center justify-center h-96 text-gray-400">
                <span className="text-6xl mb-4">📊</span>
                <p className="text-center text-sm px-4">
                  Adjust the sliders and click Predict to see AI-powered recommendations
                </p>
              </div>
            )}

            {prediction && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-4"
              >
                {/* Main Prediction */}
                <div className={`border-2 rounded-xl p-6 text-center ${getPredictionColor(prediction)}`}>
                  <p className="text-sm font-medium mb-2">Decision</p>
                  <p className="text-3xl font-bold">{prediction.prediction}</p>
                </div>

                {/* Confidence */}
                <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6">
                  <p className="text-sm font-semibold text-gray-700 mb-3">Confidence Level</p>
                  <div className="space-y-2">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden shadow-inner">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${prediction.confidence * 100}%` }}
                          transition={{ duration: 0.8, ease: "easeOut" }}
                          className={`h-full ${
                            prediction.confidence > 0.8
                              ? 'bg-gradient-to-r from-green-400 to-green-600'
                              : prediction.confidence > 0.6
                              ? 'bg-gradient-to-r from-yellow-400 to-yellow-600'
                              : 'bg-gradient-to-r from-orange-400 to-orange-600'
                          }`}
                        />
                      </div>
                      <span className="text-2xl font-bold text-gray-800 min-w-[60px] text-right">
                        {(prediction.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Risk Level */}
                <div className="bg-gray-50 rounded-xl p-6">
                  <p className="text-sm font-semibold text-gray-700 mb-3">Risk Assessment</p>
                  <span className={`inline-block px-4 py-2 rounded-full font-bold ${getRiskColor(prediction.risk_level)}`}>
                    {prediction.risk_level}
                  </span>
                </div>

                {/* Recommendation */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6">
                  <p className="text-sm font-semibold text-blue-900 mb-2 flex items-center">
                    <span className="text-xl mr-2">💡</span>
                    Recommendation
                  </p>
                  <p className="text-blue-800 font-medium">{prediction.recommendation}</p>
                </div>

                {/* Disclaimer */}
                <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4 text-sm text-yellow-800">
                  <p className="font-bold mb-1 flex items-center">
                    <span className="text-lg mr-2">⚠️</span>
                    Disclaimer
                  </p>
                  <p>This prediction is AI-generated and should not be the sole basis for investment decisions.</p>
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>

        {/* Info Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-8 bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 rounded-2xl p-6 shadow-lg"
        >
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span className="text-2xl mr-2">ℹ️</span>
            About the Predictor
          </h3>
          <div className="grid md:grid-cols-3 gap-6 text-sm text-gray-700">
            <div className="bg-white/50 p-4 rounded-xl">
              <p className="font-bold mb-2 text-blue-600">🤖 How it works</p>
              <ul className="space-y-1">
                <li>• Analyzes 9 stock features</li>
                <li>• Uses Random Forest ML model</li>
                <li>• Provides confidence scores</li>
                <li>• Evaluates risk levels</li>
              </ul>
            </div>
            <div className="bg-white/50 p-4 rounded-xl">
              <p className="font-bold mb-2 text-purple-600">📊 Input Parameters</p>
              <ul className="space-y-1">
                <li>• OHLC prices</li>
                <li>• Trading volume</li>
                <li>• Return percentage</li>
                <li>• Moving averages (SMA)</li>
                <li>• 10-day volatility</li>
              </ul>
            </div>
            <div className="bg-white/50 p-4 rounded-xl">
              <p className="font-bold mb-2 text-pink-600">🎯 Features</p>
              <ul className="space-y-1">
                <li>• Interactive sliders</li>
                <li>• Real-time predictions</li>
                <li>• Risk assessment</li>
                <li>• AI recommendations</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </motion.div>

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          cursor: pointer;
          border-radius: 50%;
          box-shadow: 0 2px 4px rgba(0,0,0,0.2);
          transition: all 0.2s;
        }

        .slider::-webkit-slider-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }

        .slider::-moz-range-thumb {
          width: 20px;
          height: 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          cursor: pointer;
          border-radius: 50%;
          border: none;
          box-shadow: 0 2px 4px rgba(0,0,0,0.2);
          transition: all 0.2s;
        }

        .slider::-moz-range-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
      `}</style>
    </div>
  );
}
