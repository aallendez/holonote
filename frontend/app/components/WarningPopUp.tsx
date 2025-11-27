import { useEffect, useState } from "react";

type Variant = "danger" | "warning" | "info";

interface PopupProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm?: () => void;
  onCancel?: () => void;
  variant?: Variant;
}

export function Popup({
  isOpen,
  onClose,
  title,
  message,
  confirmText = "Confirm",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
  variant = "info",
}: PopupProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  }, [isOpen]);

  const handleConfirm = () => {
    if (onConfirm) {
      onConfirm();
    }
    onClose();
  };

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    }
    onClose();
  };

  type VariantStyles = {
    confirmButton: string;
    cancelButton: string;
  };

  const variantStyles: Record<Variant, VariantStyles> = {
    danger: {
      confirmButton: "bg-red-600 hover:bg-red-700 text-white border-red-600",
      cancelButton:
        "border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20",
    },
    warning: {
      confirmButton:
        "bg-yellow-600 hover:bg-yellow-700 text-white border-yellow-600",
      cancelButton:
        "border-gray-200 dark:border-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800",
    },
    info: {
      confirmButton: "bg-blue-600 hover:bg-blue-700 text-white border-blue-600",
      cancelButton:
        "border-gray-200 dark:border-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800",
    },
  };

  const getVariantStyles = (variant: Variant): VariantStyles => {
    return variantStyles[variant];
  };

  const styles = getVariantStyles(variant);

  if (!isOpen && !isVisible) return null;

  return (
    <div
      className={`fixed inset-0 z-[9999] flex items-center justify-center transition-opacity duration-200 ${
        isVisible ? "opacity-100" : "opacity-0"
      }`}
      style={{ backgroundColor: "rgba(0, 0, 0, 0.5)" }}
    >
      <div
        className={`bg-white dark:bg-gray-900 rounded-lg p-6 max-w-md w-full mx-4 shadow-xl transition-all duration-200 ${
          isVisible ? "scale-100 opacity-100" : "scale-95 opacity-0"
        }`}
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
          {title}
        </h3>
        <p className="text-gray-600 dark:text-gray-300 mb-6">{message}</p>
        <div className="flex items-center gap-3 justify-end">
          <button
            onClick={handleCancel}
            className={`inline-flex items-center justify-center whitespace-nowrap rounded-lg border bg-white dark:bg-gray-900 px-4 py-2 text-sm font-medium shadow-sm active:opacity-80 transition-colors ${styles.cancelButton}`}
          >
            {cancelText}
          </button>
          {onConfirm && (
            <button
              onClick={handleConfirm}
              className={`inline-flex items-center justify-center whitespace-nowrap rounded-lg border px-4 py-2 text-sm font-medium shadow-sm active:opacity-80 transition-colors ${styles.confirmButton}`}
            >
              {confirmText}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
