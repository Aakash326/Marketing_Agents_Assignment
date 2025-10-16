import { TrendingUp, TrendingDown } from 'lucide-react';
import { formatCurrency, formatPercentage } from '../../utils/formatters';
import { Card } from '../common/Card';
import clsx from 'clsx';

export const HoldingCard = ({ holding }) => {
  const {
    symbol,
    company_name,
    quantity,
    current_price,
    current_value,
    cost_basis,
    unrealized_gain_loss,
    unrealized_gain_loss_percent
  } = holding;

  const isGain = unrealized_gain_loss > 0;

  return (
    <Card hover className="cursor-pointer">
      <div className="flex items-start justify-between">
        {/* Left Section */}
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">
              {symbol}
            </h3>
            {isGain ? (
              <TrendingUp className="w-5 h-5 text-green-500" />
            ) : (
              <TrendingDown className="w-5 h-5 text-red-500" />
            )}
          </div>

          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            {company_name || 'N/A'}
          </p>

          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <p className="text-gray-500 dark:text-gray-400">Quantity</p>
              <p className="font-semibold text-gray-900 dark:text-white">
                {quantity?.toFixed(2) || 'N/A'}
              </p>
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400">Price</p>
              <p className="font-semibold text-gray-900 dark:text-white">
                {formatCurrency(current_price)}
              </p>
            </div>
          </div>
        </div>

        {/* Right Section */}
        <div className="text-right">
          <p className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
            {formatCurrency(current_value)}
          </p>

          <div
            className={clsx(
              'inline-flex items-center gap-1 px-2 py-1 rounded-full text-sm font-medium',
              isGain
                ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
                : 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
            )}
          >
            <span>{formatCurrency(unrealized_gain_loss)}</span>
            <span>({formatPercentage(unrealized_gain_loss_percent)})</span>
          </div>

          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Cost: {formatCurrency(cost_basis)}
          </p>
        </div>
      </div>
    </Card>
  );
};
