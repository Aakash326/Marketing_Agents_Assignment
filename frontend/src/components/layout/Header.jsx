import { Menu, Moon, Sun, Search, User, Settings } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useApp } from '../../context/AppContext';
import { Button } from '../common/Button';
import clsx from 'clsx';

export const Header = () => {
  const { theme, toggleTheme } = useTheme();
  const { toggleSidebar, sidebarOpen, selectedClient, selectClient, clients } = useApp();

  return (
    <header className="sticky top-0 z-50 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
      <div className="flex items-center justify-between h-16 px-4 md:px-6">
        {/* Left Section */}
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleSidebar}
            className="lg:hidden"
            aria-label="Toggle sidebar"
          >
            <Menu className="w-5 h-5" />
          </Button>

          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
              <span className="text-white font-bold text-xl">P</span>
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                Portfolio Intelligence
              </h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Multi-Agent AI System
              </p>
            </div>
          </div>
        </div>

        {/* Center Section - Client Selector */}
        <div className="flex-1 max-w-md mx-4 hidden md:block">
          <div className="relative">
            <select
              value={selectedClient}
              onChange={(e) => selectClient(e.target.value)}
              className="w-full px-4 py-2 pr-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
            >
              {clients.map((client) => (
                <option key={client.id} value={client.id}>
                  {client.id} • {client.holdings} holdings
                </option>
              ))}
            </select>
            <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <User className="w-4 h-4 text-gray-400" />
            </div>
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2">
          {/* Theme Toggle */}
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </Button>

          {/* Settings */}
          <Button
            variant="ghost"
            size="sm"
            aria-label="Settings"
          >
            <Settings className="w-5 h-5" />
          </Button>
        </div>
      </div>

      {/* Mobile Client Selector */}
      <div className="md:hidden px-4 pb-3">
        <select
          value={selectedClient}
          onChange={(e) => selectClient(e.target.value)}
          className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          {clients.map((client) => (
            <option key={client.id} value={client.id}>
              {client.id} • {client.holdings} holdings
            </option>
          ))}
        </select>
      </div>
    </header>
  );
};
