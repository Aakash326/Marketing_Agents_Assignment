import { Lightbulb } from 'lucide-react';
import { QUERY_SUGGESTIONS } from '../../utils/constants';
import clsx from 'clsx';

export const QuerySuggestions = ({ onSelect, disabled = false }) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
        <Lightbulb className="w-4 h-4" />
        <span className="font-medium">Try asking:</span>
      </div>

      <div className="flex flex-wrap gap-2">
        {QUERY_SUGGESTIONS.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => onSelect(suggestion)}
            disabled={disabled}
            className={clsx(
              'px-3 py-2 text-sm',
              'bg-white dark:bg-gray-800',
              'border border-gray-300 dark:border-gray-600',
              'rounded-full',
              'text-gray-700 dark:text-gray-300',
              'hover:bg-gray-50 dark:hover:bg-gray-700',
              'hover:border-primary-500 dark:hover:border-primary-500',
              'transition-all duration-200',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              'focus:outline-none focus:ring-2 focus:ring-primary-500'
            )}
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
};
