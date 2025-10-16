import { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { Footer } from './Footer';
import { useSession } from '../../hooks/useSession';
import { useApp } from '../../context/AppContext';
import toast from 'react-hot-toast';

export const Layout = ({ children }) => {
  const { selectedClient } = useApp();
  const { clearSession } = useSession(selectedClient);
  const [isClearing, setIsClearing] = useState(false);

  const handleClearSession = async () => {
    if (!confirm('Are you sure you want to clear the current session? This will delete all conversation history.')) {
      return;
    }

    setIsClearing(true);
    try {
      await clearSession();
      toast.success('Session cleared successfully');
    } catch (error) {
      toast.error('Failed to clear session');
    } finally {
      setIsClearing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      <Header />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar onClearSession={handleClearSession} />

        <main className="flex-1 overflow-y-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            {children}
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
};

export default Layout;
