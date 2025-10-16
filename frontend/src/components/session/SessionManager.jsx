import { RefreshCcw, Trash2, Download } from 'lucide-react';
import { Button } from '../common/Button';
import { Badge } from '../common/Badge';
import { formatDate } from '../../utils/formatters';
import toast from 'react-hot-toast';

export const SessionManager = ({
  sessionId,
  conversationHistory = [],
  onClear,
  onRefresh,
  loading = false
}) => {
  const handleExport = () => {
    try {
      const data = {
        sessionId,
        timestamp: new Date().toISOString(),
        conversationHistory
      };

      const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json'
      });

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `session-${sessionId}-${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      toast.success('Session exported successfully');
    } catch (error) {
      toast.error('Failed to export session');
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div className="flex items-center justify-between flex-wrap gap-4">
        {/* Session Info */}
        <div className="flex items-center gap-3">
          <div>
            <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
              Session Active
            </h3>
            {sessionId && (
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5 font-mono">
                {sessionId.substring(0, 16)}...
              </p>
            )}
          </div>

          {conversationHistory.length > 0 && (
            <Badge variant="success" size="sm">
              {conversationHistory.length} messages
            </Badge>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={onRefresh}
            disabled={loading || !sessionId}
            title="Refresh session"
          >
            <RefreshCcw className="w-4 h-4" />
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={handleExport}
            disabled={!sessionId || conversationHistory.length === 0}
            title="Export session"
          >
            <Download className="w-4 h-4" />
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              if (confirm('Clear session? This cannot be undone.')) {
                onClear();
              }
            }}
            disabled={loading || !sessionId}
            className="text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
            title="Clear session"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
};
