import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, Home } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const SystemDesignPresentation = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const navigate = useNavigate();

  const slides = [
    // Slide 1: Title
    {
      title: "Portfolio Intelligence System",
      subtitle: "Multi-Agent Architecture with LangGraph & AutoGen",
      type: "title",
      content: (
        <div className="text-center space-y-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2 }}
            className="text-8xl"
          >
            🤖📊💼
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
          >
            Portfolio Intelligence System
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="text-3xl text-gray-600"
          >
            Multi-Agent AI Architecture
          </motion.p>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-xl text-gray-500"
          >
            LangGraph + AutoGen + RAG Integration
          </motion.div>
        </div>
      )
    },

    // Slide 2: System Overview
    {
      title: "System Architecture Overview",
      type: "content",
      content: (
        <div className="space-y-6">
          <div className="grid grid-cols-3 gap-6">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border-2 border-blue-300"
            >
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold mb-2">LangGraph Backend</h3>
              <p className="text-sm text-gray-700">Portfolio intelligence with 5-agent workflow</p>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border-2 border-purple-300"
            >
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-bold mb-2">AutoGen Backend</h3>
              <p className="text-sm text-gray-700">6-agent stock analysis workflow</p>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border-2 border-green-300"
            >
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-xl font-bold mb-2">RAG System</h3>
              <p className="text-sm text-gray-700">Knowledge base for market education</p>
            </motion.div>
          </div>

          <div className="bg-gray-50 p-6 rounded-xl">
            <h3 className="text-2xl font-bold mb-4">Tech Stack</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold mb-2">Backend:</h4>
                <ul className="list-disc ml-6 space-y-1 text-sm">
                  <li>FastAPI (Python)</li>
                  <li>LangGraph for workflow orchestration</li>
                  <li>AutoGen for multi-agent collaboration</li>
                  <li>OpenAI GPT-4</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Frontend:</h4>
                <ul className="list-disc ml-6 space-y-1 text-sm">
                  <li>React + Vite</li>
                  <li>Tailwind CSS</li>
                  <li>Framer Motion</li>
                  <li>Recharts for visualizations</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 3: LangGraph Agent Architecture
    {
      title: "LangGraph Multi-Agent Workflow",
      type: "content",
      content: (
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-xl">
            <h3 className="text-2xl font-bold mb-4">5-Agent Portfolio Intelligence System</h3>

            <div className="space-y-3">
              {[
                {
                  icon: "🎯",
                  name: "Planner Agent",
                  role: "Query Analysis & Routing",
                  color: "blue",
                  details: [
                    "Analyzes user queries using GPT-4 to understand intent",
                    "Determines data needs (portfolio, market, both)",
                    "Detects if user wants recommendations or just analysis",
                    "Routes to appropriate agents based on query type"
                  ]
                },
                {
                  icon: "💼",
                  name: "Portfolio Agent",
                  role: "Holdings Analysis & Risk Assessment",
                  color: "purple",
                  details: [
                    "Reads client portfolio data from Excel files (10 clients)",
                    "Calculates total portfolio value and asset allocation",
                    "Analyzes risk profile based on holdings distribution",
                    "Provides insights on diversification and sector exposure"
                  ]
                },
                {
                  icon: "📈",
                  name: "Market Agent",
                  role: "Real-time Prices & News",
                  color: "green",
                  details: [
                    "Fetches current stock prices via yfinance & Alpha Vantage",
                    "Retrieves market news and recent headlines",
                    "Extracts ticker symbols from natural language queries",
                    "Provides market trends and price movements"
                  ]
                },
                {
                  icon: "🤝",
                  name: "Collaboration Agent",
                  role: "Data Synthesis & Returns Calculation",
                  color: "orange",
                  details: [
                    "Combines portfolio data with real-time market prices",
                    "Calculates investment returns: (Current - Purchase) / Purchase × 100",
                    "Links market news to user's specific holdings",
                    "Provides comprehensive performance analysis"
                  ]
                },
                {
                  icon: "✅",
                  name: "Validator Agent",
                  role: "Quality Assurance & Fact Checking",
                  color: "red",
                  details: [
                    "Verifies response accuracy against source data",
                    "Detects ambiguous queries and requests clarification",
                    "Checks for hallucinations and unsupported claims",
                    "Ensures data sufficiency before providing answers"
                  ]
                }
              ].map((agent, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className={`bg-white rounded-lg border-l-4 border-${agent.color}-500 shadow-sm p-3`}
                >
                  <div className="flex items-start gap-3">
                    <div className="text-2xl">{agent.icon}</div>
                    <div className="flex-1">
                      <h4 className="font-bold text-base">{agent.name}</h4>
                      <p className="text-xs text-gray-600 mb-2">{agent.role}</p>
                      <ul className="space-y-1">
                        {agent.details.map((detail, i) => (
                          <li key={i} className="text-xs text-gray-700 flex items-start gap-1">
                            <span className="text-green-600 mt-0.5">•</span>
                            <span>{detail}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      )
    },

    // Slide 4: Agent Graph & Data Flow
    {
      title: "Agent Execution Graph",
      type: "content",
      content: (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl border-2 border-gray-200">
            <h3 className="text-2xl font-bold mb-6 text-center">Workflow Execution Flow</h3>

            <div className="relative">
              {/* Flow diagram */}
              <div className="flex flex-col items-center space-y-4">
                {/* START */}
                <div className="bg-green-500 text-white px-6 py-3 rounded-full font-bold">
                  START
                </div>

                <div className="text-2xl">↓</div>

                {/* Planner */}
                <div className="bg-blue-500 text-white px-8 py-4 rounded-xl font-bold text-center w-64">
                  🎯 PLANNER<br/>
                  <span className="text-sm font-normal">Analyze query & determine needs</span>
                </div>

                <div className="text-2xl">↓</div>

                {/* Conditional branching */}
                <div className="flex gap-8">
                  <div className="flex flex-col items-center">
                    <div className="bg-purple-500 text-white px-6 py-3 rounded-xl font-bold text-center w-48">
                      💼 PORTFOLIO<br/>
                      <span className="text-xs font-normal">if needs_portfolio</span>
                    </div>
                  </div>

                  <div className="flex flex-col items-center">
                    <div className="bg-green-500 text-white px-6 py-3 rounded-xl font-bold text-center w-48">
                      📈 MARKET<br/>
                      <span className="text-xs font-normal">if needs_market</span>
                    </div>
                  </div>
                </div>

                <div className="text-2xl">↓</div>

                {/* Collaboration */}
                <div className="bg-orange-500 text-white px-8 py-4 rounded-xl font-bold text-center w-64">
                  🤝 COLLABORATION<br/>
                  <span className="text-sm font-normal">Synthesize data (if both)</span>
                </div>

                <div className="text-2xl">↓</div>

                {/* Validator */}
                <div className="bg-red-500 text-white px-8 py-4 rounded-xl font-bold text-center w-64">
                  ✅ VALIDATOR<br/>
                  <span className="text-sm font-normal">Quality check & output</span>
                </div>

                <div className="text-2xl">↓</div>

                {/* END */}
                <div className="bg-gray-700 text-white px-6 py-3 rounded-full font-bold">
                  END
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 5: Data Flow
    {
      title: "Data Flow Between Agents",
      type: "content",
      content: (
        <div className="space-y-6">
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 p-6 rounded-xl">
            <h3 className="text-2xl font-bold mb-4">State Management & Data Sharing</h3>

            <div className="space-y-4">
              <div className="bg-white p-4 rounded-lg shadow">
                <h4 className="font-bold text-lg mb-2">📥 Input State</h4>
                <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
{`{
  "query": "What stocks do I own?",
  "client_id": "CLT-001",
  "conversation_history": []
}`}
                </pre>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h4 className="font-bold text-lg mb-2">🔄 Intermediate State (after Planner)</h4>
                <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
{`{
  ...input,
  "needs_portfolio": true,
  "needs_market": false,
  "wants_recommendations": false,
  "plan": "User asking about holdings..."
}`}
                </pre>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h4 className="font-bold text-lg mb-2">📊 After Portfolio Agent</h4>
                <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
{`{
  ...state,
  "portfolio_data": {
    "holdings": [{"symbol": "VTI", ...}],
    "total_value": 9948702.26
  },
  "response": "You own 6 holdings: VTI, BND..."
}`}
                </pre>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h4 className="font-bold text-lg mb-2">✅ Final Output State</h4>
                <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
{`{
  "answer": "Formatted response with markdown",
  "agents_used": ["portfolio_agent", "validator"],
  "validated": true,
  "metadata": {...}
}`}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 6: Decision Making
    {
      title: "Decision-Making Process",
      type: "content",
      content: (
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl border-2 border-blue-300">
              <h3 className="text-xl font-bold mb-4">🎯 Planner Decisions</h3>
              <div className="space-y-3">
                <div className="p-3 bg-blue-50 rounded">
                  <p className="font-semibold">Query Analysis</p>
                  <p className="text-sm text-gray-600">Uses LLM to understand user intent</p>
                </div>
                <div className="p-3 bg-blue-50 rounded">
                  <p className="font-semibold">Data Needs Detection</p>
                  <p className="text-sm text-gray-600">Sets needs_portfolio, needs_market flags</p>
                </div>
                <div className="p-3 bg-blue-50 rounded">
                  <p className="font-semibold">Advice Mode Detection</p>
                  <p className="text-sm text-gray-600">Identifies if user wants recommendations</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border-2 border-green-300">
              <h3 className="text-xl font-bold mb-4">🔀 Routing Logic</h3>
              <div className="space-y-3">
                <div className="p-3 bg-green-50 rounded">
                  <p className="font-semibold">Conditional Edges</p>
                  <p className="text-sm text-gray-600">LangGraph routes based on state flags</p>
                </div>
                <div className="p-3 bg-green-50 rounded">
                  <p className="font-semibold">Parallel Execution</p>
                  <p className="text-sm text-gray-600">Portfolio & Market can run independently</p>
                </div>
                <div className="p-3 bg-green-50 rounded">
                  <p className="font-semibold">Collaboration Trigger</p>
                  <p className="text-sm text-gray-600">Activates when both data types needed</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border-2 border-orange-300">
              <h3 className="text-xl font-bold mb-4">🤝 Synthesis Strategy</h3>
              <div className="space-y-3">
                <div className="p-3 bg-orange-50 rounded">
                  <p className="font-semibold">Return Calculations</p>
                  <p className="text-sm text-gray-600">(Current - Purchase) / Purchase × 100</p>
                </div>
                <div className="p-3 bg-orange-50 rounded">
                  <p className="font-semibold">Impact Analysis</p>
                  <p className="text-sm text-gray-600">Links market changes to portfolio value</p>
                </div>
                <div className="p-3 bg-orange-50 rounded">
                  <p className="font-semibold">Contextualization</p>
                  <p className="text-sm text-gray-600">Adds news & trends to holdings data</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border-2 border-red-300">
              <h3 className="text-xl font-bold mb-4">✅ Validation Checks</h3>
              <div className="space-y-3">
                <div className="p-3 bg-red-50 rounded">
                  <p className="font-semibold">Ambiguity Detection</p>
                  <p className="text-sm text-gray-600">Requests clarification if query unclear</p>
                </div>
                <div className="p-3 bg-red-50 rounded">
                  <p className="font-semibold">Fact Checking</p>
                  <p className="text-sm text-gray-600">Verifies response against source data</p>
                </div>
                <div className="p-3 bg-red-50 rounded">
                  <p className="font-semibold">Data Sufficiency</p>
                  <p className="text-sm text-gray-600">Ensures adequate data for answer</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 7: External System Integration
    {
      title: "External System Integration",
      type: "content",
      content: (
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            {[
              {
                icon: "🤖",
                name: "OpenAI GPT-4",
                purpose: "LLM for analysis & synthesis",
                features: ["Natural language understanding", "Response generation", "Context-aware reasoning"],
                color: "green"
              },
              {
                icon: "📊",
                name: "Alpha Vantage API",
                purpose: "Real-time market data",
                features: ["Stock prices", "Market indicators", "Historical data"],
                color: "blue"
              },
              {
                icon: "📈",
                name: "yfinance",
                purpose: "Yahoo Finance data",
                features: ["Current prices", "Company info", "Market news"],
                color: "purple"
              },
              {
                icon: "🗄️",
                name: "Portfolio Excel",
                purpose: "Client holdings storage",
                features: ["10 client portfolios", "Purchase history", "Asset allocation"],
                color: "orange"
              },
              {
                icon: "📚",
                name: "RAG System",
                purpose: "Knowledge base (FAISS + HuggingFace)",
                features: ["Stock education docs", "Semantic search", "Context retrieval"],
                color: "teal"
              },
              {
                icon: "🔍",
                name: "SEC EDGAR",
                purpose: "Company filings",
                features: ["10-K reports", "Risk factors", "Financial statements"],
                color: "red"
              }
            ].map((system, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.1 }}
                className={`bg-gradient-to-br from-${system.color}-50 to-${system.color}-100 p-4 rounded-xl border-2 border-${system.color}-300`}
              >
                <div className="text-4xl mb-2">{system.icon}</div>
                <h4 className="font-bold text-lg mb-1">{system.name}</h4>
                <p className="text-sm text-gray-700 mb-3">{system.purpose}</p>
                <ul className="space-y-1">
                  {system.features.map((feature, i) => (
                    <li key={i} className="text-xs flex items-center gap-2">
                      <span className="text-green-600">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      )
    },

    // Slide 8: AutoGen Architecture
    {
      title: "AutoGen 6-Agent Stock Analysis",
      type: "content",
      content: (
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl">
            <h3 className="text-2xl font-bold mb-4">Specialized Trading Workflow</h3>

            <div className="grid grid-cols-2 gap-3">
              {[
                {
                  icon: "🎯",
                  name: "Risk Assessment Agent",
                  role: "Portfolio risk analysis & diversification",
                  details: [
                    "Calculates portfolio beta and volatility metrics",
                    "Evaluates sector concentration risks",
                    "Recommends diversification strategies"
                  ]
                },
                {
                  icon: "📊",
                  name: "Technical Analysis Agent",
                  role: "Chart patterns & indicators",
                  details: [
                    "Analyzes price charts and technical indicators (RSI, MACD)",
                    "Identifies support/resistance levels",
                    "Detects trend patterns and momentum signals"
                  ]
                },
                {
                  icon: "💰",
                  name: "Fundamental Analysis Agent",
                  role: "Financial metrics & valuation",
                  details: [
                    "Analyzes P/E ratio, EPS, revenue growth",
                    "Reads SEC filings (10-K, 10-Q) for company health",
                    "Evaluates intrinsic value vs market price"
                  ]
                },
                {
                  icon: "📰",
                  name: "Sentiment Analysis Agent",
                  role: "News & social media sentiment",
                  details: [
                    "Analyzes market news for sentiment signals",
                    "Monitors company announcements and earnings calls",
                    "Assesses public perception and market psychology"
                  ]
                },
                {
                  icon: "⚖️",
                  name: "Compliance Agent",
                  role: "Regulatory checks & constraints",
                  details: [
                    "Ensures recommendations comply with regulations",
                    "Checks for insider trading restrictions",
                    "Validates investment suitability criteria"
                  ]
                },
                {
                  icon: "🤝",
                  name: "Coordinator Agent",
                  role: "Synthesis & final recommendation",
                  details: [
                    "Aggregates insights from all specialist agents",
                    "Resolves conflicting recommendations via voting",
                    "Generates final investment decision with rationale"
                  ]
                }
              ].map((agent, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-white p-3 rounded-lg shadow-md border-l-4 border-purple-500"
                >
                  <div className="flex items-start gap-2">
                    <div className="text-2xl">{agent.icon}</div>
                    <div className="flex-1">
                      <h4 className="font-bold text-sm">{agent.name}</h4>
                      <p className="text-xs text-gray-600 mb-2">{agent.role}</p>
                      <ul className="space-y-1">
                        {agent.details.map((detail, i) => (
                          <li key={i} className="text-xs text-gray-700 flex items-start gap-1">
                            <span className="text-purple-600 mt-0.5">•</span>
                            <span>{detail}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="mt-4 bg-white p-3 rounded-lg">
              <h4 className="font-bold text-sm mb-2">💬 Communication Pattern</h4>
              <p className="text-xs text-gray-700">
                Agents communicate via AutoGen's GroupChat mechanism, sharing analysis and building consensus through multi-round discussions.
                The Coordinator orchestrates the workflow, ensuring all perspectives are considered before generating final investment recommendations.
              </p>
            </div>
          </div>
        </div>
      )
    },

    // Slide 9: RAG Architecture
    {
      title: "RAG System Architecture",
      type: "content",
      content: (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-teal-50 to-cyan-50 p-6 rounded-xl">
            <h3 className="text-2xl font-bold mb-4">Knowledge Base for Stock Market Education</h3>

            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="bg-white p-4 rounded-lg shadow">
                <div className="text-3xl mb-2">📄</div>
                <h4 className="font-bold mb-2">Document Processing</h4>
                <ul className="text-sm space-y-1">
                  <li>• PDF & TXT loading</li>
                  <li>• Text chunking (500 chars)</li>
                  <li>• Metadata extraction</li>
                </ul>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <div className="text-3xl mb-2">🔢</div>
                <h4 className="font-bold mb-2">Embeddings</h4>
                <ul className="text-sm space-y-1">
                  <li>• HuggingFace MiniLM</li>
                  <li>• Semantic vectors</li>
                  <li>• 76 text chunks</li>
                </ul>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <div className="text-3xl mb-2">🔍</div>
                <h4 className="font-bold mb-2">Vector Search</h4>
                <ul className="text-sm space-y-1">
                  <li>• FAISS index</li>
                  <li>• Cosine similarity</li>
                  <li>• Top-k retrieval</li>
                </ul>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg">
              <h4 className="font-bold mb-3">Query Flow:</h4>
              <div className="flex items-center justify-between">
                <div className="text-center flex-1">
                  <div className="bg-blue-100 p-3 rounded-lg mb-2">📝 User Question</div>
                  <p className="text-xs text-gray-600">Natural language query</p>
                </div>
                <div className="text-2xl mx-2">→</div>
                <div className="text-center flex-1">
                  <div className="bg-purple-100 p-3 rounded-lg mb-2">🔢 Embed Query</div>
                  <p className="text-xs text-gray-600">Convert to vector</p>
                </div>
                <div className="text-2xl mx-2">→</div>
                <div className="text-center flex-1">
                  <div className="bg-green-100 p-3 rounded-lg mb-2">🔍 Search FAISS</div>
                  <p className="text-xs text-gray-600">Find similar docs</p>
                </div>
                <div className="text-2xl mx-2">→</div>
                <div className="text-center flex-1">
                  <div className="bg-orange-100 p-3 rounded-lg mb-2">🤖 LLM + Context</div>
                  <p className="text-xs text-gray-600">Generate answer</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 10: Production Architecture (Bonus)
    {
      title: "Production System Architecture",
      type: "content",
      content: (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-xl">
            <h3 className="text-2xl font-bold mb-4">🚀 Production-Ready Deployment</h3>

            <div className="space-y-4">
              <div className="bg-white p-4 rounded-lg shadow">
                <h4 className="font-bold text-lg mb-3">Infrastructure Components</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="font-semibold text-sm mb-2">🐳 Containerization</p>
                    <ul className="text-xs space-y-1 ml-4">
                      <li>• Docker containers for each service</li>
                      <li>• Docker Compose for local development</li>
                      <li>• Kubernetes for orchestration</li>
                    </ul>
                  </div>
                  <div>
                    <p className="font-semibold text-sm mb-2">⚖️ Load Balancing</p>
                    <ul className="text-xs space-y-1 ml-4">
                      <li>• NGINX reverse proxy</li>
                      <li>• Multiple FastAPI instances</li>
                      <li>• Auto-scaling based on load</li>
                    </ul>
                  </div>
                  <div>
                    <p className="font-semibold text-sm mb-2">💾 Data Layer</p>
                    <ul className="text-xs space-y-1 ml-4">
                      <li>• PostgreSQL for portfolio data</li>
                      <li>• Redis for caching & sessions</li>
                      <li>• S3 for document storage</li>
                    </ul>
                  </div>
                  <div>
                    <p className="font-semibold text-sm mb-2">📊 Monitoring</p>
                    <ul className="text-xs space-y-1 ml-4">
                      <li>• Prometheus metrics collection</li>
                      <li>• Grafana dashboards</li>
                      <li>• ELK stack for logs</li>
                    </ul>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h4 className="font-bold text-lg mb-3">Security & Compliance</h4>
                <div className="grid grid-cols-3 gap-4 text-xs">
                  <div className="p-2 bg-red-50 rounded">
                    <p className="font-semibold mb-1">🔒 Authentication</p>
                    <p>OAuth 2.0 + JWT tokens</p>
                  </div>
                  <div className="p-2 bg-yellow-50 rounded">
                    <p className="font-semibold mb-1">🛡️ API Security</p>
                    <p>Rate limiting, API keys</p>
                  </div>
                  <div className="p-2 bg-green-50 rounded">
                    <p className="font-semibold mb-1">📜 Compliance</p>
                    <p>SOC 2, GDPR ready</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h4 className="font-bold text-lg mb-3">Scalability Strategy</h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="font-semibold mb-2">Horizontal Scaling:</p>
                    <ul className="text-xs space-y-1 ml-4">
                      <li>• Stateless API servers</li>
                      <li>• Agent pool management</li>
                      <li>• Distributed task queue (Celery)</li>
                    </ul>
                  </div>
                  <div>
                    <p className="font-semibold mb-2">Performance Optimization:</p>
                    <ul className="text-xs space-y-1 ml-4">
                      <li>• Response caching (Redis)</li>
                      <li>• Async processing</li>
                      <li>• CDN for frontend assets</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },

    // Slide 11: Key Features Summary
    {
      title: "Key System Features",
      type: "content",
      content: (
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            {[
              {
                title: "🎯 Intelligent Query Routing",
                features: [
                  "LLM-powered intent detection",
                  "Context-aware agent selection",
                  "Fallback handling for ambiguous queries"
                ]
              },
              {
                title: "📊 Real-time Portfolio Analysis",
                features: [
                  "10 client portfolios supported",
                  "Live market data integration",
                  "Return calculations & performance tracking"
                ]
              },
              {
                title: "🤝 Multi-Agent Collaboration",
                features: [
                  "Data synthesis across agents",
                  "Consensus building (AutoGen)",
                  "Conflict resolution"
                ]
              },
              {
                title: "✅ Quality Assurance",
                features: [
                  "Fact checking against source data",
                  "Hallucination detection",
                  "Ambiguity & clarification requests"
                ]
              },
              {
                title: "📚 Knowledge Base (RAG)",
                features: [
                  "Stock market education",
                  "Semantic search with FAISS",
                  "Context-aware answers"
                ]
              },
              {
                title: "🔒 Security & Reliability",
                features: [
                  "Input validation & sanitization",
                  "API rate limiting",
                  "Graceful degradation with fallbacks"
                ]
              }
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white p-6 rounded-xl shadow-lg border-2 border-gray-200"
              >
                <h3 className="text-xl font-bold mb-3">{item.title}</h3>
                <ul className="space-y-2">
                  {item.features.map((feature, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm">
                      <span className="text-green-600 mt-0.5">✓</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      )
    },

    // Slide 12: Thank You
    {
      title: "Thank You",
      type: "title",
      content: (
        <div className="text-center space-y-8">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
          >
            Thank You!
          </motion.h1>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="space-y-4"
          >
            <p className="text-3xl text-gray-700">Questions?</p>
            <div className="text-xl text-gray-500 space-y-2">
              <p>Portfolio Intelligence System</p>
              <p>Multi-Agent AI Architecture</p>
              <p className="text-sm mt-4">Built with LangGraph, AutoGen, and RAG</p>
            </div>
          </motion.div>
        </div>
      )
    }
  ];

  const nextSlide = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    }
  };

  const prevSlide = () => {
    if (currentSlide > 0) {
      setCurrentSlide(currentSlide - 1);
    }
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex flex-col">
      {/* Header */}
      <div className="bg-black bg-opacity-50 backdrop-blur-sm p-4 flex items-center justify-between">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-white hover:text-blue-300 transition-colors"
        >
          <Home className="w-5 h-5" />
          <span>Home</span>
        </button>
        <div className="text-white text-sm">
          Slide {currentSlide + 1} of {slides.length}
        </div>
      </div>

      {/* Main Slide Content */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-6xl">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentSlide}
              initial={{ opacity: 0, x: 100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -100 }}
              transition={{ duration: 0.3 }}
              className="bg-white rounded-2xl shadow-2xl p-12 min-h-[600px]"
            >
              {slides[currentSlide].type === "title" ? (
                <div className="h-full flex items-center justify-center">
                  {slides[currentSlide].content}
                </div>
              ) : (
                <>
                  <h2 className="text-4xl font-bold mb-8 text-gray-800 border-b-4 border-blue-500 pb-4">
                    {slides[currentSlide].title}
                  </h2>
                  <div className="overflow-y-auto max-h-[450px]">
                    {slides[currentSlide].content}
                  </div>
                </>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="bg-black bg-opacity-50 backdrop-blur-sm p-6">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          {/* Previous Button */}
          <button
            onClick={prevSlide}
            disabled={currentSlide === 0}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              currentSlide === 0
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <ChevronLeft className="w-5 h-5" />
            Previous
          </button>

          {/* Slide Indicators */}
          <div className="flex gap-2">
            {slides.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`w-3 h-3 rounded-full transition-all ${
                  index === currentSlide
                    ? 'bg-blue-500 w-8'
                    : 'bg-gray-400 hover:bg-gray-300'
                }`}
              />
            ))}
          </div>

          {/* Next Button */}
          <button
            onClick={nextSlide}
            disabled={currentSlide === slides.length - 1}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              currentSlide === slides.length - 1
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            Next
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default SystemDesignPresentation;
