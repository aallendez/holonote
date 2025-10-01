import type { Route } from "./+types/dashboard";
import { useNavigate } from "react-router";
import { useAuth } from "../context/authContext";
import { useEffect, useMemo, useState } from "react";
import { getEntries, type Entry, createEntry } from "../api/entries";
import { getMockEntries } from "../api/entries.mock";
import { Toolbar } from "../components/Toolbar";
import { Stats } from "../components/Stats";
import { LatestEntries } from "../components/LatestEntries";
import { ContributionGrid } from "../components/ContributionGrid";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Dashboard" },
    { name: "description", content: "Explore your entries and learn more about yourself!" },
  ];
}

export default function Dashboard() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (loading) return;
    if (!user) {
      navigate("/auth/log-in", { replace: true });
    }
  }, [user, loading, navigate]);

  const [entries, setEntries] = useState<Entry[]>([]);
  const [filtered, setFiltered] = useState<Entry[]>([]);
  const [dataLoading, setDataLoading] = useState(true);
  const [range, setRange] = useState<"week" | "month" | "year" | "all">("month");

  function skewedRandomScore() {
    // Skew towards higher values near 10
    const r = Math.random();
    return Math.max(1, Math.min(10, Math.round(10 - Math.pow(r, 2) * 9)));
  }

  useEffect(() => {
    (async () => {
      setDataLoading(true);
      try {
        const useMock = new URLSearchParams(window.location.search).get("mock") === "1";
        const data = useMock ? getMockEntries() : await getEntries();
        // Normalize backend fields to frontend shape if needed
        const normalized: Entry[] = (Array.isArray(data) ? data : []).map((d: any) => ({
          id: d.entry_id || d.id,
          title: d.title,
          content: d.content,
          score: (d.score ?? undefined) == null ? skewedRandomScore() : d.score,
          createdAt: d.created_at || d.createdAt || d.entry_date,
          updatedAt: d.updated_at || d.updatedAt || d.entry_date,
        }));
        setEntries(normalized);
        setFiltered(normalized);
      } catch (e) {
        const fallback = getMockEntries();
        setEntries(fallback);
        setFiltered(fallback);
      } finally {
        setDataLoading(false);
      }
    })();
  }, []);

  function handleSearch(q: string) {
    const query = q.toLowerCase();
    setFiltered(filterByRange(entries, range).filter(
      (e) =>
        e.title.toLowerCase().includes(query) ||
        e.content.toLowerCase().includes(query)
    ));
  }

  async function handleCreate() {
    const now = new Date();
    const newEntry = await createEntry({
      user_id: "juan",
      entry_date: now.toISOString(),
      title: "New Entry",
      content: "",
      score: 1,
    });
    const normalized: Entry = {
      id: newEntry.entry_id || newEntry.id,
      title: newEntry.title,
      content: newEntry.content,
      score: newEntry.score ?? 1,
      createdAt: newEntry.created_at || newEntry.entry_date,
      updatedAt: newEntry.updated_at || newEntry.entry_date,
    };
    setEntries((prev) => [normalized, ...prev]);
    setFiltered((prev) => [normalized, ...prev]);
  }

  function filterByRange(list: Entry[], r: typeof range) {
    const now = new Date();
    const start = new Date(now);
    if (r === "week") {
      const day = now.getDay();
      start.setDate(now.getDate() - day); // from Sunday
    } else if (r === "month") {
      start.setDate(1);
    } else if (r === "year") {
      start.setMonth(0, 1);
    } else {
      return list;
    }
    start.setHours(0, 0, 0, 0);
    return list.filter((e) => new Date(e.createdAt) >= start && new Date(e.createdAt) <= now);
  }

  useEffect(() => {
    // when range changes, re-filter based on current query-less baseline
    setFiltered(filterByRange(entries, range));
  }, [range, entries]);

  const { totalEntries, currentStreak, bestStreak, avgScore } = useMemo(() => {
    const base = filterByRange(entries, range);
    const byDay = new Set<string>();
    for (const e of base) {
      const d = new Date(e.createdAt);
      d.setHours(0, 0, 0, 0);
      byDay.add(d.toISOString().slice(0, 10));
    }

    // Current streak: consecutive days up to today
    let streak = 0;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const cursor = new Date(today);
    while (byDay.has(cursor.toISOString().slice(0, 10))) {
      streak += 1;
      cursor.setDate(cursor.getDate() - 1);
    }

    // Best streak: iterate over all days between min and max
    const dates = Array.from(byDay)
      .map((d) => new Date(d))
      .sort((a, b) => a.getTime() - b.getTime());
    let best = 0;
    let current = 0;
    let prev: Date | null = null;
    for (const d of dates) {
      if (prev) {
        const diff = Math.round((d.getTime() - prev.getTime()) / (24 * 3600 * 1000));
        if (diff === 1) {
          current += 1;
        } else {
          best = Math.max(best, current);
          current = 1;
        }
      } else {
        current = 1;
      }
      prev = d;
    }
    best = Math.max(best, current);

    const avg = base.length ? base.reduce((s, e) => s + (e.score ?? 0), 0) / base.length : 0;
    return { totalEntries: base.length, currentStreak: streak, bestStreak: best, avgScore: avg };
  }, [entries, range]);

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 space-y-4">
      <Toolbar onCreate={handleCreate} onSearch={handleSearch} />

      <div className="flex items-center gap-2">
        {([
          { key: "week", label: "This week" },
          { key: "month", label: "This month" },
          { key: "year", label: "This year" },
          { key: "all", label: "All time" },
        ] as const).map((t) => (
          <button
            key={t.key}
            onClick={() => setRange(t.key)}
            className={`rounded-lg border px-3 py-1.5 text-sm transition-colors ${
              range === t.key
                ? "border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                : "border-transparent hover:border-gray-200 dark:hover:border-gray-800 bg-white/40 dark:bg-gray-900/40"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <Stats totalEntries={totalEntries} currentStreak={currentStreak} bestStreak={bestStreak} avgScore={avgScore} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          <ContributionGrid
            entries={filterByRange(entries, range)}
            mode={range}
            cellSize={range === "all" || range === "year" ? 12 : 14}
          />
          <LatestEntries entries={filtered} />
        </div>
        <div className="space-y-4">
          <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-gradient-to-br from-gray-50 to-white dark:from-gray-950 dark:to-gray-900 p-6">
            <div className="text-lg font-semibold">Welcome back 👋</div>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">
              Capture your thoughts daily and keep your streak alive.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
