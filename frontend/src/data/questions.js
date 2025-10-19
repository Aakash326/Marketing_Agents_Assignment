/**
 * 20 Investment Questions for Stock Analysis
 */

export const questions = [
  {
    id: 1,
    text: "Should I invest now?",
    icon: "📊",
    category: "decision",
    description: "Get a buy/sell/hold recommendation based on current market conditions"
  },
  {
    id: 2,
    text: "Should I sell my holdings?",
    icon: "💰",
    category: "decision",
    description: "Analyze if it's the right time to exit your position"
  },
  {
    id: 3,
    text: "Is it good for long-term (5+ years)?",
    icon: "📈",
    category: "timeframe",
    description: "Long-term investment potential analysis"
  },
  {
    id: 4,
    text: "Should I invest for 1 year?",
    icon: "⏰",
    category: "timeframe",
    description: "Short to medium-term investment outlook"
  },
  {
    id: 5,
    text: "What's the risk level?",
    icon: "⚠️",
    category: "risk",
    description: "Comprehensive risk assessment and volatility analysis"
  },
  {
    id: 6,
    text: "What's the potential return?",
    icon: "💹",
    category: "returns",
    description: "Expected returns and price target analysis"
  },
  {
    id: 7,
    text: "Is the stock overvalued?",
    icon: "📉",
    category: "valuation",
    description: "Valuation metrics and fair value assessment"
  },
  {
    id: 8,
    text: "Is the stock undervalued?",
    icon: "📊",
    category: "valuation",
    description: "Identify potential value opportunities"
  },
  {
    id: 9,
    text: "What's the growth potential?",
    icon: "🚀",
    category: "growth",
    description: "Future growth prospects and catalysts"
  },
  {
    id: 10,
    text: "Should I buy the dip?",
    icon: "💎",
    category: "timing",
    description: "Analyze if current price drop is a buying opportunity"
  },
  {
    id: 11,
    text: "What's the dividend yield?",
    icon: "💵",
    category: "income",
    description: "Dividend analysis and income potential"
  },
  {
    id: 12,
    text: "How is the company performing?",
    icon: "📊",
    category: "fundamentals",
    description: "Financial health and operational performance"
  },
  {
    id: 13,
    text: "What are the major risks?",
    icon: "🔴",
    category: "risk",
    description: "Identify key risk factors and concerns"
  },
  {
    id: 14,
    text: "Compare with competitors",
    icon: "⚖️",
    category: "comparison",
    description: "Competitive positioning and market share analysis"
  },
  {
    id: 15,
    text: "What do analysts recommend?",
    icon: "👔",
    category: "sentiment",
    description: "Wall Street consensus and price targets"
  },
  {
    id: 16,
    text: "Recent news and developments",
    icon: "📰",
    category: "news",
    description: "Latest news, events, and their impact"
  },
  {
    id: 17,
    text: "Technical analysis overview",
    icon: "📈",
    category: "technical",
    description: "Chart patterns, trends, and technical indicators"
  },
  {
    id: 18,
    text: "Best entry price point?",
    icon: "🎯",
    category: "timing",
    description: "Optimal entry price and timing strategy"
  },
  {
    id: 19,
    text: "When should I take profits?",
    icon: "💰",
    category: "strategy",
    description: "Exit strategy and profit-taking levels"
  },
  {
    id: 20,
    text: "Portfolio allocation suggestion",
    icon: "🥧",
    category: "strategy",
    description: "Recommended position sizing for your portfolio"
  }
];

// Helper function to get question by ID
export const getQuestionById = (id) => {
  return questions.find(q => q.id === id);
};

// Helper function to get questions by category
export const getQuestionsByCategory = (category) => {
  return questions.filter(q => q.category === category);
};

// Get all categories
export const categories = [...new Set(questions.map(q => q.category))];
