import { useState, useCallback } from 'react';
import { apiService } from '../services/api';
import toast from 'react-hot-toast';
import { validateQuery } from '../utils/validators';

export const useQuery = () => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [executionTime, setExecutionTime] = useState(null);

  const executeQuery = useCallback(async (query, clientId, sessionId = null, conversationHistory = []) => {
    // Validate query
    const validation = validateQuery(query);
    if (!validation.valid) {
      toast.error(validation.error);
      return { success: false, error: validation.error };
    }

    setLoading(true);
    setError(null);
    const startTime = Date.now();

    try {
      const result = await apiService.query({
        query,
        client_id: clientId,
        session_id: sessionId,
        conversation_history: conversationHistory
      });

      const endTime = Date.now();
      const execTime = endTime - startTime;
      setExecutionTime(execTime);
      setResponse(result);

      // Handle clarification
      if (result.needs_clarification) {
        return {
          success: true,
          needsClarification: true,
          data: result
        };
      }

      toast.success('Query completed successfully');
      return {
        success: true,
        needsClarification: false,
        data: result
      };

    } catch (err) {
      // Better error message extraction
      let errorMessage = 'Failed to execute query';
      
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err && typeof err === 'object') {
        // Try to extract message from object
        errorMessage = err.message || err.error || err.detail || JSON.stringify(err);
      }
      
      console.error('Query execution error:', err);
      setError(errorMessage);
      toast.error(errorMessage);
      return {
        success: false,
        error: errorMessage
      };
    } finally {
      setLoading(false);
    }
  }, []);

  const clarifyQuery = useCallback(async (sessionId, clarification, originalQuery) => {
    setLoading(true);
    setError(null);
    const startTime = Date.now();

    try {
      const result = await apiService.clarify({
        session_id: sessionId,
        clarification,
        original_query: originalQuery
      });

      const endTime = Date.now();
      const execTime = endTime - startTime;
      setExecutionTime(execTime);
      setResponse(result);

      toast.success('Clarification processed successfully');
      return {
        success: true,
        data: result
      };

    } catch (err) {
      // Better error message extraction
      let errorMessage = 'Failed to process clarification';
      
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err && typeof err === 'object') {
        // Try to extract message from object
        errorMessage = err.message || err.error || err.detail || JSON.stringify(err);
      }
      
      console.error('Clarification error:', err);
      setError(errorMessage);
      toast.error(errorMessage);
      return {
        success: false,
        error: errorMessage
      };
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setLoading(false);
    setResponse(null);
    setError(null);
    setExecutionTime(null);
  }, []);

  return {
    loading,
    response,
    error,
    executionTime,
    executeQuery,
    clarifyQuery,
    reset
  };
};
