import type { Route } from "./+types/new-entry";
import { useNavigate } from "react-router";
import { useAuth } from "../context/authContext";
import { useEffect, useState } from "react";
import { createEntry } from "../api/entries";
import { Toolbar } from "../components/Toolbar";
import { Popup } from "../components/WarningPopUp";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New Entry" },
    { name: "description", content: "Create a new journal entry" },
  ];
}

export default function NewEntry() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showCancelConfirm, setShowCancelConfirm] = useState(false);

  useEffect(() => {
    if (loading) return;
    if (!user) {
      navigate("/auth/log-in", { replace: true });
    }
  }, [user, loading, navigate]);

  const handleCancel = () => {
    if (title.trim() || content.trim()) {
      setShowCancelConfirm(true);
    } else {
      navigate("/dashboard");
    }
  };

  const handleConfirmCancel = () => {
    navigate("/dashboard");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim() || !content.trim()) {
      setError("Both title and content are required");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const now = new Date();
      await createEntry({
        entry_date: now.toISOString(),
        title: title.trim(),
        content: content.trim(),
        score: 1,
      });
      
      // Success - redirect to dashboard
      navigate("/dashboard");
    } catch (err) {
      console.error("Failed to create entry:", err);
      setError("Failed to create entry. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const currentDate = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 space-y-6">
      <Toolbar onCreate={() => {}} onSearch={() => {}} />
      
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">New Entry</h1>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {currentDate}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Title
            </label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter entry title..."
              className="w-full rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-700"
              disabled={isSubmitting}
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="content" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Content
            </label>
            <textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write your thoughts here..."
              rows={12}
              className="w-full rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-700 resize-none"
              disabled={isSubmitting}
            />
          </div>

          {error && (
            <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-3">
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}

          <div className="flex items-center gap-3 pt-4">
            <button
              type="submit"
              disabled={isSubmitting || !title.trim() || !content.trim()}
              className="inline-flex items-center justify-center whitespace-nowrap rounded-lg bg-green-600 hover:bg-green-700 text-white px-6 py-2 text-sm font-medium shadow-sm active:opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isSubmitting ? "Creating..." : "Create Entry"}
            </button>
            
            <button
              type="button"
              onClick={handleCancel}
              disabled={isSubmitting}
              className="inline-flex items-center justify-center whitespace-nowrap rounded-lg border border-red-200 dark:border-red-800 bg-white dark:bg-gray-900 text-red-600 dark:text-red-400 px-6 py-2 text-sm font-medium shadow-sm hover:bg-red-50 dark:hover:bg-red-900/20 active:opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      {/* Cancel Confirmation Dialog */}
      <Popup
        isOpen={showCancelConfirm}
        onClose={() => setShowCancelConfirm(false)}
        title="Cancel Entry"
        message="Are you sure you want to cancel this entry? Any unsaved changes will be lost."
        confirmText="Yes, Cancel"
        cancelText="Keep Editing"
        onConfirm={handleConfirmCancel}
        variant="danger"
      />
    </div>
  );
}
