import type { Route } from "./+types/dashboard";
import { useNavigate } from "react-router";
import { useAuth } from "../context/authContext";
import { useEffect, useMemo, useState } from "react";
import { getEntries, type Entry } from "../api/entries";
import { useTodayHolo } from "../hooks/useTodayHolo";
import { Toolbar } from "../components/Toolbar";
import { Stats } from "../components/Stats";
import { LatestEntries } from "../components/LatestEntries";
import { ContributionGrid } from "../components/ContributionGrid";
import { HoloPopup } from "../components/HoloPopup";
import { HoloCTA } from "../components/HoloCTA";
import { LatestHolo } from "../components/LatestHolo";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { getAvgScore } from "../api/holos";

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
  const [showHoloPopup, setShowHoloPopup] = useState(false);
  const [refreshLatestHolo, setRefreshLatestHolo] = useState(false);
  const [avgScore, setAvgScore] = useState<number | null>(null);
  
  // Use the custom hook for today's holo check
  const { data: todayHolo, refetch: refetchTodayHolo } = useTodayHolo();
  const hasTodayHolo = !!todayHolo;

  useEffect(() => {
    if (loading) return;
    if (!user) return;
    (async () => {
      setDataLoading(true);
      try {
        const data = await getEntries();
        // Use backend data directly since Entry interface now matches backend
        const entries: Entry[] = Array.isArray(data) ? data : [];
        setEntries(entries);
        setFiltered(entries);
      } catch (e) {
        // On failure, show empty state rather than mock data
        setEntries([]);
        setFiltered([]);
      } finally {
        setDataLoading(false);
      }
    })();
  }, [loading, user]);

  // Fetch average score
  useEffect(() => {
    if (loading) return;
    if (!user) return;
    (async () => {
      try {
        const response = await getAvgScore();
        setAvgScore(response.avg_score);
      } catch (e) {
        console.error("Failed to fetch average score:", e);
        setAvgScore(null);
      }
    })();
  }, [loading, user]);

  function handleSearch(q: string) {
    const query = q.toLowerCase();
    setFiltered(filterByRange(entries, range).filter(
      (e) =>
        e.title.toLowerCase().includes(query) ||
        e.content.toLowerCase().includes(query)
    ));
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
    return list.filter((e) => new Date(e.created_at) >= start && new Date(e.created_at) <= now);
  }

  useEffect(() => {
    // when range changes, re-filter based on current query-less baseline
    setFiltered(filterByRange(entries, range));
  }, [range, entries]);

  const { totalEntries, currentStreak, bestStreak } = useMemo(() => {
    const base = filterByRange(entries, range);
    const byDay = new Set<string>();
    for (const e of base) {
      const d = new Date(e.created_at);
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

    return { totalEntries: base.length, currentStreak: streak, bestStreak: best };
  }, [entries, range]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner label="Loading dashboard..." size={24} />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 space-y-4">
      <Toolbar onSearch={handleSearch} />

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

      <Stats totalEntries={totalEntries} currentStreak={currentStreak} bestStreak={bestStreak} avgScore={avgScore || 0} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          <ContributionGrid
            entries={filterByRange(entries, range)}
            mode={range}
            cellSize={range === "all" || range === "year" ? 12 : 14}
          />
          <LatestEntries entries={filtered} loading={dataLoading} />
        </div>
        <div className="space-y-4">
          <LatestHolo onStartHolo={() => setShowHoloPopup(true)} refreshTrigger={refreshLatestHolo} />
          <HoloCTA onStartHolo={() => setShowHoloPopup(true)} hasTodayHolo={hasTodayHolo} />
        </div>
      </div>

      <HoloPopup
        isOpen={showHoloPopup}
        onClose={() => setShowHoloPopup(false)}
        onComplete={async () => {
          // Refresh today's holo status after completion
          await refetchTodayHolo();
          // Trigger LatestHolo refresh
          setRefreshLatestHolo(prev => !prev);
          console.log('Holo completed successfully!');
        }}
      />
    </div>
  );
}
