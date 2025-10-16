import { useState } from 'react';
import { useApp } from '../context/AppContext';
import { useQuery } from '../hooks/useQuery';
import { useSession } from '../hooks/useSession';
import { QueryInput } from '../components/query/QueryInput';
import { ResponseDisplay } from '../components/query/ResponseDisplay';
import { ClarificationModal } from '../components/query/ClarificationModal';
import { ConversationHistory } from '../components/session/ConversationHistory';
import { SessionManager } from '../components/session/SessionManager';
import { AgentActivityPanel } from '../components/agent/AgentActivityPanel';

export const Dashboard = () => {
  const { selectedClient } = useApp();
  const {
    loading,
    response,
    error,
    executionTime,
    executeQuery,
    clarifyQuery
  } = useQuery();

  const {
    sessionId,
    conversationHistory,
    updateSession,
    addToHistory,
    clearSession,
    refreshSession
  } = useSession(selectedClient);

  const [showClarificationModal, setShowClarificationModal] = useState(false);
  const [clarificationData, setClarificationData] = useState(null);

  const handleQuerySubmit = async (query) => {
    // Add user message to history
    addToHistory('user', query);

    // Execute query
    const result = await executeQuery(
      query,
      selectedClient,
      sessionId,
      conversationHistory
    );

    if (result.success) {
      const data = result.data;

      // Update session
      if (data.session_id) {
        updateSession(data.session_id, data.conversation_history || []);
      }

      // Handle clarification
      if (result.needsClarification) {
        setClarificationData({
          message: data.clarification_message,
          originalQuery: query,
          sessionId: data.session_id
        });
        setShowClarificationModal(true);
      } else {
        // Add assistant response to history
        addToHistory('assistant', data.response || data.message, {
          agentState: data.agent_state,
          executionTime
        });
      }
    }
  };

  const handleClarificationSubmit = async (clarification) => {
    if (!clarificationData) return;

    const result = await clarifyQuery(
      clarificationData.sessionId,
      clarification,
      clarificationData.originalQuery
    );

    if (result.success) {
      const data = result.data;

      // Update session
      if (data.session_id) {
        updateSession(data.session_id, data.conversation_history || []);
      }

      // Add clarification and response to history
      addToHistory('user', clarification);
      addToHistory('assistant', data.response || data.message, {
        agentState: data.agent_state,
        executionTime
      });

      // Close modal
      setShowClarificationModal(false);
      setClarificationData(null);
    }
  };

  const handleClearHistory = () => {
    clearSession();
  };

  return (
    <div className="space-y-6">
      {/* Session Manager */}
      {sessionId && (
        <SessionManager
          sessionId={sessionId}
          conversationHistory={conversationHistory}
          onClear={clearSession}
          onRefresh={refreshSession}
          loading={loading}
        />
      )}

      {/* Query Input */}
      <QueryInput
        onSubmit={handleQuerySubmit}
        loading={loading}
        disabled={loading}
      />

      {/* Response Display */}
      <ResponseDisplay
        response={response}
        loading={loading}
        error={error}
        executionTime={executionTime}
        agentState={response?.agent_state}
      />

      {/* Agent Activity Panel */}
      {response?.agent_state && (
        <AgentActivityPanel
          agentState={response.agent_state}
          executionTime={executionTime}
        />
      )}

      {/* Conversation History */}
      {conversationHistory.length > 0 && (
        <ConversationHistory
          messages={conversationHistory}
          onClear={handleClearHistory}
          loading={loading}
        />
      )}

      {/* Clarification Modal */}
      <ClarificationModal
        isOpen={showClarificationModal}
        onClose={() => {
          setShowClarificationModal(false);
          setClarificationData(null);
        }}
        onSubmit={handleClarificationSubmit}
        message={clarificationData?.message}
        originalQuery={clarificationData?.originalQuery}
        loading={loading}
      />
    </div>
  );
};

export default Dashboard;
