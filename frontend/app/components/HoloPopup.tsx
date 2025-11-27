import { useState, useEffect } from "react";
import {
  getHoloConfig,
  createHoloConfig,
  createHoloDaily,
  type HoloConfig,
  type HoloDailyCreate,
} from "../api/holos";
import { LoadingSpinner } from "./LoadingSpinner";

interface HoloPopupProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: () => void;
}

const DEFAULT_QUESTIONS = [
  "Did I wake up feeling refreshed?",
  "Did I exercise or move my body today?",
  "Did I eat nutritious meals?",
  "Did I connect with someone I care about?",
  "Did I learn something new?",
  "Did I take time for self-care?",
  "Did I make progress on my goals?",
  "Did I feel grateful for something today?",
  "Did I get enough sleep last night?",
  "Did I feel productive and accomplished?",
];

export function HoloPopup({ isOpen, onClose, onComplete }: HoloPopupProps) {
  const [questions, setQuestions] = useState<string[]>([]);
  const [answers, setAnswers] = useState<Record<string, boolean>>({});
  const [dailyScore, setDailyScore] = useState<number>(5);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadHoloConfig();
    }
  }, [isOpen]);

  const loadHoloConfig = async () => {
    console.log("🔄 Loading holo config...");
    setLoading(true);
    setError(null);
    try {
      console.log("🔄 Calling getHoloConfig...");
      const config = await getHoloConfig();
      console.log("🔄 Got config:", config);
      console.log("🔄 Questions:", config.questions);
      setQuestions(config.questions);
      setAnswers({});
    } catch (err) {
      console.error("🔄 Error loading config:", err);
      if (
        err instanceof Error &&
        err.message.includes("No holo configuration found")
      ) {
        console.log("🔄 No config found, creating default...");
        // Create default config if none exists
        try {
          const newConfig = await createHoloConfig(DEFAULT_QUESTIONS);
          console.log("🔄 Created new config:", newConfig);
          setQuestions(newConfig.questions);
          setAnswers({});
        } catch (createErr) {
          console.error("🔄 Error creating config:", createErr);
          setError("Failed to create holo configuration");
        }
      } else {
        console.error("🔄 Other error:", err);
        setError("Failed to load holo configuration");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (question: string, value: boolean) => {
    setAnswers((prev) => ({
      ...prev,
      [question]: value,
    }));
  };

  // Remove the calculateScore function since score is now user input

  const handleSubmit = async () => {
    if (questions.length === 0) return;

    setSubmitting(true);
    setError(null);

    try {
      const today = new Date().toISOString().split("T")[0];

      const holoDaily: HoloDailyCreate = {
        entry_date: today,
        score: dailyScore,
        answers,
      };

      await createHoloDaily(holoDaily);
      onComplete();
      onClose();
    } catch (err) {
      console.error("Error submitting holo daily:", err);
      setError(
        `Failed to submit your holo daily: ${err instanceof Error ? err.message : "Unknown error"}`,
      );
    } finally {
      setSubmitting(false);
    }
  };

  const allAnswered =
    questions.length > 0 && Object.keys(answers).length === questions.length;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center p-4 z-[9999]">
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <div className="relative bg-white dark:bg-gray-900 rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                Daily Holo
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Answer these questions to track your daily well-being
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {dailyScore}/10
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  Today's Score
                </div>
              </div>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <LoadingSpinner label="Loading questions..." size={32} />
            </div>
          ) : error ? (
            <div className="text-center py-8">
              <div className="text-red-600 dark:text-red-400 mb-2">{error}</div>
              <button
                onClick={loadHoloConfig}
                className="px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
              >
                Try Again
              </button>
            </div>
          ) : questions.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-gray-600 dark:text-gray-300 mb-4">
                No questions available
              </div>
              <button
                onClick={loadHoloConfig}
                className="px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
              >
                Load Questions
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Daily Score Input */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950 rounded-xl p-6 border border-blue-200 dark:border-blue-800">
                <div className="text-center">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    How was your day overall?
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mb-4">
                    Rate your day from 0 (terrible) to 10 (amazing)
                  </p>
                  <div className="flex items-center justify-center space-x-2">
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      0
                    </span>
                    <input
                      type="range"
                      min="0"
                      max="10"
                      value={dailyScore}
                      onChange={(e) => setDailyScore(parseInt(e.target.value))}
                      className="w-48 h-2 bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 rounded-lg appearance-none cursor-pointer"
                      style={{
                        background: `linear-gradient(to right, #ef4444 0%, #f59e0b 50%, #10b981 100%)`,
                      }}
                    />
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      10
                    </span>
                  </div>
                  <div className="mt-2 text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {dailyScore}
                  </div>
                </div>
              </div>

              {/* Questions */}
              <div className="space-y-3">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                  Daily Reflection Questions
                </h3>
                {questions.map((question, index) => (
                  <div
                    key={index}
                    className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-gray-900 dark:text-white font-medium text-sm leading-relaxed">
                        {question}
                      </span>
                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={() => handleAnswerChange(question, true)}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                            answers[question] === true
                              ? "bg-green-100 text-green-700 border-2 border-green-300 dark:bg-green-900 dark:text-green-300 dark:border-green-600"
                              : "bg-gray-100 text-gray-600 border-2 border-gray-200 hover:bg-green-50 hover:text-green-600 hover:border-green-300 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-green-900 dark:hover:text-green-300 dark:hover:border-green-600"
                          }`}
                        >
                          ✓ Yes
                        </button>
                        <button
                          onClick={() => handleAnswerChange(question, false)}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                            answers[question] === false
                              ? "bg-red-100 text-red-700 border-2 border-red-300 dark:bg-red-900 dark:text-red-300 dark:border-red-600"
                              : "bg-gray-100 text-gray-600 border-2 border-gray-200 hover:bg-red-50 hover:text-red-600 hover:border-red-300 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-red-900 dark:hover:text-red-300 dark:hover:border-red-600"
                          }`}
                        >
                          ✗ No
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {questions.length > 0 && (
          <div className="p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-600 dark:text-gray-300">
                {Object.keys(answers).length} of {questions.length} questions
                answered • Score: {dailyScore}/10
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={onClose}
                  className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSubmit}
                  disabled={!allAnswered || submitting}
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
                >
                  {submitting ? (
                    <LoadingSpinner
                      label="Submitting..."
                      size={16}
                      className="text-white"
                    />
                  ) : (
                    "Submit Holo"
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
