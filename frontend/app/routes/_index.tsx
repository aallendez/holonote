import { Navigate, Link } from "react-router";
import { useAuth } from "../context/authContext";

export default function Index() {
  const { user, loading } = useAuth();
  if (loading) {
    return null;
  }
  if (user) return <Navigate to="/dashboard" replace />;
  return (
    <main className="cursor-default flex flex-col items-center justify-center px-6 py-16">
      <div className="max-w-4xl w-full text-center">
        <div className="flex items-center justify-center gap-3 mb-6">
          <img src="/logo.svg" alt="Holonote" className="h-10 w-10" />
          <span className="text-2xl font-semibold tracking-tight">Holonote</span>
        </div>

        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-gray-900 dark:text-white">
          Reflect daily. Grow intentionally.
        </h1>
        <p className="mt-4 text-base md:text-lg text-gray-600 dark:text-gray-300">
          Holonote helps you build a mindful habit with quick daily check-ins. <br />Get insights into your habits and patterns.
        </p>

        <div className="mt-8 flex items-center justify-center gap-3">
          <Link
            to="/auth/log-in"
            className="inline-flex items-center justify-center rounded-lg bg-black text-white px-5 py-3 text-sm font-medium shadow-lg hover:bg-gray-800 transition-colors"
          >
            Log in to get started
          </Link>
          <a
            href="#features"
            className="inline-flex items-center justify-center rounded-lg border border-gray-300 dark:border-gray-700 px-5 py-3 text-sm font-medium text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors"
          >
            Learn more
          </a>
        </div>

        <div id="features" className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
          <div className="rounded-xl border border-gray-200 dark:border-gray-800 p-6 bg-white/50 dark:bg-gray-950/50">
            <div className="text-base font-semibold text-gray-900 dark:text-white mb-1">Daily Holo</div>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              A lightweight daily pulse with 10 quick questions to anchor your day.
            </p>
          </div>
          <div className="rounded-xl border border-gray-200 dark:border-gray-800 p-6 bg-white/50 dark:bg-gray-950/50">
            <div className="text-base font-semibold text-gray-900 dark:text-white mb-1">Trends & insights</div>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              See streaks and simple stats to keep momentum and notice patterns.
            </p>
          </div>
          <div className="rounded-xl border border-gray-200 dark:border-gray-800 p-6 bg-white/50 dark:bg-gray-950/50">
            <div className="text-base font-semibold text-gray-900 dark:text-white mb-1">Private by design</div>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Your reflections stay yours. Secure auth and minimal data by default.
            </p>
          </div>
        </div>

        <p className="mt-10 text-xs text-gray-500 dark:text-gray-400">
          By continuing you agree to a mindful habit, not perfection. One check-in a day is enough.
        </p>
      </div>
    </main>
  );
}