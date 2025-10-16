import { useState } from 'react';
import { RefreshCcw, Download, TrendingUp, Briefcase, DollarSign } from 'lucide-react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { HoldingCard } from './HoldingCard';
import { AssetAllocation } from './AssetAllocation';
import { PerformanceChart } from './PerformanceChart';
import { formatCurrency, formatPercentage } from '../../utils/formatters';
import clsx from 'clsx';

export const PortfolioOverview = ({
  portfolio,
  metrics,
  loading = false,
  onRefresh
}) => {
  const [sortBy, setSortBy] = useState('value'); // value, gain, symbol

  if (!portfolio || !portfolio.holdings) {
    return (
      <Card>
        <div className="text-center py-12">
          <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">
            {loading ? 'Loading portfolio...' : 'No portfolio data available'}
          </p>
        </div>
      </Card>
    );
  }

  const holdings = portfolio.holdings || [];

  // Sort holdings
  const sortedHoldings = [...holdings].sort((a, b) => {
    switch (sortBy) {
      case 'value':
        return (b.current_value || 0) - (a.current_value || 0);
      case 'gain':
        return (b.unrealized_gain_loss || 0) - (a.unrealized_gain_loss || 0);
      case 'symbol':
        return (a.symbol || '').localeCompare(b.symbol || '');
      default:
        return 0;
    }
  });

  const totalGainIsPositive = metrics.totalGain >= 0;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                Total Holdings
              </p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {metrics.totalHoldings}
              </p>
            </div>
            <div className="p-3 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
              <Briefcase className="w-6 h-6 text-primary-600 dark:text-primary-400" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                Total Value
              </p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {formatCurrency(metrics.totalValue)}
              </p>
            </div>
            <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <DollarSign className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                Total Gain/Loss
              </p>
              <p
                className={clsx(
                  'text-3xl font-bold',
                  totalGainIsPositive
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                )}
              >
                {formatCurrency(metrics.totalGain)}
              </p>
              <p
                className={clsx(
                  'text-sm font-medium mt-1',
                  totalGainIsPositive
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                )}
              >
                {formatPercentage(metrics.totalGainPercent)}
              </p>
            </div>
            <div
              className={clsx(
                'p-3 rounded-lg',
                totalGainIsPositive
                  ? 'bg-green-100 dark:bg-green-900/30'
                  : 'bg-red-100 dark:bg-red-900/30'
              )}
            >
              <TrendingUp
                className={clsx(
                  'w-6 h-6',
                  totalGainIsPositive
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                )}
              />
            </div>
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AssetAllocation holdings={holdings} />
        <PerformanceChart holdings={holdings} />
      </div>

      {/* Holdings List */}
      <Card
        title="Holdings"
        subtitle={`${holdings.length} position${holdings.length !== 1 ? 's' : ''}`}
        headerAction={
          <div className="flex items-center gap-2">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-1 text-sm bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="value">Sort by Value</option>
              <option value="gain">Sort by Gain/Loss</option>
              <option value="symbol">Sort by Symbol</option>
            </select>

            <Button
              variant="ghost"
              size="sm"
              onClick={onRefresh}
              loading={loading}
              title="Refresh portfolio"
            >
              <RefreshCcw className="w-4 h-4" />
            </Button>
          </div>
        }
      >
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {sortedHoldings.map((holding) => (
            <HoldingCard key={holding.symbol} holding={holding} />
          ))}
        </div>
      </Card>
    </div>
  );
};
