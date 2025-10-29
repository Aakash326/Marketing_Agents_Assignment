import React, { useState } from 'react';
import ChatMessages from '../components/ChatMessages';
import ChatInput from '../components/ChatInput';
import { BookOpen, Sparkles } from 'lucide-react';
import { ragQuery } from '../services/api';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleQuery = async (query) => {
    // Add user message immediately
    setMessages(prev => [...prev, { role: 'user', content: query }]);
    setIsLoading(true);

    try {
      const ragRes = await ragQuery(query, 4);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: ragRes.answer || 'No answer found.',
        sources: ragRes.sources
      }]);
    } catch (error) {
      console.error('Error querying RAG:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, an error occurred while processing your question about stock markets.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const suggestions = [
    "What is a P/E ratio?",
    "Explain the difference between stocks and bonds",
    "What are the main types of stocks?",
    "How does the stock market work?",
    "What is market capitalization?",
    "Explain dividend yields"
  ];

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-md p-6 border-b-4 border-gradient-to-r from-blue-500 to-purple-500">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Stock Market Knowledge Assistant
              </h1>
              <p className="text-gray-600 text-sm mt-1">Ask me anything about stocks, trading, and market concepts</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden max-w-6xl mx-auto w-full p-6">
        <div className="h-full flex flex-col space-y-4">

          {/* Suggestion Pills */}
          {messages.length === 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-5 h-5 text-purple-600" />
                <h2 className="text-lg font-semibold text-gray-800">Quick Questions</h2>
              </div>
              <div className="flex flex-wrap gap-2">
                {suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuery(suggestion)}
                    className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-full text-sm font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>

              <div className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-200">
                <p className="text-sm text-gray-700">
                  💡 <strong>Tip:</strong> This assistant uses RAG (Retrieval-Augmented Generation) to provide accurate answers about stock market concepts from our knowledge base.
                </p>
              </div>
            </div>
          )}

          {/* Chat Messages */}
          <div className="flex-1 overflow-hidden bg-white rounded-2xl shadow-lg">
            <ChatMessages messages={messages} />
          </div>

          {/* Loading Indicator */}
          {isLoading && (
            <div className="flex items-center justify-center gap-2 text-blue-600">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <span className="text-sm font-medium">Searching knowledge base...</span>
            </div>
          )}

          {/* Chat Input */}
          <ChatInput onSubmit={handleQuery} placeholder="Ask about stocks, P/E ratios, bonds, market concepts..." />
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
