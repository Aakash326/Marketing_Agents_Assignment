import React, { useState, useEffect } from 'react';
import AgentStatusBar from '../components/AgentStatusBar';
import PortfolioSummaryCard from '../components/PortfolioSummaryCard';
import ChatMessages from '../components/ChatMessages';
import ChatInput from '../components/ChatInput';
import QuerySuggestions from '../components/QuerySuggestions';
import { Activity } from 'lucide-react';

const ChatPage = () => {
  const [selectedClient, setSelectedClient] = useState('CLT-001');
  const [messages, setMessages] = useState([]);
  const [agentStatuses, setAgentStatuses] = useState({});
  const [sessionId, setSessionId] = useState(null);
  const [ws, setWs] = useState(null);

  // Initialize session
  useEffect(() => {
    initializeSession();
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [selectedClient]);

  const initializeSession = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: selectedClient })
      });
      const data = await response.json();
      setSessionId(data.session_id);

      // Connect WebSocket for real-time updates
      connectWebSocket(data.session_id);
    } catch (error) {
      console.error('Error initializing session:', error);
    }
  };

  const connectWebSocket = (sessionId) => {
    const websocket = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);

    websocket.onopen = () => {
      console.log('WebSocket connected');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'agent_status') {
        setAgentStatuses(prev => ({
          ...prev,
          [data.agent]: data.status
        }));
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket closed');
    };

    setWs(websocket);
  };

  const handleQuery = async (query) => {
    // Add user message immediately
    setMessages(prev => [...prev, { role: 'user', content: query }]);

    // Reset agent statuses
    setAgentStatuses({
      planner: 'working',
      portfolio: 'idle',
      market: 'idle',
      collaboration: 'idle',
      validator: 'idle'
    });

    try {
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: selectedClient,
          query: query
        })
      });

      const result = await response.json();

      // Add assistant message
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: result.answer,
        visualizationData: result.visualization_data
      }]);

      // Update final agent statuses
      setAgentStatuses({
        planner: 'complete',
        portfolio: result.agents_used?.includes('portfolio_agent') ? 'complete' : 'idle',
        market: result.agents_used?.includes('market_agent') ? 'complete' : 'idle',
        collaboration: result.agents_used?.includes('collaboration_agent') ? 'complete' : 'idle',
        validator: 'complete'
      });

    } catch (error) {
      console.error('Error processing query:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, an error occurred while processing your query.'
      }]);
    }
  };

  const clients = ['CLT-001', 'CLT-002', 'CLT-003', 'CLT-004', 'CLT-005',
                   'CLT-007', 'CLT-009', 'CLT-010'];

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm p-4">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">
            📊 Portfolio Intelligence
          </h1>
          <select
            value={selectedClient}
            onChange={(e) => setSelectedClient(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {clients.map(client => (
              <option key={client} value={client}>{client}</option>
            ))}
          </select>
        </div>
      </header>

      {/* Main Content - Split Panel */}
      <div className="flex-1 grid grid-cols-3 gap-6 p-6 overflow-hidden">

        {/* LEFT: Chat Area (2/3 width) */}
        <div className="col-span-2 flex flex-col space-y-4">
          <AgentStatusBar agentStatuses={agentStatuses} />

          <QuerySuggestions
            clientId={selectedClient}
            onSelect={handleQuery}
          />

          <div className="flex-1 overflow-hidden">
            <ChatMessages messages={messages} />
          </div>

          <ChatInput onSubmit={handleQuery} />
        </div>

        {/* RIGHT: Context Panel (1/3 width) */}
        <div className="col-span-1 overflow-y-auto space-y-4">
          <PortfolioSummaryCard clientId={selectedClient} />

          {/* Recent Activity Card */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-4 border-b">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <Activity className="w-5 h-5" />
                Recent Activity
              </h3>
            </div>
            <div className="p-4">
              <div className="text-sm text-gray-600">
                {messages.length} messages in this session
              </div>
              {sessionId && (
                <div className="text-xs text-gray-500 mt-2">
                  Session ID: {sessionId.substring(0, 8)}...
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
