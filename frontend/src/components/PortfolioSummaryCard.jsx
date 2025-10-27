import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { TrendingUp, Package, PieChartIcon } from 'lucide-react';

const PortfolioSummaryCard = ({ clientId }) => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSummary();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchSummary, 30000);
    return () => clearInterval(interval);
  }, [clientId]);

  const fetchSummary = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/portfolio/${clientId}/summary`);
      const data = await response.json();
      setSummary(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching portfolio summary:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (!summary) return null;

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Package className="w-5 h-5" />
          Portfolio Overview
        </h3>
      </div>
      <div className="p-4 space-y-4">
        {/* Key Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-50 p-3 rounded-lg">
            <div className="text-xs text-gray-600 mb-1">Total Holdings</div>
            <div className="text-2xl font-bold text-blue-600">
              {summary.total_holdings}
            </div>
          </div>

          <div className="bg-green-50 p-3 rounded-lg">
            <div className="text-xs text-gray-600 mb-1">Portfolio Value</div>
            <div className="text-2xl font-bold text-green-600">
              ${(summary.total_value / 1000).toFixed(0)}K
            </div>
          </div>
        </div>

        {/* Asset Allocation Chart */}
        {summary.asset_allocation && summary.asset_allocation.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
              <PieChartIcon className="w-4 h-4" />
              Asset Allocation
            </h4>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={summary.asset_allocation}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={70}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {summary.asset_allocation.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Top Holdings */}
        {summary.top_holdings && summary.top_holdings.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Top Holdings
            </h4>
            <div className="space-y-2">
              {summary.top_holdings.slice(0, 3).map((holding, index) => (
                <div key={index} className="flex justify-between items-center text-sm">
                  <span className="font-medium">{holding.symbol}</span>
                  <span className="text-gray-600">{holding.quantity} shares</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="text-xs text-gray-500 pt-2 border-t">
          Last updated: {new Date(summary.last_updated).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default PortfolioSummaryCard;
