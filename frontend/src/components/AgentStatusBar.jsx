import React from 'react';

const AgentStatusBar = ({ agentStatuses = {} }) => {
  const agents = [
    { id: 'planner', name: 'Planner', icon: '🎯', description: 'Query Analysis' },
    { id: 'portfolio', name: 'Portfolio', icon: '💼', description: 'Holdings Data' },
    { id: 'market', name: 'Market', icon: '📈', description: 'Live Prices' },
    { id: 'collaboration', name: 'Synthesis', icon: '🤝', description: 'Data Fusion' },
    { id: 'validator', name: 'Validator', icon: '✅', description: 'Accuracy Check' }
  ];

  const getStatusColor = (status) => {
    switch(status) {
      case 'idle': return 'bg-gray-100 border-gray-300';
      case 'working': return 'bg-blue-100 border-blue-400 animate-pulse';
      case 'complete': return 'bg-green-100 border-green-400';
      case 'error': return 'bg-red-100 border-red-400';
      default: return 'bg-gray-100 border-gray-300';
    }
  };

  const getStatusIcon = (status) => {
    switch(status) {
      case 'working': return '⚡';
      case 'complete': return '✓';
      case 'error': return '✗';
      default: return '○';
    }
  };

  return (
    <div className="mb-6">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">AI Agent Status</h3>
      <div className="grid grid-cols-5 gap-3">
        {agents.map(agent => {
          const status = agentStatuses[agent.id] || 'idle';
          return (
            <div
              key={agent.id}
              className={`p-4 border-2 rounded-lg transition-all duration-300 ${getStatusColor(status)}`}
            >
              <div className="text-center">
                <div className="text-3xl mb-2">
                  {agent.icon}
                </div>
                <div className="text-sm font-semibold text-gray-800">
                  {agent.name}
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {agent.description}
                </div>
                <div className="mt-2 text-lg">
                  {getStatusIcon(status)}
                </div>
                <div className="text-xs text-gray-500 capitalize mt-1">
                  {status}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AgentStatusBar;
