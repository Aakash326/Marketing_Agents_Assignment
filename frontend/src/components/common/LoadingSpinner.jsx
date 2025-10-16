import clsx from 'clsx';

export const LoadingSkeleton = ({ lines = 4, className = '' }) => {
  return (
    <div className={clsx('animate-pulse space-y-4', className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className={clsx(
            'h-4 bg-gray-200 dark:bg-gray-700 rounded',
            i % 3 === 0 ? 'w-3/4' : i % 3 === 1 ? 'w-1/2' : 'w-5/6'
          )}
        />
      ))}
    </div>
  );
};

export const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizes = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-4',
    lg: 'w-12 h-12 border-4',
  };

  return (
    <div className={clsx('flex items-center justify-center', className)}>
      <div
        className={clsx(
          'border-gray-200 dark:border-gray-700',
          'border-t-primary-600',
          'rounded-full',
          'animate-spin',
          sizes[size]
        )}
      />
    </div>
  );
};

export const LoadingDots = ({ className = '' }) => {
  return (
    <div className={clsx('flex items-center justify-center gap-1', className)}>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="w-2 h-2 bg-primary-600 rounded-full animate-pulse"
          style={{
            animationDelay: `${i * 0.15}s`,
          }}
        />
      ))}
    </div>
  );
};
