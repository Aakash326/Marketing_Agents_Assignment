import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { companies } from '../data/companies';
import stockQuestions from '../data/stockQuestions';

function StockAnalysis() {
  const [step, setStep] = useState(1); // 1: Select Company, 2: Select Question, 3: Results
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleCompanySelect = (company) => {
    setSelectedCompany(company);
    setStep(2);
    setError(null);
  };

  const handleQuestionSelect = (question) => {
    setSelectedQuestion(question);
  };

  const handleAnalyze = async () => {
    if (!selectedCompany || !selectedQuestion) return;

    setLoading(true);
    setResult(null);
    setError(null);
    setStep(3);

    try {
      // Call the AutoGen 6-agent workflow API
      const response = await axios.post('http://localhost:8001/api/stock-analysis', {
        symbol: selectedCompany.symbol,
        question: selectedQuestion.text,
        portfolio_value: 100000.0,
        risk_per_trade: 2.0
      }, {
        timeout: 120000 // 2 minute timeout for agent processing
      });

      const data = response.data;

      // Transform API response
      setResult({
        symbol: data.symbol,
        company: selectedCompany.name,
        question: selectedQuestion.text,
        recommendation: data.recommendation,
        confidence: data.confidence,
        summary: data.summary,
        execution_plan: data.execution_plan,
        technical_analysis: data.technical_analysis,
        fundamental_analysis: data.fundamental_analysis,
        risk_assessment: data.risk_assessment,
        agentReports: Object.entries(data.agent_outputs || {}).map(([agent, output]) => ({
          agent: agent,
          status: output.substring(0, 150) + '...',
          emoji: getAgentEmoji(agent),
          fullOutput: output
        })),
        timestamp: data.timestamp || new Date().toLocaleString()
      });

    } catch (err) {
      console.error('Error analyzing stock:', err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to analyze stock. Please ensure the AutoGen backend is running on port 8001.'
      );
    } finally {
      setLoading(false);
    }
  };

  const getAgentEmoji = (agentName) => {
    const emojiMap = {
      'OrganiserAgent': '🗂️',
      'RiskManager': '⚠️',
      'DataAnalyst': '📊',
      'QuantitativeAnalyst': '📈',
      'StrategyDeveloper': '🎯',
      'ReportAgent': '📋'
    };
    return emojiMap[agentName] || '🤖';
  };

  const resetWorkflow = () => {
    setStep(1);
    setSelectedCompany(null);
    setSelectedQuestion(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-gray-800">
            📈 6-Agent Stock Analysis
          </h1>
          <p className="text-gray-600">
            Select a company and question to get comprehensive analysis from 6 specialized AI agents
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8 flex items-center justify-center">
          <div className="flex items-center space-x-4">
            <div className={`flex items-center ${step >= 1 ? 'text-blue-600' : 'text-gray-400'}`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${step >= 1 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>
                1
              </div>
              <span className="ml-2 font-semibold">Select Company</span>
            </div>
            <div className="w-16 h-1 bg-gray-300"></div>
            <div className={`flex items-center ${step >= 2 ? 'text-blue-600' : 'text-gray-400'}`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${step >= 2 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>
                2
              </div>
              <span className="ml-2 font-semibold">Select Question</span>
            </div>
            <div className="w-16 h-1 bg-gray-300"></div>
            <div className={`flex items-center ${step >= 3 ? 'text-blue-600' : 'text-gray-400'}`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${step >= 3 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>
                3
              </div>
              <span className="ml-2 font-semibold">Analysis</span>
            </div>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {/* Step 1: Company Selection */}
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="bg-white rounded-xl shadow-lg p-6"
            >
              <h2 className="text-2xl font-bold mb-6 text-gray-800">Select a Company</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {companies.map((company) => (
                  <motion.button
                    key={company.symbol}
                    whileHover={{ scale: 1.05, y: -5 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleCompanySelect(company)}
                    className="bg-gradient-to-br from-blue-50 to-purple-50 hover:from-blue-100 hover:to-purple-100 border-2 border-blue-200 rounded-xl p-4 text-left transition-all"
                  >
                    <div className="text-4xl mb-2">{company.logo}</div>
                    <div className="font-bold text-gray-800 text-lg">{company.symbol}</div>
                    <div className="text-sm text-gray-600 mb-2">{company.name}</div>
                    <div className="text-xs text-gray-500 bg-white px-2 py-1 rounded-full inline-block">
                      {company.sector}
                    </div>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}

          {/* Step 2: Question Selection */}
          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="space-y-6"
            >
              {/* Selected Company Card */}
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <span className="text-6xl mr-4">{selectedCompany.logo}</span>
                    <div>
                      <h2 className="text-3xl font-bold">{selectedCompany.symbol}</h2>
                      <p className="text-blue-100">{selectedCompany.name}</p>
                      <p className="text-sm text-blue-200">{selectedCompany.sector}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setStep(1)}
                    className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                  >
                    ← Change Company
                  </button>
                </div>
              </div>

              {/* Question Selection */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-6 text-gray-800">Select Your Question</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {stockQuestions.map((question) => (
                    <motion.button
                      key={question.id}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => handleQuestionSelect(question)}
                      className={`text-left p-4 rounded-xl border-2 transition-all ${
                        selectedQuestion?.id === question.id
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-blue-300 bg-gray-50'
                      }`}
                    >
                      <div className="flex items-start">
                        <span className="text-2xl mr-3">{question.icon}</span>
                        <div className="flex-1">
                          <div className="font-semibold text-gray-800 mb-1">{question.text}</div>
                          <div className="text-xs text-gray-600">{question.description}</div>
                          <div className="mt-2">
                            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                              {question.category.replace('_', ' ')}
                            </span>
                          </div>
                        </div>
                      </div>
                    </motion.button>
                  ))}
                </div>

                {/* Analyze Button */}
                {selectedQuestion && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-6 flex justify-center"
                  >
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleAnalyze}
                      className="px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-bold text-lg shadow-lg"
                    >
                      🚀 Start 6-Agent Analysis
                    </motion.button>
                  </motion.div>
                )}
              </div>
            </motion.div>
          )}

          {/* Step 3: Loading & Results */}
          {step === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-6"
            >
              {/* Loading State */}
              {loading && (
                <div className="bg-white rounded-xl shadow-lg p-12 text-center">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    className="text-8xl mb-4 inline-block"
                  >
                    🤖
                  </motion.div>
                  <p className="text-2xl font-bold text-gray-800 mb-2">6 AI Agents Working...</p>
                  <p className="text-gray-600 mb-4">Analyzing {selectedCompany?.name} ({selectedCompany?.symbol})</p>
                  <p className="text-sm text-gray-500 italic">"{selectedQuestion?.text}"</p>
                  <div className="mt-6 flex justify-center space-x-2">
                    {['OrganiserAgent', 'RiskManager', 'DataAnalyst', 'QuantitativeAnalyst', 'StrategyDeveloper', 'ReportAgent'].map((agent, i) => (
                      <motion.div
                        key={agent}
                        initial={{ opacity: 0.3 }}
                        animate={{ opacity: [0.3, 1, 0.3] }}
                        transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}
                        className="w-3 h-3 rounded-full bg-blue-600"
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Error Display */}
              {error && !loading && (
                <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6">
                  <div className="flex items-start">
                    <span className="text-4xl mr-4">❌</span>
                    <div className="flex-1">
                      <h3 className="font-bold text-red-900 text-xl mb-2">Analysis Failed</h3>
                      <p className="text-red-700 mb-4">{error}</p>
                      <button
                        onClick={resetWorkflow}
                        className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                      >
                        ← Start Over
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Results Display */}
              {result && !loading && !error && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  {/* Header Card */}
                  <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl shadow-lg p-8">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center">
                        <span className="text-6xl mr-4">{selectedCompany?.logo}</span>
                        <div>
                          <h2 className="text-4xl font-bold">{result.symbol}</h2>
                          <p className="text-green-100">{result.company}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-5xl font-bold mb-1">{result.recommendation}</div>
                        <div className="text-lg text-green-100">Confidence: {result.confidence}%</div>
                      </div>
                    </div>
                    <div className="bg-white/20 rounded-lg p-3 backdrop-blur">
                      <p className="text-sm italic">"{result.question}"</p>
                    </div>
                    <div className="mt-4 flex justify-between items-center">
                      <span className="text-sm text-green-100">{result.timestamp}</span>
                      <button
                        onClick={resetWorkflow}
                        className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                      >
                        ← New Analysis
                      </button>
                    </div>
                  </div>

                  {/* Agent Status */}
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h3 className="text-2xl font-bold mb-4 text-gray-800">Agent Collaboration Status</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {result.agentReports?.map((agent, i) => (
                        <div key={i} className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-lg p-4 border-2 border-blue-200">
                          <div className="flex items-center mb-2">
                            <span className="text-3xl mr-2">{agent.emoji}</span>
                            <span className="font-bold text-gray-800">{agent.agent}</span>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">{agent.status}</p>
                          {agent.fullOutput && (
                            <details className="mt-2">
                              <summary className="text-xs text-blue-600 cursor-pointer hover:underline font-semibold">
                                View full output →
                              </summary>
                              <pre className="text-xs text-gray-700 mt-2 p-3 bg-white rounded border overflow-x-auto max-h-48 overflow-y-auto">
                                {agent.fullOutput}
                              </pre>
                            </details>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Analysis Sections */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Summary */}
                    {result.summary && (
                      <div className="bg-white rounded-xl shadow-lg p-6">
                        <h3 className="text-xl font-bold mb-4 text-gray-800 flex items-center">
                          <span className="mr-2">📋</span>
                          Analysis Summary
                        </h3>
                        <div className="text-gray-700 whitespace-pre-wrap">
                          {result.summary}
                        </div>
                      </div>
                    )}

                    {/* Execution Plan */}
                    {result.execution_plan && (
                      <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-6">
                        <h3 className="text-xl font-bold mb-4 text-blue-900 flex items-center">
                          <span className="mr-2">🎯</span>
                          Execution Plan
                        </h3>
                        <div className="text-blue-800 whitespace-pre-wrap">
                          {result.execution_plan}
                        </div>
                      </div>
                    )}

                    {/* Technical Analysis */}
                    {result.technical_analysis && (
                      <div className="bg-purple-50 border-2 border-purple-200 rounded-xl p-6">
                        <h3 className="text-xl font-bold mb-4 text-purple-900 flex items-center">
                          <span className="mr-2">📈</span>
                          Technical Analysis
                        </h3>
                        <div className="text-purple-800 whitespace-pre-wrap">
                          {result.technical_analysis}
                        </div>
                      </div>
                    )}

                    {/* Risk Assessment */}
                    {result.risk_assessment && (
                      <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6">
                        <h3 className="text-xl font-bold mb-4 text-red-900 flex items-center">
                          <span className="mr-2">⚠️</span>
                          Risk Assessment
                        </h3>
                        <div className="text-red-800 whitespace-pre-wrap">
                          {result.risk_assessment}
                        </div>
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Info Banner */}
        {step === 1 && (
          <div className="mt-8 bg-purple-50 border-2 border-purple-200 rounded-xl p-6">
            <div className="flex items-start">
              <span className="text-4xl mr-4">🤖</span>
              <div>
                <h3 className="font-bold text-purple-900 text-lg mb-2">6-Agent AutoGen Workflow</h3>
                <p className="text-sm text-purple-700 mb-3">
                  This system uses 6 specialized AI agents working in collaboration:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-purple-700">
                  <div>• <strong>Organiser Agent:</strong> Market data collection</div>
                  <div>• <strong>Risk Manager:</strong> Risk analysis & position sizing</div>
                  <div>• <strong>Data Analyst:</strong> Fundamental analysis</div>
                  <div>• <strong>Quantitative Analyst:</strong> Technical indicators</div>
                  <div>• <strong>Strategy Developer:</strong> Entry/exit strategy</div>
                  <div>• <strong>Report Agent:</strong> Final recommendation</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}

export default StockAnalysis;
