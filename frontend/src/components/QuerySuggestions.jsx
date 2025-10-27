import React, { useEffect, useState } from 'react';
import { ChevronDown, ChevronUp, Sparkles } from 'lucide-react';

const QuerySuggestions = ({ clientId, onSelect }) => {
  const [suggestions, setSuggestions] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('portfolio');

  useEffect(() => {
    fetchSuggestions();
  }, [clientId]);

  const fetchSuggestions = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/portfolio/${clientId}/query-suggestions`
      );
      const data = await response.json();
      setSuggestions(data);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  if (!suggestions) return null;

  const categories = [
    { key: 'portfolio', label: 'Portfolio', icon: '📊' },
    { key: 'performance', label: 'Performance', icon: '📈' },
    { key: 'market', label: 'Market', icon: '🌐' },
    { key: 'analysis', label: 'Analysis', icon: '🔍' }
  ];

  return (
    <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-200">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between text-left"
      >
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-blue-600" />
          <span className="font-semibold text-gray-800">
            Quick Query Suggestions
          </span>
        </div>
        {expanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
      </button>

      {expanded && (
        <div className="mt-4 space-y-3">
          {/* Category Tabs */}
          <div className="flex gap-2 flex-wrap">
            {categories.map(cat => (
              <button
                key={cat.key}
                onClick={() => setSelectedCategory(cat.key)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  selectedCategory === cat.key
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                {cat.icon} {cat.label}
              </button>
            ))}
          </div>

          {/* Suggestion Buttons */}
          <div className="grid grid-cols-2 gap-2">
            {suggestions[selectedCategory]?.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => onSelect(suggestion)}
                className="border border-gray-300 bg-white rounded-lg px-3 py-3 text-left text-sm hover:bg-blue-100 hover:border-blue-300 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuerySuggestions;
