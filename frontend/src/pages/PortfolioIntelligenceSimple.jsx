import React, { useState } from 'react';

function PortfolioIntelligenceSimple() {
  const [selectedClient, setSelectedClient] = useState('CLT-001');

  const clients = Array.from({ length: 10 }, (_, i) => ({
    id: `CLT-${String(i + 1).padStart(3, '0')}`,
    name: `Client ${i + 1}`
  }));

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-4">Portfolio Intelligence (Test)</h1>

      <div className="bg-white rounded-lg shadow p-6">
        <label className="block mb-2">Select Client</label>
        <select
          value={selectedClient}
          onChange={(e) => setSelectedClient(e.target.value)}
          className="w-full px-4 py-2 border rounded"
        >
          {clients.map(client => (
            <option key={client.id} value={client.id}>
              {client.id} - {client.name}
            </option>
          ))}
        </select>

        <div className="mt-4">
          <p>Selected: {selectedClient}</p>
        </div>
      </div>
    </div>
  );
}

export default PortfolioIntelligenceSimple;
