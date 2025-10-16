import { Badge } from '../common/Badge';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';
import clsx from 'clsx';

export const AgentStatusBadge = ({
  name,
  active = false,
  status = 'idle', // idle, active, completed
  showIcon = true,
  size = 'md'
}) => {
  const getVariant = () => {
    if (status === 'completed') return 'success';
    if (status === 'active') return 'primary';
    return 'default';
  };

  const getIcon = () => {
    if (!showIcon) return null;

    if (status === 'completed') {
      return <CheckCircle2 className="w-3 h-3" />;
    }

    if (status === 'active') {
      return <Loader2 className="w-3 h-3 animate-spin" />;
    }

    return <Circle className="w-3 h-3" />;
  };

  return (
    <Badge
      variant={getVariant()}
      size={size}
      className={clsx(
        'transition-all duration-300',
        status === 'active' && 'animate-pulse'
      )}
    >
      {getIcon()}
      {name}
    </Badge>
  );
};
