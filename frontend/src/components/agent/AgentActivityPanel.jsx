import { Activity } from 'lucide-react';
import { Card } from '../common/Card';
import { AgentStatusBadge } from './AgentStatusBadge';
import { WorkflowVisualization } from './WorkflowVisualization';
import { AGENT_NAMES } from '../../utils/constants';

export const AgentActivityPanel = ({ agentState = {}, executionTime = null }) => {
  const agents = [
    { name: AGENT_NAMES.PLANNER, key: 'planner_used' },
    { name: AGENT_NAMES.PORTFOLIO, key: 'portfolio_used' },
    { name: AGENT_NAMES.MARKET, key: 'market_used' },
    { name: AGENT_NAMES.SEC, key: 'sec_used' },
    { name: AGENT_NAMES.COLLABORATION, key: 'collaboration_used' },
    { name: AGENT_NAMES.VALIDATOR, key: 'validator_used' }
  ];

  const activeAgentsCount = agents.filter(agent => agentState[agent.key]).length;

  return (
    <Card
      title="Agent Activity"
      subtitle={`${activeAgentsCount} agent${activeAgentsCount !== 1 ? 's' : ''} involved`}
      headerAction={
        <div className="flex items-center gap-2 text-primary-600 dark:text-primary-400">
          <Activity className="w-4 h-4" />
          <span className="text-sm font-medium">Live</span>
        </div>
      }
    >
      <div className="space-y-6">
        {/* Agent Badges */}
        <div className="flex flex-wrap gap-2">
          {agents.map((agent) => (
            <AgentStatusBadge
              key={agent.name}
              name={agent.name}
              active={agentState[agent.key]}
              status={agentState[agent.key] ? 'completed' : 'idle'}
            />
          ))}
        </div>

        {/* Workflow Visualization */}
        <WorkflowVisualization agentState={agentState} />

        {/* Summary */}
        <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {activeAgentsCount}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Agents Active
              </p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {executionTime ? `${(executionTime / 1000).toFixed(2)}s` : 'N/A'}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Execution Time
              </p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};
