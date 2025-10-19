/**
 * 20 Companies for Stock Analysis
 */

export const companies = [
  {
    symbol: "AAPL",
    name: "Apple Inc.",
    sector: "Technology",
    logo: "🍎",
    description: "Consumer electronics and software company"
  },
  {
    symbol: "MSFT",
    name: "Microsoft Corporation",
    sector: "Technology",
    logo: "🪟",
    description: "Software, cloud computing, and AI"
  },
  {
    symbol: "GOOGL",
    name: "Alphabet Inc.",
    sector: "Technology",
    logo: "🔍",
    description: "Search engine, advertising, and cloud"
  },
  {
    symbol: "AMZN",
    name: "Amazon.com Inc.",
    sector: "Consumer Cyclical",
    logo: "📦",
    description: "E-commerce and cloud computing"
  },
  {
    symbol: "NVDA",
    name: "NVIDIA Corporation",
    sector: "Technology",
    logo: "🎮",
    description: "Graphics processing units and AI chips"
  },
  {
    symbol: "TSLA",
    name: "Tesla Inc.",
    sector: "Automotive",
    logo: "⚡",
    description: "Electric vehicles and clean energy"
  },
  {
    symbol: "META",
    name: "Meta Platforms Inc.",
    sector: "Technology",
    logo: "📘",
    description: "Social media and metaverse"
  },
  {
    symbol: "BRK.B",
    name: "Berkshire Hathaway",
    sector: "Financial",
    logo: "💰",
    description: "Diversified holding company"
  },
  {
    symbol: "JPM",
    name: "JPMorgan Chase & Co.",
    sector: "Financial",
    logo: "🏦",
    description: "Banking and financial services"
  },
  {
    symbol: "V",
    name: "Visa Inc.",
    sector: "Financial",
    logo: "💳",
    description: "Payment processing technology"
  },
  {
    symbol: "JNJ",
    name: "Johnson & Johnson",
    sector: "Healthcare",
    logo: "🏥",
    description: "Pharmaceuticals and medical devices"
  },
  {
    symbol: "WMT",
    name: "Walmart Inc.",
    sector: "Retail",
    logo: "🛒",
    description: "Retail corporation"
  },
  {
    symbol: "PG",
    name: "Procter & Gamble Co.",
    sector: "Consumer Defensive",
    logo: "🧴",
    description: "Consumer goods"
  },
  {
    symbol: "MA",
    name: "Mastercard Inc.",
    sector: "Financial",
    logo: "💳",
    description: "Payment processing services"
  },
  {
    symbol: "HD",
    name: "The Home Depot Inc.",
    sector: "Retail",
    logo: "🔨",
    description: "Home improvement retail"
  },
  {
    symbol: "DIS",
    name: "The Walt Disney Company",
    sector: "Entertainment",
    logo: "🏰",
    description: "Entertainment and media"
  },
  {
    symbol: "NFLX",
    name: "Netflix Inc.",
    sector: "Entertainment",
    logo: "🎬",
    description: "Streaming entertainment"
  },
  {
    symbol: "KO",
    name: "The Coca-Cola Company",
    sector: "Beverage",
    logo: "🥤",
    description: "Beverage manufacturer"
  },
  {
    symbol: "PEP",
    name: "PepsiCo Inc.",
    sector: "Beverage",
    logo: "🥤",
    description: "Food and beverage company"
  },
  {
    symbol: "NKE",
    name: "Nike Inc.",
    sector: "Apparel",
    logo: "👟",
    description: "Athletic footwear and apparel"
  }
];

// Helper function to get company by symbol
export const getCompanyBySymbol = (symbol) => {
  return companies.find(c => c.symbol === symbol);
};

// Helper function to search companies
export const searchCompanies = (query) => {
  const lowerQuery = query.toLowerCase();
  return companies.filter(c => 
    c.symbol.toLowerCase().includes(lowerQuery) ||
    c.name.toLowerCase().includes(lowerQuery) ||
    c.sector.toLowerCase().includes(lowerQuery)
  );
};
