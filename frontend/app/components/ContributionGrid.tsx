import type { Entry } from "../api/entries";

type ContributionGridProps = {
  entries: Entry[];
  mode?: "week" | "month" | "year" | "all";
  weeks?: number; // used when mode is undefined
  cellSize?: number; // px size of each day cell
};

function getDateKey(d: Date) {
  return d.toISOString().slice(0, 10);
}

export function ContributionGrid({ entries, mode = "year", weeks = 30, cellSize = 12 }: ContributionGridProps) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  let start = new Date(today);
  let end = new Date(today);

  if (mode === "year") {
    start = new Date(today.getFullYear(), 0, 1);
    end = new Date(today.getFullYear(), 11, 31);
    const startDay = start.getDay();
    start.setDate(start.getDate() - startDay);
  } else if (mode === "all") {
    // Span from earliest to latest entry
    const dates = entries.map((e) => new Date(e.createdAt)).sort((a, b) => a.getTime() - b.getTime());
    if (dates.length) {
      start = new Date(dates[0]);
      end = new Date(dates[dates.length - 1]);
    }
    start.setHours(0, 0, 0, 0);
    end.setHours(0, 0, 0, 0);
    const startDay = start.getDay();
    start.setDate(start.getDate() - startDay);
  } else if (mode === "month") {
    start = new Date(today.getFullYear(), today.getMonth(), 1);
    end = new Date(today.getFullYear(), today.getMonth() + 1, 0);
  } else if (mode === "week") {
    start = new Date(today);
    start.setDate(today.getDate() - 6);
    end = new Date(today);
  } else {
    // fallback rolling window
    start = new Date(today);
    start.setDate(today.getDate() - weeks * 7 + 1);
    end = new Date(today);
  }

  const counts = new Map<string, number>();
  for (const e of entries) {
    const d = new Date(e.createdAt);
    d.setHours(0, 0, 0, 0);
    const key = getDateKey(d);
    counts.set(key, (counts.get(key) || 0) + 1);
  }

  const days: { date: Date; count: number }[] = [];
  const cursor = new Date(start);
  while (cursor <= end) {
    const key = getDateKey(cursor);
    days.push({ date: new Date(cursor), count: counts.get(key) || 0 });
    cursor.setDate(cursor.getDate() + 1);
  }

  const columns: { date: Date; count: number }[][] = [];
  if (mode === "week") {
    // Single row of 7 days
    columns.push(days.slice(Math.max(0, days.length - 7)));
  } else {
    for (let i = 0; i < days.length; i += 7) {
      columns.push(days.slice(i, i + 7));
    }
  }

  function intensity(count: number) {
    if (count === 0) return "bg-gray-100 dark:bg-gray-800";
    if (count === 1) return "bg-emerald-200 dark:bg-emerald-900";
    if (count === 2) return "bg-emerald-300 dark:bg-emerald-800";
    if (count === 3) return "bg-emerald-400 dark:bg-emerald-700";
    return "bg-emerald-500 dark:bg-emerald-600";
  }

  // Month and year labels/boundaries
  const monthLabels: string[] = [];
  const monthStarts: boolean[] = [];
  const yearLabels: string[] = [];
  const yearStarts: boolean[] = [];
  for (let i = 0; i < columns.length; i++) {
    const firstDay = columns[i][0]?.date;
    const prevLast = i > 0 ? columns[i - 1][columns[i - 1].length - 1]?.date : null;
    const isMonthStart = !prevLast || (firstDay && prevLast && firstDay.getMonth() !== prevLast.getMonth());
    const isYearStart = !prevLast || (firstDay && prevLast && firstDay.getFullYear() !== prevLast.getFullYear());
    monthStarts.push(!!isMonthStart);
    yearStarts.push(!!isYearStart);
    // Show month labels every 3 months only in year mode
    const showMonthLabel = mode === "year" && isMonthStart && firstDay && firstDay.getMonth() % 3 === 0;
    monthLabels.push(showMonthLabel && firstDay ? firstDay.toLocaleString(undefined, { month: "short" }) : "");
    // Year labels for all-time mode
    yearLabels.push(isYearStart && firstDay ? String(firstDay.getFullYear()) : "");
  }

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white/60 dark:bg-gray-900/60 backdrop-blur p-4">
      <div className="text-sm font-semibold mb-3">{mode === 'year' ? `Activity ${today.getFullYear()}` : (mode === 'all' ? 'Activity (All time)' : 'Activity')}</div>
      <div className="flex items-start gap-2 overflow-x-auto">
        {(mode === "year" || mode === "all") && (
          <div className="flex flex-col gap-1 text-[10px] leading-none text-gray-500 dark:text-gray-400 select-none" style={{ marginTop: Math.max(0, (cellSize - 12) / 2) }}>
            {['S','M','T','W','T','F','S'].map((d) => (
              <div key={d} className="flex items-center justify-center" style={{ width: cellSize, height: cellSize }}>{d}</div>
            ))}
          </div>
        )}
        <div className="flex flex-col">
          {mode === "year" && (
            <div className="flex gap-1 mb-1 text-[10px] text-gray-500 dark:text-gray-400 select-none">
              {columns.map((_, i) => (
                <div key={i} style={{ width: cellSize, height: cellSize }}>
                  {monthLabels[i]}
                </div>
              ))}
            </div>
          )}
          {mode === "all" && (
            <div className="flex gap-1 mb-1 text-[10px] text-gray-500 dark:text-gray-400 select-none">
              {columns.map((_, i) => (
                <div key={i} style={{ width: cellSize, height: cellSize }}>
                  {yearLabels[i]}
                </div>
              ))}
            </div>
          )}
          {mode === "week" ? (
            <div className="flex gap-1">
              {columns[0]?.map((d, j) => (
                <div key={j} className="flex flex-col items-center gap-1">
                  <div title={`${d.count} entries on ${d.date.toDateString()}`} className={`rounded ${intensity(d.count)}`} style={{ width: cellSize, height: cellSize }} />
                  <div className="text-[10px] text-gray-500 dark:text-gray-400 select-none" style={{ width: cellSize, height: 12 }}>
                    {"SMTWTFS"[d.date.getDay()]}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex gap-1">
              {columns.map((col, i) => (
                <div
                  key={i}
                  className={`flex flex-col gap-1 ${(mode === 'year') && monthStarts[i] ? 'border-l border-gray-200 dark:border-gray-800' : ''}`}
                  title={(mode === 'year') && monthStarts[i] && col[0] ? col[0].date.toLocaleString(undefined, { month: 'long' }) : undefined}
                >
                  {col.map((d, j) => (
                    <div
                      key={j}
                      title={`${d.count} entries on ${d.date.toDateString()}`}
                      className={`rounded ${intensity(d.count)}`}
                      style={{ width: cellSize, height: cellSize }}
                    />
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <div className="mt-3 text-xs text-gray-500 dark:text-gray-400 flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded bg-gray-100 dark:bg-gray-800" />
          <span>Empty</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded bg-emerald-500 dark:bg-emerald-600" />
          <span>Entry made</span>
        </div>
      </div>
    </div>
  );
}


