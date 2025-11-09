import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import ErrorBoundary from './components/ErrorBoundary';
import Home from './pages/Home';
import PortfolioIntelligence from './pages/PortfolioIntelligence';
import StockAnalysis from './pages/StockAnalysis';
import ChatPage from './pages/ChatPage';
import SystemDesignPresentation from './pages/SystemDesignPresentation';
import StockPredictor from './pages/StockPredictor';
import './App.css';

function Navigation() {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Home', icon: '🏠' },
    { path: '/portfolio', label: 'Portfolio Intelligence', icon: '📊' },
    { path: '/stock-analysis', label: 'Stock Analysis', icon: '📈' },
    { path: '/stock-predictor', label: 'Stock Predictor', icon: '🎯' },
    { path: '/chat', label: 'Enhanced Chat', icon: '💬' },
    { path: '/presentation', label: 'System Design', icon: '📊' }
  ];

  return (
    <nav className="sticky top-0 z-50 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white shadow-2xl backdrop-blur-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-3 cursor-pointer group"
          >
            <motion.span 
              className="text-4xl"
              whileHover={{ rotate: 360, scale: 1.2 }}
              transition={{ duration: 0.6 }}
            >
              💼
            </motion.span>
            <div>
              <span className="text-2xl font-extrabold block">Portfolio Intelligence</span>
              <span className="text-xs text-blue-100 block">Powered by AI Multi-Agents</span>
            </div>
          </motion.div>
          
          {/* Navigation Items */}
          <div className="hidden md:flex space-x-2">
            {navItems.map((item, index) => (
              <Link key={item.path} to={item.path}>
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.08, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                    location.pathname === item.path
                      ? 'bg-white text-blue-600 shadow-lg'
                      : 'bg-white/10 hover:bg-white/20 backdrop-blur-sm'
                  }`}
                >
                  <span className="mr-2 text-xl">{item.icon}</span>
                  {item.label}
                </motion.div>
              </Link>
            ))}
          </div>
          
          {/* Mobile Menu Icon */}
          <div className="md:hidden">
            <motion.button
              whileTap={{ scale: 0.9 }}
              className="text-3xl"
            >
              ☰
            </motion.button>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
          <Navigation />
          <ErrorBoundary>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/portfolio" element={<PortfolioIntelligence />} />
              <Route path="/stock-analysis" element={<StockAnalysis />} />
              <Route path="/stock-predictor" element={<StockPredictor />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/presentation" element={<SystemDesignPresentation />} />
            </Routes>
          </ErrorBoundary>
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
