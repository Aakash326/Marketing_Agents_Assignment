import { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Button } from '../common/Button';
import { QuerySuggestions } from './QuerySuggestions';
import clsx from 'clsx';

const MAX_LENGTH = 1000;

export const QueryInput = ({ onSubmit, loading = false, disabled = false }) => {
  const [query, setQuery] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  }, [query]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Cmd/Ctrl + K to focus
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        textareaRef.current?.focus();
      }

      // Cmd/Ctrl + Enter to submit
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault();
        handleSubmit();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [query]);

  const handleSubmit = () => {
    const trimmed = query.trim();
    if (trimmed && !loading && !disabled) {
      onSubmit(trimmed);
      setQuery('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    textareaRef.current?.focus();
  };

  const charCount = query.length;
  const isOverLimit = charCount > MAX_LENGTH;

  return (
    <div className="space-y-4">
      <div className="relative">
        <textarea
          ref={textareaRef}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about your portfolio... (Cmd/Ctrl + K to focus, Cmd/Ctrl + Enter to submit)"
          disabled={disabled || loading}
          rows={3}
          className={clsx(
            'w-full px-4 py-3 pr-24',
            'bg-white dark:bg-gray-800',
            'border-2 rounded-lg',
            'text-gray-900 dark:text-white',
            'placeholder-gray-400 dark:placeholder-gray-500',
            'focus:outline-none focus:ring-2 focus:ring-primary-500',
            'resize-none transition-all duration-200',
            isOverLimit
              ? 'border-red-500 dark:border-red-500'
              : 'border-gray-300 dark:border-gray-600',
            'disabled:opacity-50 disabled:cursor-not-allowed'
          )}
          style={{ minHeight: '80px' }}
        />

        {/* Submit Button */}
        <div className="absolute bottom-3 right-3">
          <Button
            onClick={handleSubmit}
            disabled={disabled || loading || !query.trim() || isOverLimit}
            size="sm"
            aria-label="Submit query"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>

      {/* Character Counter */}
      <div className="flex items-center justify-between text-sm">
        <div className="text-gray-500 dark:text-gray-400">
          <kbd className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 rounded border border-gray-300 dark:border-gray-600">
            ⌘/Ctrl + Enter
          </kbd>
          <span className="ml-2">to submit</span>
        </div>

        <span
          className={clsx(
            'font-medium',
            isOverLimit
              ? 'text-red-600 dark:text-red-400'
              : charCount > MAX_LENGTH * 0.9
              ? 'text-yellow-600 dark:text-yellow-400'
              : 'text-gray-500 dark:text-gray-400'
          )}
        >
          {charCount} / {MAX_LENGTH}
        </span>
      </div>

      {/* Query Suggestions */}
      <QuerySuggestions onSelect={handleSuggestionClick} disabled={loading} />
    </div>
  );
};
