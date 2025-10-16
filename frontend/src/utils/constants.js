export const CLIENTS = [
  { id: 'CLT-001', initials: 'C1', holdings: 7 },
  { id: 'CLT-002', initials: 'C2', holdings: 8 },
  { id: 'CLT-003', initials: 'C3', holdings: 5 },
  { id: 'CLT-004', initials: 'C4', holdings: 12 },
  { id: 'CLT-005', initials: 'C5', holdings: 6 },
];

export const QUERY_SUGGESTIONS = [
  "What stocks do I own?",
  "Which holdings have the best return?",
  "Show my portfolio allocation",
  "What's the current price of AAPL?",
  "How is my portfolio performing?",
  "Get the latest SEC filings for TSLA",
  "What are the top gainers in my portfolio?",
  "Show me high-risk holdings"
];

export const AGENT_NAMES = {
  PLANNER: 'Planner',
  PORTFOLIO: 'Portfolio',
  MARKET: 'Market',
  SEC: 'SEC',
  COLLABORATION: 'Collaboration',
  VALIDATOR: 'Validator'
};

export const AGENT_DESCRIPTIONS = {
  [AGENT_NAMES.PLANNER]: 'Analyzes queries and plans the execution strategy',
  [AGENT_NAMES.PORTFOLIO]: 'Manages and retrieves portfolio data',
  [AGENT_NAMES.MARKET]: 'Fetches real-time market data and prices',
  [AGENT_NAMES.SEC]: 'Retrieves SEC filings and regulatory documents',
  [AGENT_NAMES.COLLABORATION]: 'Coordinates multiple agents for complex queries',
  [AGENT_NAMES.VALIDATOR]: 'Validates and quality-checks responses'
};

export const KEYBOARD_SHORTCUTS = [
  { keys: ['Cmd', 'K'], description: 'Focus query input', mac: true },
  { keys: ['Ctrl', 'K'], description: 'Focus query input', mac: false },
  { keys: ['Cmd', 'Enter'], description: 'Submit query', mac: true },
  { keys: ['Ctrl', 'Enter'], description: 'Submit query', mac: false },
  { keys: ['Cmd', '/'], description: 'Show shortcuts', mac: true },
  { keys: ['Ctrl', '/'], description: 'Show shortcuts', mac: false },
  { keys: ['Esc'], description: 'Close modals', mac: null }
];

export const ROUTES = {
  DASHBOARD: '/',
  PORTFOLIO: '/portfolio',
  ANALYTICS: '/analytics'
};
