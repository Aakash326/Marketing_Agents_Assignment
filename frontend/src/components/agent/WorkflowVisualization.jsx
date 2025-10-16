import { ArrowRight, Info } from 'lucide-react';
import { AGENT_NAMES, AGENT_DESCRIPTIONS } from '../../utils/constants';
import clsx from 'clsx';
import { useState } from 'react';

const AgentNode = ({ name, active, status = 'idle', onClick }) => {
  const getStatusColor = () => {
    if (status === 'completed') return 'bg-green-500';
    if (status === 'active') return 'bg-yellow-500 animate-pulse';
    if (active) return 'bg-primary-500';
    return 'bg-gray-300 dark:bg-gray-600';
  };

  return (
    <div
      className="flex flex-col items-center gap-2 cursor-pointer group"
      onClick={onClick}
    >
      <div
        className={clsx(
          'w-12 h-12 rounded-full flex items-center justify-center',
          'transition-all duration-300',
          'border-4 border-white dark:border-gray-800',
          'shadow-lg group-hover:shadow-xl group-hover:scale-110',
          getStatusColor()
        )}
      >
        <span className="text-white font-bold text-sm">
          {name.charAt(0)}
        </span>
      </div>
      <span className="text-xs font-medium text-gray-700 dark:text-gray-300 text-center">
        {name}
      </span>
    </div>
  );
};

const Arrow = ({ active = false }) => {
  return (
    <ArrowRight
      className={clsx(
        'w-6 h-6 transition-all duration-300',
        active
          ? 'text-primary-500 dark:text-primary-400'
          : 'text-gray-300 dark:text-gray-600'
      )}
    />
  );
};

export const WorkflowVisualization = ({ agentState = {} }) => {
  const [selectedAgent, setSelectedAgent] = useState(null);

  const agents = [
    { name: AGENT_NAMES.PLANNER, key: 'planner_used' },
    { name: AGENT_NAMES.PORTFOLIO, key: 'portfolio_used' },
    { name: AGENT_NAMES.MARKET, key: 'market_used' },
    { name: AGENT_NAMES.COLLABORATION, key: 'collaboration_used' },
    { name: AGENT_NAMES.VALIDATOR, key: 'validator_used' }
  ];

  const getAgentStatus = (key) => {
    if (!agentState[key]) return 'idle';
    // You can extend this to track active/completed states
    return 'completed';
  };

  return (
    <div className="space-y-6">
      {/* Workflow Diagram */}
      <div className="relative bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-lg p-8 overflow-x-auto">
        <div className="flex items-center justify-between min-w-max gap-4">
          {agents.map((agent, index) => (
            <div key={agent.name} className="flex items-center gap-4">
              <AgentNode
                name={agent.name}
                active={agentState[agent.key]}
                status={getAgentStatus(agent.key)}
                onClick={() => setSelectedAgent(agent.name)}
              />
              {index < agents.length - 1 && (
                <Arrow active={agentState[agent.key]} />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap items-center justify-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded-full" />
          <span className="text-gray-700 dark:text-gray-300">Completed</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-yellow-500 rounded-full animate-pulse" />
          <span className="text-gray-700 dark:text-gray-300">Processing</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-primary-500 rounded-full" />
          <span className="text-gray-700 dark:text-gray-300">Active</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-gray-300 dark:bg-gray-600 rounded-full" />
          <span className="text-gray-700 dark:text-gray-300">Inactive</span>
        </div>
      </div>

      {/* Agent Description */}
      {selectedAgent && (
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800 animate-fade-in">
          <div className="flex items-start gap-3">
            <Info className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-blue-900 dark:text-blue-200 mb-1">
                {selectedAgent}
              </h4>
              <p className="text-sm text-blue-800 dark:text-blue-300">
                {AGENT_DESCRIPTIONS[selectedAgent]}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
