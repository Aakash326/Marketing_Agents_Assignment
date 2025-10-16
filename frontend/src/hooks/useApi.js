import { useState, useCallback } from 'react';
import toast from 'react-hot-toast';

/**
 * Generic hook for API calls with loading and error states
 */
export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (apiFunction, options = {}) => {
    const {
      onSuccess,
      onError,
      showSuccessToast = false,
      showErrorToast = true,
      successMessage = 'Operation completed successfully',
    } = options;

    setLoading(true);
    setError(null);

    try {
      const result = await apiFunction();

      if (onSuccess) {
        onSuccess(result);
      }

      if (showSuccessToast) {
        toast.success(successMessage);
      }

      return { success: true, data: result };
    } catch (err) {
      const errorMessage = err.message || 'An error occurred';
      setError(errorMessage);

      if (onError) {
        onError(errorMessage);
      }

      if (showErrorToast) {
        toast.error(errorMessage);
      }

      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
  }, []);

  return {
    loading,
    error,
    execute,
    reset
  };
};
