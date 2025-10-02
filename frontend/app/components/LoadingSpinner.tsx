type LoadingSpinnerProps = {
  label?: string;
  className?: string;
  size?: number; // px
};

export function LoadingSpinner({ label = "Loading...", className = "", size = 20 }: LoadingSpinnerProps) {
  const spinnerSize = `${size}px`;
  const borderSize = `${Math.max(2, Math.round(size / 10))}px`;
  return (
    <div className={`flex items-center justify-center gap-2 text-gray-600 dark:text-gray-300 ${className}`}>
      <span
        aria-hidden
        className="inline-block animate-spin rounded-full border-current border-t-transparent"
        style={{ width: spinnerSize, height: spinnerSize, borderWidth: borderSize }}
      />
      <span className="text-sm select-none">{label}</span>
    </div>
  );
}


