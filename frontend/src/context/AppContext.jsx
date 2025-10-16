import { createContext, useContext, useState, useCallback } from 'react';
import { CLIENTS } from '../utils/constants';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [selectedClient, setSelectedClient] = useState(() => {
    const savedClient = localStorage.getItem('selectedClient');
    return savedClient || CLIENTS[0].id;
  });

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showShortcuts, setShowShortcuts] = useState(false);

  const selectClient = useCallback((clientId) => {
    setSelectedClient(clientId);
    localStorage.setItem('selectedClient', clientId);
  }, []);

  const toggleSidebar = useCallback(() => {
    setSidebarOpen(prev => !prev);
  }, []);

  const toggleShortcuts = useCallback(() => {
    setShowShortcuts(prev => !prev);
  }, []);

  const getClientInfo = useCallback((clientId) => {
    return CLIENTS.find(client => client.id === clientId) || CLIENTS[0];
  }, []);

  const value = {
    selectedClient,
    selectClient,
    getClientInfo,
    sidebarOpen,
    setSidebarOpen,
    toggleSidebar,
    showShortcuts,
    setShowShortcuts,
    toggleShortcuts,
    clients: CLIENTS
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};
