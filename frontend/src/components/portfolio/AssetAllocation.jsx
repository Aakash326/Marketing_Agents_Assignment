import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Card } from '../common/Card';

const COLORS = [
  '#3b82f6', // blue
  '#10b981', // green
  '#f59e0b', // yellow
  '#ef4444', // red
  '#8b5cf6', // purple
  '#ec4899', // pink
  '#14b8a6', // teal
  '#f97316', // orange
];

export const AssetAllocation = ({ holdings = [] }) => {
  // Prepare data for pie chart
  const data = holdings.map((holding, index) => ({
    name: holding.symbol,
    value: holding.current_value || 0,
    color: COLORS[index % COLORS.length]
  }));

  const totalValue = data.reduce((sum, item) => sum + item.value, 0);

  // Calculate percentages
  const dataWithPercentages = data.map(item => ({
    ...item,
    percentage: totalValue > 0 ? ((item.value / totalValue) * 100).toFixed(1) : 0
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="font-semibold text-gray-900 dark:text-white mb-1">
            {data.name}
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            ${data.value.toLocaleString()}
          </p>
          <p className="text-sm font-medium text-primary-600 dark:text-primary-400">
            {data.percentage}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card title="Asset Allocation" subtitle="Portfolio distribution by holding">
      {data.length === 0 ? (
        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
          No holdings data available
        </div>
      ) : (
        <div className="space-y-4">
          {/* Pie Chart */}
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={dataWithPercentages}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name} (${percentage}%)`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {dataWithPercentages.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>

          {/* Legend List */}
          <div className="space-y-2">
            {dataWithPercentages.map((item) => (
              <div
                key={item.name}
                className="flex items-center justify-between text-sm"
              >
                <div className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="font-medium text-gray-900 dark:text-white">
                    {item.name}
                  </span>
                </div>
                <span className="text-gray-600 dark:text-gray-400">
                  {item.percentage}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
};
