import { useState } from 'react';
import { Copy, Check, ChevronDown, ChevronUp } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Button } from '../common/Button';
import { Badge } from '../common/Badge';
import { LoadingSkeleton } from '../common/LoadingSpinner';
import { formatExecutionTime } from '../../utils/formatters';
import clsx from 'clsx';
import toast from 'react-hot-toast';

export const ResponseDisplay = ({
  response,
  loading = false,
  error = null,
  executionTime = null,
  agentState = null
}) => {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(true);

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 p-6 animate-fade-in">
        <LoadingSkeleton lines={6} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 rounded-lg border-2 border-red-200 dark:border-red-800 p-6 animate-slide-up">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
            <span className="text-white text-lg">!</span>
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-red-900 dark:text-red-200 mb-2">
              Error
            </h3>
            <p className="text-red-800 dark:text-red-300">
              {error}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600 p-12 text-center">
        <p className="text-gray-500 dark:text-gray-400 text-lg">
          Ask a question to get started
        </p>
      </div>
    );
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(response.response || response.message || '');
      setCopied(true);
      toast.success('Copied to clipboard');
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error('Failed to copy');
    }
  };

  // Get active agents
  const activeAgents = agentState
    ? Object.entries(agentState)
        .filter(([key, value]) => value === true && key.endsWith('_used'))
        .map(([key]) => key.replace('_used', ''))
    : [];

  const isLongResponse = (response.response?.length || 0) > 500;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 animate-slide-up">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3 flex-wrap">
            {/* Agent Badges */}
            {activeAgents.length > 0 && (
              <div className="flex items-center gap-2">
                {activeAgents.map((agent) => (
                  <Badge
                    key={agent}
                    variant="primary"
                    size="sm"
                    dot
                  >
                    {agent.charAt(0).toUpperCase() + agent.slice(1)}
                  </Badge>
                ))}
              </div>
            )}

            {/* Execution Time */}
            {executionTime && (
              <Badge variant="default" size="sm">
                {formatExecutionTime(executionTime)}
              </Badge>
            )}
          </div>

          <div className="flex items-center gap-2">
            {/* Copy Button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCopy}
              disabled={copied}
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4" />
                  Copied
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  Copy
                </>
              )}
            </Button>

            {/* Expand/Collapse for long responses */}
            {isLongResponse && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setExpanded(!expanded)}
              >
                {expanded ? (
                  <>
                    <ChevronUp className="w-4 h-4" />
                    Collapse
                  </>
                ) : (
                  <>
                    <ChevronDown className="w-4 h-4" />
                    Expand
                  </>
                )}
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div
        className={clsx(
          'px-6 py-4',
          !expanded && isLongResponse && 'max-h-64 overflow-hidden relative'
        )}
      >
        <div className="prose dark:prose-invert max-w-none">
          <ReactMarkdown>
            {response.response || response.message || 'No response'}
          </ReactMarkdown>
        </div>

        {!expanded && isLongResponse && (
          <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-white dark:from-gray-800 to-transparent" />
        )}
      </div>
    </div>
  );
};
