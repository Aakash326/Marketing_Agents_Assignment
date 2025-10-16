import { useApp } from '../context/AppContext';
import { usePortfolio } from '../hooks/usePortfolio';
import { PortfolioOverview } from '../components/portfolio/PortfolioOverview';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { Card } from '../components/common/Card';
import { AlertTriangle, RefreshCcw } from 'lucide-react';
import { Button } from '../components/common/Button';

export const Portfolio = () => {
  const { selectedClient } = useApp();
  const {
    portfolio,
    metrics,
    loading,
    error,
    lastUpdated,
    refresh
  } = usePortfolio(selectedClient);

  if (loading && !portfolio) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error && !portfolio) {
    return (
      <Card>
        <div className="flex flex-col items-center justify-center py-12">
          <AlertTriangle className="w-12 h-12 text-red-500 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Failed to Load Portfolio
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4 text-center">
            {error}
          </p>
          <Button onClick={refresh} variant="primary">
            <RefreshCcw className="w-4 h-4" />
            Try Again
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Portfolio Dashboard
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Client: {selectedClient}
            {lastUpdated && (
              <span className="ml-2">
                • Last updated: {lastUpdated.toLocaleTimeString()}
              </span>
            )}
          </p>
        </div>
      </div>

      {/* Portfolio Overview */}
      <PortfolioOverview
        portfolio={portfolio}
        metrics={metrics}
        loading={loading}
        onRefresh={refresh}
      />
    </div>
  );
};

export default Portfolio;
