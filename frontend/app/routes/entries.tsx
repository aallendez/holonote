import type { Route } from "./+types/entries";
import { useNavigate, useSearchParams } from "react-router";
import { useAuth } from "../context/authContext";
import { useEffect, useState } from "react";
import { getEntries, deleteEntry, type Entry } from "../api/entries";
import { Toolbar } from "../components/Toolbar";
import { Popup } from "../components/WarningPopUp";
import { LoadingSpinner } from "../components/LoadingSpinner";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Entry Details" },
    { name: "description", content: "View journal entry details" },
  ];
}

export default function Entries() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [entry, setEntry] = useState<Entry | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const entryId = searchParams.get("entry");

  useEffect(() => {
    if (authLoading) return;
    if (!user) {
      navigate("/auth/log-in", { replace: true });
      return;
    }

    if (!entryId) {
      navigate("/dashboard", { replace: true });
      return;
    }

    fetchEntry();
  }, [user, authLoading, navigate, entryId]);

  const fetchEntry = async () => {
    if (!entryId) return;

    try {
      setLoading(true);
      setError(null);
      const entries = await getEntries();
      const foundEntry = entries.find((e: Entry) => e.entry_id === entryId);
      
      if (!foundEntry) {
        setError("Entry not found");
        return;
      }
      
      setEntry(foundEntry);
    } catch (err) {
      console.error("Failed to fetch entry:", err);
      setError("Failed to load entry. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!entry) return;

    try {
      setDeleting(true);
      setError(null);
      await deleteEntry(entry.entry_id);
      
      // Success - redirect to dashboard
      navigate("/dashboard");
    } catch (err) {
      console.error("Failed to delete entry:", err);
      setError("Failed to delete entry. Please try again.");
    } finally {
      setDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  const handleConfirmDelete = () => {
    handleDelete();
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-6">
        <Toolbar onCreate={() => {}} onSearch={() => {}} />
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner label="Loading entry..." />
        </div>
      </div>
    );
  }

  if (error || !entry) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-6 space-y-6">
        <Toolbar onCreate={() => {}} onSearch={() => {}} />
        
        <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-6">
          <h2 className="text-lg font-semibold text-red-800 dark:text-red-200 mb-2">
            Error
          </h2>
          <p className="text-red-600 dark:text-red-400 mb-4">
            {error || "Entry not found"}
          </p>
          <button
            onClick={() => navigate("/dashboard")}
            className="inline-flex items-center justify-center whitespace-nowrap rounded-lg bg-red-600 hover:bg-red-700 text-white px-4 py-2 text-sm font-medium shadow-sm active:opacity-80 transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 space-y-6">
      <Toolbar onCreate={() => {}} onSearch={() => {}} />
      
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <button
            onClick={() => navigate("/dashboard")}
            className="inline-flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
          >
            <span>←</span>
            Back to Dashboard
          </button>
          
          <button
            onClick={() => setShowDeleteConfirm(true)}
            disabled={deleting}
            className="inline-flex items-center justify-center whitespace-nowrap rounded-lg border border-red-200 dark:border-red-800 bg-white dark:bg-gray-900 text-red-600 dark:text-red-400 px-4 py-2 text-sm font-medium shadow-sm hover:bg-red-50 dark:hover:bg-red-900/20 active:opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {deleting ? "Deleting..." : "Delete Entry"}
          </button>
        </div>

        <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 space-y-6">
          <div className="space-y-2">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {formatDate(entry.created_at)}
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
              {entry.title}
            </h1>
          </div>

          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Content
            </h2>
            <div className="prose prose-sm max-w-none text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
              {entry.content}
            </div>
          </div>
        </div>

        {error && (
          <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-3">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}
      </div>

      {/* Delete Confirmation Dialog */}
      <Popup
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        title="Delete Entry"
        message="Are you sure you want to delete this entry? This action cannot be undone."
        confirmText="Yes, Delete"
        cancelText="Cancel"
        onConfirm={handleConfirmDelete}
        variant="danger"
      />
    </div>
  );
}
