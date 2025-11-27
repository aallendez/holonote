import { useEffect, useState } from "react";
import type { DragEvent } from "react";
import { Navigate } from "react-router";
import { useAuth } from "../context/authContext";
import { LoadingSpinner } from "../components/LoadingSpinner";
import {
  createHoloConfig,
  getHoloConfig,
  updateHoloConfig,
  type HoloConfig,
} from "../api/holos";
import { Toolbar } from "../components/Toolbar";

export default function SettingsRoute() {
  const { user, loading } = useAuth();
  const [initialQuestions, setInitialQuestions] = useState<string[] | null>(
    null,
  );
  const [questions, setQuestions] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragIndex, setDragIndex] = useState<number | null>(null);
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null);

  const userDisplayName = user?.displayName || "Anonymous";
  const userEmail = user?.email || "";
  const photoUrl = user?.photoURL || user?.providerData?.[0]?.photoURL;

  useEffect(() => {
    if (!user) return;
    let isMounted = true;
    (async () => {
      setBusy(true);
      setError(null);
      try {
        const cfg: HoloConfig = await getHoloConfig();
        if (!isMounted) return;
        setInitialQuestions(cfg.questions);
        setQuestions(cfg.questions);
      } catch (e: any) {
        // If no config yet, start empty
        if (String(e?.message || "").includes("No holo configuration")) {
          if (!isMounted) return;
          setInitialQuestions([]);
          setQuestions([]);
        } else {
          setError(e?.message || "Failed to load holo config");
        }
      } finally {
        setBusy(false);
      }
    })();
    return () => {
      isMounted = false;
    };
  }, [user]);

  if (loading)
    return (
      <div className="p-6">
        <LoadingSpinner label="Loading..." />
      </div>
    );
  if (!user) return <Navigate to="/auth/log-in" replace />;

  function onDragStart(index: number) {
    setDragIndex(index);
  }

  function onDragOver(index: number, e: DragEvent) {
    e.preventDefault();
    if (dragOverIndex !== index) setDragOverIndex(index);
  }

  function onDrop(index: number) {
    if (dragIndex == null || index === dragIndex) {
      setDragIndex(null);
      setDragOverIndex(null);
      return;
    }
    setQuestions((prev) => {
      const next = prev.slice();
      const [m] = next.splice(dragIndex, 1);
      const insertAt = index > dragIndex ? index : index;
      next.splice(insertAt, 0, m);
      return next;
    });
    setDragIndex(null);
    setDragOverIndex(null);
  }

  function removeQuestion(index: number) {
    setQuestions((prev) => prev.filter((_, i) => i !== index));
  }

  function addQuestion() {
    setQuestions((prev) => [...prev, ""]);
  }

  function updateQuestion(index: number, value: string) {
    setQuestions((prev) => prev.map((q, i) => (i === index ? value : q)));
  }

  const hasChanges =
    initialQuestions != null &&
    JSON.stringify(initialQuestions) !== JSON.stringify(questions);

  async function handleSave() {
    if (!hasChanges) return;
    setBusy(true);
    setError(null);
    try {
      const cleaned = questions
        .map((q) => q.trim())
        .filter((q) => q.length > 0);
      if ((initialQuestions || []).length === 0) {
        await createHoloConfig(cleaned);
      } else {
        await updateHoloConfig(cleaned);
      }
      setInitialQuestions(cleaned);
      setQuestions(cleaned);
    } catch (e: any) {
      setError(e?.message || "Failed to save changes");
    } finally {
      setBusy(false);
    }
  }

  function handleDiscard() {
    if (initialQuestions != null) setQuestions(initialQuestions);
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 space-y-4">
      <Toolbar onCreate={() => {}} onSearch={() => {}} />
      <section className="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white/70 dark:bg-gray-900/70 backdrop-blur p-6 flex items-center gap-5 shadow-sm">
        <div className="w-14 h-14 rounded-full overflow-hidden bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
          {photoUrl ? (
            <img
              src={photoUrl}
              alt={userDisplayName}
              className="w-14 h-14 object-cover"
            />
          ) : (
            <svg
              viewBox="0 0 24 24"
              className="w-7 h-7 text-gray-500"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M20 21a8 8 0 0 0-16 0" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          )}
        </div>
        <div className="flex flex-col">
          <div className="text-lg font-semibold tracking-tight">
            {userDisplayName}
          </div>
          {userEmail && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {userEmail}
            </div>
          )}
        </div>
      </section>

      <section className="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white/70 dark:bg-gray-900/70 backdrop-blur p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold tracking-tight">
            Edit your holo
          </h2>
          {busy && <LoadingSpinner size={16} />}
        </div>
        {error && <div className="mb-3 text-sm text-red-600">{error}</div>}
        <div className="flex flex-col gap-2">
          {questions.length === 0 && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              No questions yet. Add your first question.
            </div>
          )}
          {questions.map((q, i) => {
            const isDragging = dragIndex === i;
            const isOver =
              dragOverIndex === i && dragIndex !== null && dragIndex !== i;
            return (
              <div
                key={i}
                className={`group flex items-center gap-3 rounded-lg border ${isOver ? "border-blue-300 ring-2 ring-blue-200" : "border-gray-200 dark:border-gray-800"} bg-white dark:bg-gray-900 px-3 py-2 shadow-sm`}
                draggable
                onDragStart={() => onDragStart(i)}
                onDragOver={(e) => onDragOver(i, e)}
                onDrop={() => onDrop(i)}
              >
                <div
                  className={`cursor-move text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 ${isDragging ? "opacity-70" : ""}`}
                  title="Drag to reorder"
                >
                  <svg
                    viewBox="0 0 24 24"
                    width="18"
                    height="18"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M8 9h8M8 15h8" />
                  </svg>
                </div>
                <input
                  value={q}
                  onChange={(e) => updateQuestion(i, e.target.value)}
                  placeholder={`Question #${i + 1}`}
                  className="flex-1 rounded-md border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-700"
                />
                <button
                  onClick={() => removeQuestion(i)}
                  className="px-2 py-1 rounded-md border border-gray-200 dark:border-gray-800 text-xs text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
                >
                  Delete
                </button>
              </div>
            );
          })}
          <div>
            <button
              onClick={addQuestion}
              className="inline-flex items-center gap-2 rounded-md border border-gray-200 dark:border-gray-800 px-3 py-2 text-sm hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              Add question
            </button>
          </div>
        </div>
        <div className="mt-5 flex items-center gap-2">
          <button
            onClick={handleSave}
            disabled={!hasChanges || busy}
            className="inline-flex items-center rounded-md bg-gray-900 text-white dark:bg-white dark:text-gray-900 px-3 py-2 text-sm font-medium disabled:opacity-50 hover:opacity-90"
          >
            Save changes
          </button>
          <button
            onClick={handleDiscard}
            disabled={!hasChanges || busy}
            className="inline-flex items-center rounded-md border border-gray-200 dark:border-gray-800 px-3 py-2 text-sm disabled:opacity-50 hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            Discard
          </button>
        </div>
      </section>
    </div>
  );
}
