import { useLatestHolo } from '../hooks/useLatestHolo';
import { LoadingSpinner } from './LoadingSpinner';

interface LatestHoloProps {
  onStartHolo: () => void;
  refreshTrigger?: boolean;
}

export function LatestHolo({ onStartHolo, refreshTrigger }: LatestHoloProps) {
  const { data: latestHolo, loading, error, isAuthenticated } = useLatestHolo(refreshTrigger);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600 dark:text-green-400';
    if (score >= 6) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreEmoji = (score: number) => {
    if (score >= 8) return '😊';
    if (score >= 6) return '😐';
    return '😔';
  };

  if (loading) {
    return (
      <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-gradient-to-br from-green-50 to-green-200 dark:from-green-950 dark:to-green-900 p-6">
        <LoadingSpinner label="Loading your latest holo..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-gradient-to-br from-green-50 to-green-200 dark:from-green-950 dark:to-green-900 p-6">
        <div className="text-center">
          <div className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Please log in
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
            You need to be logged in to view your holos
          </p>
        </div>
      </div>
    );
  }

  if (!latestHolo) {
    return (
      <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-gradient-to-br from-green-50 to-green-200 dark:from-green-950 dark:to-green-900 p-6">
        <div className="text-center">
          <div className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            No Holo Yet
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
            Start your daily reflection journey
          </p>
        </div>
      </div>
    );
  }

  const yesAnswers = Object.values(latestHolo.answers).filter(Boolean).length;
  const totalQuestions = Object.keys(latestHolo.answers).length;
  const completionRate = totalQuestions > 0 ? Math.round((yesAnswers / totalQuestions) * 100) : 0;

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-gradient-to-br from-green-50 to-green-200 dark:from-green-950 dark:to-green-900 p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            Latest Holo
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-300">
            {formatDate(latestHolo.entry_date)}
          </div>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${getScoreColor(latestHolo.score)}`}>
            {latestHolo.score}/10
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            {getScoreEmoji(latestHolo.score)} Daily Score
          </div>
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600 dark:text-gray-300">Completion Rate</span>
          <span className="font-medium text-gray-900 dark:text-white">
            {completionRate}% ({yesAnswers}/{totalQuestions})
          </span>
        </div>
      </div>
    </div>
  );
}
