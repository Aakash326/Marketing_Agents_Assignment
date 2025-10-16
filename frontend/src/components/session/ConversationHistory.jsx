import { useState } from 'react';
import { ChevronDown, ChevronUp, MessageSquare, Trash2 } from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { Button } from '../common/Button';
import { Badge } from '../common/Badge';
import clsx from 'clsx';

export const ConversationHistory = ({
  messages = [],
  onClear,
  loading = false
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const interactionCount = Math.floor(messages.length / 2);

  if (messages.length === 0) {
    return null;
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <MessageSquare className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          <span className="font-semibold text-gray-900 dark:text-white">
            Conversation History
          </span>
          <Badge variant="default" size="sm">
            {interactionCount} interaction{interactionCount !== 1 ? 's' : ''}
          </Badge>
        </div>

        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                if (confirm('Clear conversation history?')) {
                  onClear();
                }
              }}
              disabled={loading}
              className="text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          )}

          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-gray-400" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-400" />
          )}
        </div>
      </button>

      {/* Messages */}
      {isExpanded && (
        <div
          className={clsx(
            'px-6 py-4 space-y-4',
            'border-t border-gray-200 dark:border-gray-700',
            'max-h-96 overflow-y-auto'
          )}
        >
          {messages.map((message, index) => (
            <MessageBubble
              key={index}
              role={message.role}
              content={message.content}
              timestamp={message.timestamp}
              metadata={message.metadata}
            />
          ))}
        </div>
      )}
    </div>
  );
};
