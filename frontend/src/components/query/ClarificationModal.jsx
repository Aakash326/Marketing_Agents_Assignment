import { useState, useEffect, useRef } from 'react';
import { X, AlertCircle } from 'lucide-react';
import { Button } from '../common/Button';
import clsx from 'clsx';

export const ClarificationModal = ({
  isOpen,
  onClose,
  onSubmit,
  message,
  originalQuery,
  loading = false
}) => {
  const [clarification, setClarification] = useState('');
  const inputRef = useRef(null);

  // Auto-focus on input when modal opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  // Handle ESC key
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = clarification.trim();
    if (trimmed && !loading) {
      onSubmit(trimmed);
      setClarification('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div
          className={clsx(
            'relative w-full max-w-lg',
            'bg-white dark:bg-gray-800',
            'rounded-lg shadow-xl',
            'border border-gray-200 dark:border-gray-700',
            'animate-slide-up'
          )}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-start justify-between p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0">
                <AlertCircle className="w-6 h-6 text-yellow-500" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Need Clarification
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  Please provide more details
                </p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              aria-label="Close"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Content */}
          <form onSubmit={handleSubmit} className="p-6 space-y-4">
            {/* Original Query */}
            {originalQuery && (
              <div className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-md">
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">
                  Original Query:
                </p>
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  {originalQuery}
                </p>
              </div>
            )}

            {/* Clarification Message */}
            {message && (
              <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-md border border-yellow-200 dark:border-yellow-800">
                <p className="text-sm text-yellow-900 dark:text-yellow-200">
                  {message}
                </p>
              </div>
            )}

            {/* Input */}
            <div>
              <label
                htmlFor="clarification"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                Your Clarification
              </label>
              <textarea
                ref={inputRef}
                id="clarification"
                value={clarification}
                onChange={(e) => setClarification(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Please provide additional details..."
                rows={4}
                disabled={loading}
                className="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Press Enter to submit, Shift+Enter for new line
              </p>
            </div>

            {/* Actions */}
            <div className="flex gap-3 justify-end">
              <Button
                type="button"
                variant="ghost"
                onClick={onClose}
                disabled={loading}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="primary"
                loading={loading}
                disabled={!clarification.trim()}
              >
                Submit
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
