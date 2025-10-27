import React from 'react';
import {
  BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const DataVisualization = ({ data }) => {
  if (!data) return null;

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <div className="grid grid-cols-2 gap-4 my-4">
      {/* Holdings Bar Chart */}
      {data.holdings && data.holdings.length > 0 && (
        <div className="bg-white rounded-lg shadow p-4">
          <h4 className="text-base font-semibold mb-3">Holdings Distribution</h4>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={data.holdings}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="symbol" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="quantity" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Asset Allocation Pie Chart */}
      {data.allocation && Object.keys(data.allocation).length > 0 && (
        <div className="bg-white rounded-lg shadow p-4">
          <h4 className="text-base font-semibold mb-3">Asset Allocation</h4>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={Object.entries(data.allocation).map(([name, value]) => ({
                  name,
                  value
                }))}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name} ${(percent * 100).toFixed(0)}%`
                }
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {Object.keys(data.allocation).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Performance Chart (if available) */}
      {data.performance && data.performance.length > 0 && (
        <div className="col-span-2 bg-white rounded-lg shadow p-4">
          <h4 className="text-base font-semibold mb-3">Performance Comparison</h4>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={data.performance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="symbol" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="return_pct" fill="#10b981" name="Return %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default DataVisualization;
