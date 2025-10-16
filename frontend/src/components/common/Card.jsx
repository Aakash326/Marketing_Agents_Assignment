import clsx from 'clsx';

export const Card = ({
  children,
  title,
  subtitle,
  headerAction,
  className = '',
  padding = true,
  hover = false,
  ...props
}) => {
  return (
    <div
      className={clsx(
        'bg-white dark:bg-gray-800',
        'rounded-lg shadow-md',
        'border border-gray-200 dark:border-gray-700',
        'transition-all duration-200',
        hover && 'hover:shadow-lg',
        className
      )}
      {...props}
    >
      {(title || headerAction) && (
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <div>
            {title && (
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                {title}
              </h3>
            )}
            {subtitle && (
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {subtitle}
              </p>
            )}
          </div>
          {headerAction}
        </div>
      )}
      <div className={clsx(padding && 'p-6')}>
        {children}
      </div>
    </div>
  );
};
