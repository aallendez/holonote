type StatsProps = {
  totalEntries: number;
  currentStreak: number;
  bestStreak: number;
  avgScore: number;
};

export function Stats({ totalEntries, currentStreak, bestStreak, avgScore }: StatsProps) {
  const items = [
    { label: "Total Entries", value: totalEntries },
    { label: "Current Streak", value: currentStreak },
    { label: "Best Streak", value: bestStreak },
    { label: "Avg. Score", value: "N/A" },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
      {items.map((it) => (
        <div
          key={it.label}
          className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white/60 dark:bg-gray-900/60 backdrop-blur p-4"
        >
          <div className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">
            {it.label}
          </div>
          <div className="mt-2 text-2xl font-semibold">{it.value}</div>
        </div>
      ))}
    </div>
  );
}


