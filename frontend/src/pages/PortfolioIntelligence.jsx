import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

function PortfolioIntelligence() {
  const [selectedClient, setSelectedClient] = useState('CLT-001');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingPortfolio, setLoadingPortfolio] = useState(false);
  const [response, setResponse] = useState(null);
  const [portfolioData, setPortfolioData] = useState(null);
  const [conversationHistory, setConversationHistory] = useState([]);

  // Available clients (CLT-001 to CLT-010)
  const clients = Array.from({ length: 10 }, (_, i) => ({
    id: `CLT-${String(i + 1).padStart(3, '0')}`,
    name: `Client ${i + 1}`
  }));

  const sampleQuestions = [
    "What's the total value of my portfolio?",
    "What stocks do I own?",
    "What's the risk profile of my portfolio?",
    "Which stocks should I consider selling?",
    "How diversified is my portfolio?",
    "What are the growth prospects?",
    "How is my portfolio performing?",
    "Show me my tech sector allocation"
  ];

  // Fetch portfolio data when client changes
  useEffect(() => {
    fetchPortfolioData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedClient]);

  const fetchPortfolioData = async () => {
    if (!selectedClient) return;

    setLoadingPortfolio(true);
    try {
      const result = await axios.get(`http://localhost:8000/api/portfolio/${selectedClient}`);
      setPortfolioData(result.data);
    } catch (error) {
      console.error('Error fetching portfolio:', error);
      // Set mock data for demonstration
      setPortfolioData({
        client_id: selectedClient,
        client_name: clients.find(c => c.id === selectedClient)?.name || 'Unknown',
        total_value: 150000 + Math.random() * 50000,
        holdings: [
          { ticker: 'AAPL', shares: 100, current_price: 182.50, market_value: 18250 },
          { ticker: 'MSFT', shares: 50, current_price: 420.00, market_value: 21000 },
          { ticker: 'GOOGL', shares: 75, current_price: 145.00, market_value: 10875 }
        ],
        ytd_return: 0.12 + Math.random() * 0.1
      });
    } finally {
      setLoadingPortfolio(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || !selectedClient) return;

    setLoading(true);
    try {
      const result = await axios.post('http://localhost:8000/api/query', {
        query: query,
        client_id: selectedClient,
        conversation_history: conversationHistory
      });

      setResponse(result.data);

      // Add to conversation history
      setConversationHistory(prev => [
        ...prev,
        { role: 'user', content: query },
        { role: 'assistant', content: result.data.answer }
      ]);
    } catch (error) {
      setResponse({
        answer: `Error: ${error.message}. The backend API might not be running. Please start the LangGraph backend on port 8000.`,
        agents_used: [],
        metadata: {}
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto"
      >
        <h1 className="text-4xl font-bold mb-2 text-gray-800">
          📊 Portfolio Intelligence
        </h1>
        <p className="text-gray-600 mb-8">
          Ask questions about your portfolio and get AI-powered insights
        </p>

        {/* Client Selection */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Select Client
          </label>
          <select
            value={selectedClient}
            onChange={(e) => setSelectedClient(e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none bg-white"
          >
            {clients.map(client => (
              <option key={client.id} value={client.id}>
                {client.id} - {client.name}
              </option>
            ))}
          </select>
        </div>

        {/* Portfolio Summary */}
        {loadingPortfolio ? (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <div className="flex items-center justify-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-3 text-gray-600">Loading portfolio data...</span>
            </div>
          </div>
        ) : portfolioData && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl shadow-lg p-6 mb-6 border-2 border-blue-100"
          >
            <h2 className="text-xl font-bold mb-4 text-gray-800">
              Portfolio Summary - {portfolioData.client_name}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Total Value */}
              <div className="bg-white rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600 mb-1">Total Value</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${(portfolioData.total_value || 0).toLocaleString('en-US', { maximumFractionDigits: 0 })}
                </p>
              </div>

              {/* Number of Holdings */}
              <div className="bg-white rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600 mb-1">Holdings</p>
                <p className="text-2xl font-bold text-gray-900">
                  {portfolioData.holdings?.length || 0}
                </p>
                <p className="text-xs text-gray-500">stocks</p>
              </div>

              {/* YTD Return */}
              <div className="bg-white rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600 mb-1">YTD Return</p>
                <p className={`text-2xl font-bold ${(portfolioData.ytd_return || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {(portfolioData.ytd_return || 0) >= 0 ? '+' : ''}{((portfolioData.ytd_return || 0) * 100).toFixed(1)}%
                </p>
              </div>

              {/* Top Holding */}
              <div className="bg-white rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600 mb-1">Top Holding</p>
                <p className="text-2xl font-bold text-gray-900">
                  {portfolioData.holdings?.[0]?.symbol || portfolioData.holdings?.[0]?.ticker || 'N/A'}
                </p>
                <p className="text-xs text-gray-500">
                  ${(portfolioData.holdings?.[0]?.market_value || 0).toLocaleString()}
                </p>
              </div>
            </div>

            {/* Holdings List */}
            {portfolioData.holdings && portfolioData.holdings.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-semibold text-gray-700 mb-2">Current Holdings:</p>
                <div className="flex flex-wrap gap-2">
                  {portfolioData.holdings.map((holding, i) => (
                    <span
                      key={i}
                      className="px-3 py-1 bg-white rounded-full text-sm font-medium text-gray-700 shadow-sm"
                    >
                      {holding.symbol || holding.ticker} ({holding.quantity || holding.shares} shares)
                    </span>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}

        {/* Portfolio Analytics Charts */}
        {portfolioData && portfolioData.holdings && portfolioData.holdings.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <h2 className="text-2xl font-bold mb-4 text-gray-800 flex items-center">
              <span className="mr-2">📈</span>
              Portfolio Analytics
            </h2>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              {/* Holdings Distribution (Pie Chart) */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-800">Holdings Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={portfolioData.holdings.map((h, i) => ({
                        name: h.symbol || h.ticker,
                        value: h.market_value || ((h.quantity || h.shares) * h.current_price) || 0,
                        color: `hsl(${(i * 360) / portfolioData.holdings.length}, 70%, 60%)`
                      }))}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {portfolioData.holdings.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={`hsl(${(index * 360) / portfolioData.holdings.length}, 70%, 60%)`} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Holdings Value (Bar Chart) */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-800">Holdings Value</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={portfolioData.holdings.map(h => ({
                      name: h.symbol || h.ticker,
                      value: h.market_value || ((h.quantity || h.shares) * h.current_price) || 0
                    })).sort((a, b) => b.value - a.value)}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                    <Bar dataKey="value" fill="#8b5cf6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Holdings Detail Table */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold mb-4 text-gray-800">Holdings Details</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 border-b-2 border-gray-200">
                    <tr>
                      <th className="px-4 py-3 text-left font-semibold text-gray-700">Symbol</th>
                      <th className="px-4 py-3 text-right font-semibold text-gray-700">Shares</th>
                      <th className="px-4 py-3 text-right font-semibold text-gray-700">Avg Price</th>
                      <th className="px-4 py-3 text-right font-semibold text-gray-700">Current Price</th>
                      <th className="px-4 py-3 text-right font-semibold text-gray-700">Market Value</th>
                      <th className="px-4 py-3 text-right font-semibold text-gray-700">Gain/Loss</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {portfolioData.holdings.map((holding, i) => {
                      const currentPrice = holding.current_price || holding.purchase_price || holding.avg_price || 0;
                      const avgPrice = holding.purchase_price || holding.avg_price || holding.current_price || 0;
                      const shares = holding.quantity || holding.shares || 0;
                      const marketValue = holding.market_value || (shares * currentPrice);
                      const gainLoss = ((currentPrice - avgPrice) / avgPrice) * 100;

                      return (
                        <tr key={i} className="hover:bg-gray-50">
                          <td className="px-4 py-3 font-medium text-gray-900">
                            {holding.ticker || holding.symbol}
                          </td>
                          <td className="px-4 py-3 text-right text-gray-700">
                            {shares.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right text-gray-700">
                            ${avgPrice.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-gray-700">
                            ${currentPrice.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right font-semibold text-gray-900">
                            ${marketValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                          </td>
                          <td className={`px-4 py-3 text-right font-semibold ${
                            gainLoss >= 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {gainLoss >= 0 ? '+' : ''}{gainLoss.toFixed(2)}%
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                  <tfoot className="bg-gray-50 border-t-2 border-gray-200">
                    <tr>
                      <td colSpan="4" className="px-4 py-3 text-right font-bold text-gray-900">
                        Total Portfolio Value:
                      </td>
                      <td className="px-4 py-3 text-right font-bold text-gray-900">
                        ${portfolioData.total_value?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </td>
                      <td></td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </motion.div>
        )}

        {/* Query Input */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <form onSubmit={handleSubmit}>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Your Question
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask about your portfolio..."
                className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
              />
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '⏳ Analyzing...' : '🚀 Analyze'}
              </motion.button>
            </div>
          </form>

          {/* Sample Questions */}
          <div className="mt-4">
            <p className="text-sm text-gray-500 mb-2">Try these questions:</p>
            <div className="flex flex-wrap gap-2">
              {sampleQuestions.map((q, i) => (
                <button
                  key={i}
                  onClick={() => setQuery(q)}
                  className="text-sm px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Response */}
        {response && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-6"
          >
            <h2 className="text-xl font-bold mb-4 text-gray-800 flex items-center">
              <span className="mr-2">💡</span>
              Analysis Result
            </h2>

            {/* Agent Timeline */}
            {response.agents_used && response.agents_used.length > 0 && (
              <div className="mb-6 pb-6 border-b border-gray-200">
                <p className="text-sm font-semibold text-gray-600 mb-3">Agent Activity:</p>
                <div className="flex items-center justify-between gap-2">
                  {response.agents_used.map((agent, i) => (
                    <React.Fragment key={i}>
                      <div className="flex flex-col items-center">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold shadow-lg">
                          ✓
                        </div>
                        <p className="text-xs text-gray-600 mt-1 text-center">
                          {agent.replace('_', ' ')}
                        </p>
                      </div>
                      {i < response.agents_used.length - 1 && (
                        <div className="flex-1 h-0.5 bg-gradient-to-r from-blue-500 to-purple-500"></div>
                      )}
                    </React.Fragment>
                  ))}
                </div>
              </div>
            )}

            <div className="prose prose-sm max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  h1: ({node, ...props}) => <h1 className="text-2xl font-bold mb-3 mt-4 text-gray-900" {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-xl font-bold mb-2 mt-4 text-gray-800" {...props} />,
                  h3: ({node, ...props}) => <h3 className="text-lg font-semibold mb-2 mt-3 text-gray-800" {...props} />,
                  p: ({node, ...props}) => <p className="mb-3 text-gray-700 leading-relaxed" {...props} />,
                  ul: ({node, ...props}) => <ul className="list-disc ml-6 mb-3 space-y-1" {...props} />,
                  ol: ({node, ...props}) => <ol className="list-decimal ml-6 mb-3 space-y-1" {...props} />,
                  li: ({node, ...props}) => <li className="text-gray-700" {...props} />,
                  strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />,
                  code: ({node, inline, ...props}) =>
                    inline ?
                      <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-blue-600" {...props} /> :
                      <code className="block bg-gray-800 text-white p-3 rounded my-2 text-sm font-mono overflow-x-auto" {...props} />,
                }}
              >
                {response.answer}
              </ReactMarkdown>
            </div>

            {/* Metadata */}
            {response.metadata && Object.keys(response.metadata).length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {response.metadata.execution_time !== undefined && (
                    <div className="text-center p-2 bg-gray-50 rounded">
                      <p className="text-xs text-gray-500">Execution Time</p>
                      <p className="text-sm font-semibold text-gray-700">
                        {Number(response.metadata.execution_time).toFixed(2)}s
                      </p>
                    </div>
                  )}
                  {response.metadata.workflow_steps !== undefined && (
                    <div className="text-center p-2 bg-gray-50 rounded">
                      <p className="text-xs text-gray-500">Workflow Steps</p>
                      <p className="text-sm font-semibold text-gray-700">
                        {response.metadata.workflow_steps}
                      </p>
                    </div>
                  )}
                  {response.metadata.validated !== undefined && (
                    <div className="text-center p-2 bg-gray-50 rounded">
                      <p className="text-xs text-gray-500">Validated</p>
                      <p className="text-sm font-semibold text-gray-700">
                        {response.metadata.validated ? '✓ Yes' : '✗ No'}
                      </p>
                    </div>
                  )}
                  {response.agents_used && Array.isArray(response.agents_used) && (
                    <div className="text-center p-2 bg-gray-50 rounded">
                      <p className="text-xs text-gray-500">Agents Used</p>
                      <p className="text-sm font-semibold text-gray-700">
                        {response.agents_used.length}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {response.sources && response.sources.length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-sm font-semibold text-gray-600 mb-2">Sources:</p>
                <ul className="list-disc list-inside text-sm text-gray-600">
                  {response.sources.map((source, i) => (
                    <li key={i}>{source}</li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}

        {/* Conversation History */}
        {conversationHistory.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-800 flex items-center">
                <span className="mr-2">💬</span>
                Conversation History
              </h2>
              <button
                onClick={() => setConversationHistory([])}
                className="text-sm text-red-600 hover:text-red-700 font-medium"
              >
                Clear History
              </button>
            </div>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {conversationHistory.map((msg, i) => (
                <div
                  key={i}
                  className={`p-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-blue-50 border-l-4 border-blue-500'
                      : 'bg-gray-50 border-l-4 border-purple-500'
                  }`}
                >
                  <p className="text-xs font-semibold text-gray-500 mb-1">
                    {msg.role === 'user' ? '👤 You' : '🤖 AI Assistant'}
                  </p>
                  {msg.role === 'user' ? (
                    <p className="text-sm text-gray-700">{msg.content}</p>
                  ) : (
                    <div className="prose prose-sm max-w-none text-sm">
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          h2: ({node, ...props}) => <h2 className="text-base font-bold mb-1 mt-2 text-gray-800" {...props} />,
                          p: ({node, ...props}) => <p className="mb-2 text-gray-700" {...props} />,
                          ul: ({node, ...props}) => <ul className="list-disc ml-4 mb-2 space-y-0.5" {...props} />,
                          li: ({node, ...props}) => <li className="text-gray-700 text-sm" {...props} />,
                          strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />,
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Info Banner */}
        <div className="mt-6 bg-blue-50 border-2 border-blue-200 rounded-xl p-4">
          <div className="flex items-start">
            <span className="text-2xl mr-3">ℹ️</span>
            <div>
              <h3 className="font-semibold text-blue-900 mb-1">About Portfolio Intelligence</h3>
              <p className="text-sm text-blue-700">
                This system uses LangGraph multi-agent workflow to analyze portfolios. 
                Agents collaborate to provide comprehensive insights on risk, diversification, 
                and investment opportunities based on real market data from Alpha Vantage API.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

export default PortfolioIntelligence;
