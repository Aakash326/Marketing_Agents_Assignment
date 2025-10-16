import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';
import { storageService } from '../services/storage';

export const useSession = (clientId) => {
  const [sessionId, setSessionId] = useState(null);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load session from localStorage on mount
  useEffect(() => {
    if (!clientId) return;

    const savedSessionId = storageService.getSession(clientId);
    if (savedSessionId) {
      setSessionId(savedSessionId);
      loadSessionData(savedSessionId);
    }
  }, [clientId]);

  const loadSessionData = async (sid) => {
    setLoading(true);
    try {
      const session = await apiService.getSession(sid);
      if (session && session.conversation_history) {
        setConversationHistory(session.conversation_history);
        storageService.setConversation(sid, session.conversation_history);
      }
    } catch (err) {
      console.error('Failed to load session:', err);
      // If session doesn't exist on server, clear local storage
      storageService.removeSession(clientId);
      setSessionId(null);
    } finally {
      setLoading(false);
    }
  };

  const updateSession = useCallback((newSessionId, history = []) => {
    setSessionId(newSessionId);
    setConversationHistory(history);

    if (clientId) {
      storageService.setSession(clientId, newSessionId);
      storageService.setConversation(newSessionId, history);
    }
  }, [clientId]);

  const addToHistory = useCallback((role, content, metadata = {}) => {
    const message = {
      role,
      content,
      timestamp: new Date().toISOString(),
      ...metadata
    };

    setConversationHistory(prev => {
      const updated = [...prev, message];
      if (sessionId) {
        storageService.setConversation(sessionId, updated);
      }
      return updated;
    });
  }, [sessionId]);

  const clearSession = useCallback(async () => {
    if (sessionId) {
      try {
        await apiService.deleteSession(sessionId);
      } catch (err) {
        console.error('Failed to delete session on server:', err);
      }
    }

    setSessionId(null);
    setConversationHistory([]);

    if (clientId) {
      storageService.clearClientData(clientId);
    }
  }, [sessionId, clientId]);

  const refreshSession = useCallback(async () => {
    if (sessionId) {
      await loadSessionData(sessionId);
    }
  }, [sessionId]);

  return {
    sessionId,
    conversationHistory,
    loading,
    updateSession,
    addToHistory,
    clearSession,
    refreshSession
  };
};
