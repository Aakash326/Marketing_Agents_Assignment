import { useState } from 'react';
import { Copy, Check, User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { formatRelativeTime } from '../../utils/formatters';
import clsx from 'clsx';
import toast from 'react-hot-toast';

export const MessageBubble = ({ role, content, timestamp, metadata = {} }) => {
  const [copied, setCopied] = useState(false);
  const [showTimestamp, setShowTimestamp] = useState(false);

  const isUser = role === 'user';

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      toast.success('Copied to clipboard');
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error('Failed to copy');
    }
  };

  return (
    <div
      className={clsx(
        'flex gap-3 animate-fade-in',
        isUser ? 'flex-row-reverse' : 'flex-row'
      )}
      onMouseEnter={() => setShowTimestamp(true)}
      onMouseLeave={() => setShowTimestamp(false)}
    >
      {/* Avatar */}
      <div
        className={clsx(
          'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
          isUser
            ? 'bg-primary-600 text-white'
            : 'bg-gray-600 dark:bg-gray-700 text-white'
        )}
      >
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      {/* Message Content */}
      <div className={clsx('flex-1 max-w-3xl', isUser && 'flex flex-col items-end')}>
        <div
          className={clsx(
            'px-4 py-3 rounded-lg',
            'shadow-sm border',
            'transition-all duration-200',
            'hover:shadow-md',
            isUser
              ? 'bg-primary-600 text-white border-primary-700'
              : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-gray-200 dark:border-gray-700'
          )}
        >
          {isUser ? (
            <p className="text-sm whitespace-pre-wrap">{content}</p>
          ) : (
            <div className="prose dark:prose-invert prose-sm max-w-none">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          )}
        </div>

        {/* Timestamp and Actions */}
        <div
          className={clsx(
            'flex items-center gap-2 mt-1 px-2 text-xs transition-opacity duration-200',
            showTimestamp ? 'opacity-100' : 'opacity-0'
          )}
        >
          {timestamp && (
            <span className="text-gray-500 dark:text-gray-400">
              {formatRelativeTime(timestamp)}
            </span>
          )}

          <button
            onClick={handleCopy}
            className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
            aria-label="Copy message"
          >
            {copied ? (
              <Check className="w-3 h-3" />
            ) : (
              <Copy className="w-3 h-3" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
