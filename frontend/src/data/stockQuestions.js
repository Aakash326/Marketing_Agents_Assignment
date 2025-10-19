/**
 * 20 Stock Analysis Questions for 6-Agent Trading System
 * Categories: Buy/Sell Decisions, Investment Horizon, Risk Analysis, Valuation, Market Timing
 */

export const stockQuestions = [
  // Buy/Sell Decision Questions
  {
    id: 1,
    text: "Should I buy this stock?",
    category: "buy_sell",
    icon: "🛒",
    description: "Get a comprehensive buy recommendation with technical and fundamental analysis"
  },
  {
    id: 2,
    text: "Should I sell this stock?",
    category: "buy_sell",
    icon: "💰",
    description: "Determine if it's the right time to exit your position"
  },
  {
    id: 3,
    text: "Is this a good time to buy?",
    category: "timing",
    icon: "⏰",
    description: "Analyze current market timing and entry points"
  },
  {
    id: 4,
    text: "Is this stock overvalued or undervalued?",
    category: "valuation",
    icon: "💎",
    description: "Get valuation analysis based on fundamentals and technicals"
  },

  // Investment Horizon Questions
  {
    id: 5,
    text: "Should I invest in this for 1 year?",
    category: "horizon",
    icon: "📅",
    description: "1-year investment outlook with price targets"
  },
  {
    id: 6,
    text: "Is this good for long-term investment (5+ years)?",
    category: "horizon",
    icon: "🎯",
    description: "Long-term growth potential and sustainability analysis"
  },
  {
    id: 7,
    text: "Is this suitable for short-term trading?",
    category: "horizon",
    icon: "⚡",
    description: "Short-term trading opportunities and momentum analysis"
  },
  {
    id: 8,
    text: "Should I hold this stock for 3-6 months?",
    category: "horizon",
    icon: "🗓️",
    description: "Medium-term outlook and catalysts"
  },

  // Risk Analysis Questions
  {
    id: 9,
    text: "What are the risks of investing in this stock?",
    category: "risk",
    icon: "⚠️",
    description: "Comprehensive risk assessment and mitigation strategies"
  },
  {
    id: 10,
    text: "How volatile is this stock?",
    category: "risk",
    icon: "📊",
    description: "Volatility metrics and historical price movements"
  },
  {
    id: 11,
    text: "What is my potential gain/loss ratio?",
    category: "risk",
    icon: "⚖️",
    description: "Risk-reward analysis with stop-loss recommendations"
  },
  {
    id: 12,
    text: "Is this stock too risky for my portfolio?",
    category: "risk",
    icon: "🛡️",
    description: "Risk profile assessment based on your portfolio"
  },

  // Price Target & Growth Questions
  {
    id: 13,
    text: "What is the price target for this stock?",
    category: "target",
    icon: "🎯",
    description: "Analyst consensus and AI-calculated price targets"
  },
  {
    id: 14,
    text: "Can this stock double in value?",
    category: "growth",
    icon: "📈",
    description: "Growth potential and catalysts for price appreciation"
  },
  {
    id: 15,
    text: "What are the growth prospects?",
    category: "growth",
    icon: "🚀",
    description: "Revenue growth, earnings projections, and expansion plans"
  },

  // Market Conditions & Timing
  {
    id: 16,
    text: "How is the market sentiment for this stock?",
    category: "sentiment",
    icon: "💭",
    description: "News sentiment, social media buzz, and analyst ratings"
  },
  {
    id: 17,
    text: "What do technical indicators suggest?",
    category: "technical",
    icon: "📉",
    description: "RSI, MACD, moving averages, and chart patterns"
  },
  {
    id: 18,
    text: "Are there any upcoming catalysts?",
    category: "catalysts",
    icon: "🔔",
    description: "Earnings reports, product launches, and market events"
  },

  // Strategy Questions
  {
    id: 19,
    text: "What is the best entry and exit strategy?",
    category: "strategy",
    icon: "🎲",
    description: "Optimal entry points, stop-loss, and take-profit levels"
  },
  {
    id: 20,
    text: "Should I add this to my diversified portfolio?",
    category: "portfolio",
    icon: "📂",
    description: "Portfolio fit analysis and diversification benefits"
  }
];

// Group questions by category for easy filtering
export const questionsByCategory = {
  buy_sell: stockQuestions.filter(q => q.category === 'buy_sell'),
  horizon: stockQuestions.filter(q => q.category === 'horizon'),
  risk: stockQuestions.filter(q => q.category === 'risk'),
  target: stockQuestions.filter(q => q.category === 'target'),
  growth: stockQuestions.filter(q => q.category === 'growth'),
  sentiment: stockQuestions.filter(q => q.category === 'sentiment'),
  technical: stockQuestions.filter(q => q.category === 'technical'),
  catalysts: stockQuestions.filter(q => q.category === 'catalysts'),
  strategy: stockQuestions.filter(q => q.category === 'strategy'),
  portfolio: stockQuestions.filter(q => q.category === 'portfolio'),
  valuation: stockQuestions.filter(q => q.category === 'valuation'),
  timing: stockQuestions.filter(q => q.category === 'timing')
};

export default stockQuestions;
