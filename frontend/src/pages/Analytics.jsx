import { useApp } from '../context/AppContext';
import { usePortfolio } from '../hooks/usePortfolio';
import { Card } from '../components/common/Card';
import { PerformanceChart } from '../components/portfolio/PerformanceChart';
import { AssetAllocation } from '../components/portfolio/AssetAllocation';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { TrendingUp, TrendingDown, Activity, DollarSign } from 'lucide-react';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import clsx from 'clsx';

export const Analytics = () => {
  const { selectedClient } = useApp();
  const { portfolio, metrics, loading } = usePortfolio(selectedClient);

  if (loading && !portfolio) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  const holdings = portfolio?.holdings || [];

  // Calculate additional metrics
  const topGainer = holdings.reduce((max, holding) =>
    (holding.unrealized_gain_loss || 0) > (max.unrealized_gain_loss || 0) ? holding : max
  , holdings[0] || {});

  const topLoser = holdings.reduce((min, holding) =>
    (holding.unrealized_gain_loss || 0) < (min.unrealized_gain_loss || 0) ? holding : min
  , holdings[0] || {});

  const avgGainPercent = holdings.length > 0
    ? holdings.reduce((sum, h) => sum + (h.unrealized_gain_loss_percent || 0), 0) / holdings.length
    : 0;

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Portfolio Analytics
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Detailed performance analysis for {selectedClient}
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                Total Return
              </p>
              <p
                className={clsx(
                  'text-2xl font-bold',
                  metrics.totalGain >= 0
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                )}
              >
                {formatCurrency(metrics.totalGain)}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {formatPercentage(metrics.totalGainPercent)}
              </p>
            </div>
            <div
              className={clsx(
                'p-3 rounded-lg',
                metrics.totalGain >= 0
                  ? 'bg-green-100 dark:bg-green-900/30'
                  : 'bg-red-100 dark:bg-red-900/30'
              )}
            >
              <DollarSign
                className={clsx(
                  'w-6 h-6',
                  metrics.totalGain >= 0
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                )}
              />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                Avg Return %
              </p>
              <p
                className={clsx(
                  'text-2xl font-bold',
                  avgGainPercent >= 0
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                )}
              >
                {formatPercentage(avgGainPercent)}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Across {metrics.totalHoldings} holdings
              </p>
            </div>
            <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <Activity className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                Top Gainer
              </p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">
                {topGainer?.symbol || 'N/A'}
              </p>
              <p className="text-sm text-green-600 dark:text-green-400 mt-1">
                {formatCurrency(topGainer?.unrealized_gain_loss)}
              </p>
            </div>
            <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <TrendingUp className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                Top Loser
              </p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">
                {topLoser?.symbol || 'N/A'}
              </p>
              <p className="text-sm text-red-600 dark:text-red-400 mt-1">
                {formatCurrency(topLoser?.unrealized_gain_loss)}
              </p>
            </div>
            <div className="p-3 bg-red-100 dark:bg-red-900/30 rounded-lg">
              <TrendingDown className="w-6 h-6 text-red-600 dark:text-red-400" />
            </div>
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PerformanceChart holdings={holdings} />
        <AssetAllocation holdings={holdings} />
      </div>

      {/* Holdings Performance Table */}
      <Card title="Holdings Performance" subtitle="Detailed breakdown">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 dark:bg-gray-700/50">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-gray-900 dark:text-white">
                  Symbol
                </th>
                <th className="px-4 py-3 text-right font-semibold text-gray-900 dark:text-white">
                  Value
                </th>
                <th className="px-4 py-3 text-right font-semibold text-gray-900 dark:text-white">
                  Cost Basis
                </th>
                <th className="px-4 py-3 text-right font-semibold text-gray-900 dark:text-white">
                  Gain/Loss
                </th>
                <th className="px-4 py-3 text-right font-semibold text-gray-900 dark:text-white">
                  Return %
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {holdings.map((holding) => {
                const isGain = (holding.unrealized_gain_loss || 0) >= 0;
                return (
                  <tr
                    key={holding.symbol}
                    className="hover:bg-gray-50 dark:hover:bg-gray-700/30"
                  >
                    <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">
                      {holding.symbol}
                    </td>
                    <td className="px-4 py-3 text-right text-gray-900 dark:text-white">
                      {formatCurrency(holding.current_value)}
                    </td>
                    <td className="px-4 py-3 text-right text-gray-600 dark:text-gray-400">
                      {formatCurrency(holding.cost_basis)}
                    </td>
                    <td
                      className={clsx(
                        'px-4 py-3 text-right font-medium',
                        isGain
                          ? 'text-green-600 dark:text-green-400'
                          : 'text-red-600 dark:text-red-400'
                      )}
                    >
                      {formatCurrency(holding.unrealized_gain_loss)}
                    </td>
                    <td
                      className={clsx(
                        'px-4 py-3 text-right font-medium',
                        isGain
                          ? 'text-green-600 dark:text-green-400'
                          : 'text-red-600 dark:text-red-400'
                      )}
                    >
                      {formatPercentage(holding.unrealized_gain_loss_percent)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default Analytics;
