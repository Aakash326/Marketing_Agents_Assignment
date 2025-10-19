import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  const features = [
    {
      icon: '🤖',
      title: 'Multi-Agent System',
      description: 'Powered by LangGraph and AutoGen with 6 specialized agents',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: '📊',
      title: 'Portfolio Intelligence',
      description: 'Real-time portfolio analysis and recommendations',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: '📈',
      title: 'Stock Analysis',
      description: 'Comprehensive fundamental and technical analysis',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: '💡',
      title: 'Alpha Vantage Integration',
      description: 'Real market data with intelligent fallback mechanisms',
      color: 'from-orange-500 to-red-500'
    }
  ];

  const tools = [
    { name: 'Portfolio Intelligence', path: '/portfolio', icon: '📊', desc: 'Analyze your portfolio with AI agents' },
    { name: 'Stock Analysis', path: '/stock-analysis', icon: '📈', desc: '6-agent trading workflow' }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 text-white py-24 overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-white rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse-scale"></div>
        </div>
        
        <div className="container mx-auto px-4 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-5xl mx-auto"
          >
            <motion.div 
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-7xl mb-6"
            >
              💼📊🤖
            </motion.div>
            
            <h1 className="text-6xl md:text-7xl font-extrabold mb-6 bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent">
              Portfolio Intelligence System
            </h1>
            
            <p className="text-2xl md:text-3xl mb-10 text-blue-50 font-light">
              AI-Powered Investment Analysis with Multi-Agent Architecture
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <motion.button
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/portfolio')}
                className="bg-white text-blue-600 px-10 py-5 rounded-2xl font-bold text-xl shadow-2xl hover:shadow-3xl transition-all flex items-center justify-center gap-2 group"
              >
                <span>📊</span>
                Try Portfolio Analysis
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/stock-analysis')}
                className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-10 py-5 rounded-2xl font-bold text-xl shadow-2xl hover:shadow-3xl transition-all border-2 border-white/30 flex items-center justify-center gap-2 group"
              >
                <span>📈</span>
                Stock Analysis
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </motion.button>
            </div>
          </motion.div>
        </div>
        
        {/* Wave decoration */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 100" className="w-full">
            <path fill="#f9fafb" fillOpacity="1" d="M0,32L48,37.3C96,43,192,53,288,58.7C384,64,480,64,576,58.7C672,53,768,43,864,42.7C960,43,1056,53,1152,53.3C1248,53,1344,43,1392,37.3L1440,32L1440,100L1392,100C1344,100,1248,100,1152,100C1056,100,960,100,864,100C768,100,672,100,576,100C480,100,384,100,288,100C192,100,96,100,48,100L0,100Z"></path>
          </svg>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-5xl font-extrabold text-center mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Powerful Features
          </h2>
          <p className="text-center text-gray-600 mb-16 text-lg">
            Built with cutting-edge AI technology for smarter investment decisions
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.15, duration: 0.6 }}
              viewport={{ once: true }}
              whileHover={{ y: -8, scale: 1.02 }}
              className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all border border-gray-100 group cursor-pointer"
            >
              <div className={`text-6xl mb-6 transform group-hover:scale-110 transition-transform duration-300`}>
                {feature.icon}
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-800 group-hover:text-blue-600 transition-colors">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              <div className={`mt-4 h-1 w-0 group-hover:w-full transition-all duration-300 bg-gradient-to-r ${feature.color} rounded-full`}></div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Tools Section */}
      <div className="relative bg-gradient-to-br from-gray-50 to-blue-50 py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl font-extrabold text-center mb-4 text-gray-800">
              Get Started Now
            </h2>
            <p className="text-center text-gray-600 mb-16 text-lg">
              Choose your analysis tool and unlock powerful insights
            </p>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {tools.map((tool, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index === 0 ? -30 : 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.2, duration: 0.6 }}
                viewport={{ once: true }}
                whileHover={{ y: -10, scale: 1.03 }}
                onClick={() => navigate(tool.path)}
                className="group relative bg-white rounded-3xl p-10 shadow-xl hover:shadow-3xl transition-all cursor-pointer overflow-hidden border-2 border-gray-100 hover:border-blue-400"
              >
                {/* Background gradient on hover */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-purple-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                
                <div className="relative z-10">
                  <motion.div 
                    className="text-7xl mb-6"
                    whileHover={{ rotate: 360, scale: 1.2 }}
                    transition={{ duration: 0.6 }}
                  >
                    {tool.icon}
                  </motion.div>
                  <h3 className="text-3xl font-bold mb-3 text-gray-800 group-hover:text-blue-600 transition-colors">
                    {tool.name}
                  </h3>
                  <p className="text-gray-600 mb-6 text-lg leading-relaxed">{tool.desc}</p>
                  <div className="flex items-center text-blue-600 font-bold text-lg group-hover:translate-x-2 transition-transform">
                    Launch Tool
                    <motion.span 
                      className="ml-2 text-2xl"
                      animate={{ x: [0, 5, 0] }}
                      transition={{ repeat: Infinity, duration: 1.5 }}
                    >
                      →
                    </motion.span>
                  </div>
                </div>
                
                {/* Decorative corner */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-400 to-purple-400 opacity-10 rounded-bl-full group-hover:opacity-20 transition-opacity"></div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Status Section */}
      <div className="container mx-auto px-4 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="relative bg-gradient-to-r from-green-50 via-emerald-50 to-teal-50 rounded-3xl p-10 border-2 border-green-200 shadow-xl overflow-hidden"
        >
          {/* Decorative elements */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-green-200 opacity-10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-emerald-200 opacity-10 rounded-full blur-3xl"></div>
          
          <div className="relative z-10">
            <div className="flex flex-col md:flex-row items-center justify-center gap-4 mb-6">
              <motion.div 
                className="w-4 h-4 bg-green-500 rounded-full"
                animate={{ scale: [1, 1.2, 1], opacity: [1, 0.7, 1] }}
                transition={{ repeat: Infinity, duration: 2 }}
              ></motion.div>
              <p className="text-2xl font-bold text-gray-800">
                <span className="text-green-600">System Online</span>
              </p>
            </div>
            
            <p className="text-center text-gray-700 mb-6 text-lg">
              Backend API running on <span className="font-mono bg-white px-3 py-1 rounded-lg shadow-sm">port 8000</span>
            </p>
            
            <div className="flex flex-wrap justify-center gap-4 mt-6">
              {[
                { icon: '🔌', text: 'Alpha Vantage API' },
                { icon: '📡', text: 'Real-time Data' },
                { icon: '🤖', text: '6-Agent Workflow' },
                { icon: '🚀', text: 'LangGraph Powered' }
              ].map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-md"
                >
                  <span className="text-2xl">{item.icon}</span>
                  <span className="text-sm font-semibold text-gray-700">{item.text}</span>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default Home;
