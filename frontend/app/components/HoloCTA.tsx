interface HoloCTAProps {
  onStartHolo: () => void;
  hasTodayHolo?: boolean;
}

export function HoloCTA({ onStartHolo, hasTodayHolo = false }: HoloCTAProps) {
  if (hasTodayHolo) {
    return (
      <div className="rounded-xl border min-h-[120px] flex flex-col justify-between border-gray-200 dark:border-gray-800 bg-gradient-to-br from-green-200 to-green-100 dark:from-green-950 dark:to-green-700 p-6">
        <div className="text-center">
          <div className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            🎉 Great Job!
          </div>
          
          <div className="mb-6">
            <div className="mb-2">
              <img 
                src="/logo.svg" 
                alt="Holo Logo" 
                className="mx-auto h-16 w-16 text-blue-600 dark:text-blue-400"
              />
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-300">
              You've already completed today's Holo
            </div>
          </div>
          
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Come back tomorrow for your next reflection
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border min-h-[120px] flex flex-col justify-between border-gray-200 dark:border-gray-800 bg-gradient-to-br from-green-200 to-green-100 dark:from-green-950 dark:to-green-700 p-6">
      <div className="text-center">
        <div className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Ready for your Holo?
        </div>
        
        {/* Logo */}
        <div className="mb-6">
          <img 
            src="/logo.svg" 
            alt="Holo Logo" 
            className="mx-auto h-16 w-16 text-blue-600 dark:text-blue-400"
          />
        </div>
        
        <button
          onClick={onStartHolo}
          className="w-full bg-black hover:bg-gray-800 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl"
        >
          Start Daily Holo
        </button>
      </div>
    </div>
  );
}
