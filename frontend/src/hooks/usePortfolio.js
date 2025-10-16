import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';
import toast from 'react-hot-toast';

export const usePortfolio = (clientId) => {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchPortfolio = useCallback(async (showToast = false) => {
    if (!clientId) return;

    setLoading(true);
    setError(null);

    try {
      const data = await apiService.getPortfolio(clientId);
      setPortfolio(data);
      setLastUpdated(new Date());

      if (showToast) {
        toast.success('Portfolio data refreshed');
      }

      return { success: true, data };
    } catch (err) {
      const errorMessage = err.message || 'Failed to fetch portfolio';
      setError(errorMessage);

      if (showToast) {
        toast.error(errorMessage);
      }

      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, [clientId]);

  // Auto-fetch on mount or when clientId changes
  useEffect(() => {
    fetchPortfolio();
  }, [fetchPortfolio]);

  // Auto-refresh every 5 minutes
  useEffect(() => {
    const interval = setInterval(() => {
      fetchPortfolio(false); // Silent refresh
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(interval);
  }, [fetchPortfolio]);

  const refresh = useCallback(() => {
    return fetchPortfolio(true);
  }, [fetchPortfolio]);

  // Calculate portfolio metrics
  const metrics = {
    totalHoldings: portfolio?.holdings?.length || 0,
    totalValue: portfolio?.holdings?.reduce((sum, h) => sum + (h.current_value || 0), 0) || 0,
    totalGain: portfolio?.holdings?.reduce((sum, h) => {
      const gain = (h.current_value || 0) - (h.cost_basis || 0);
      return sum + gain;
    }, 0) || 0,
    get totalGainPercent() {
      const totalCost = portfolio?.holdings?.reduce((sum, h) => sum + (h.cost_basis || 0), 0) || 0;
      return totalCost > 0 ? (this.totalGain / totalCost) * 100 : 0;
    }
  };

  return {
    portfolio,
    metrics,
    loading,
    error,
    lastUpdated,
    refresh,
    fetchPortfolio
  };
};
