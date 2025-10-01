import type { Entry } from "../api/entries";

type LatestEntriesProps = {
  entries: Entry[];
};

export function LatestEntries({ entries }: LatestEntriesProps) {
  const latest = [...entries]
    .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
    .slice(0, 5);

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white/60 dark:bg-gray-900/60 backdrop-blur p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold tracking-tight">Latest Entries</h3>
        <a href="/entries" className="text-xs text-gray-600 dark:text-gray-300 group group-hover:underline mr-2">See all entries <p className="inline-block ml-1 transition-transform -rotate-45 group-hover:translate-x-1 group-hover:-translate-y-1">→</p></a>
      </div>
      <div className="mt-3 overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 dark:text-gray-400">
              <th className="py-2 pr-4 font-medium">Title</th>
              <th className="py-2 pr-4 font-medium">Date</th>
              <th className="py-2 pr-4 font-medium">Score</th>
              <th className="py-2 pl-2"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
            {latest.length === 0 && (
              <tr>
                <td colSpan={4} className="py-3 text-gray-500 dark:text-gray-400">No entries yet.</td>
              </tr>
            )}
            {latest.map((e) => (
              <tr
                key={e.id}
                className="group hover:bg-gray-50/60 dark:hover:bg-gray-900/60 transition-colors cursor-pointer"
                onClick={() => { window.location.href = `/entries?entry=${encodeURIComponent(e.id)}`; }}
              >
                <td className="py-3 pr-4 font-medium truncate max-w-[280px] text-gray-900 dark:text-gray-100">{e.title}</td>
                <td className="py-3 pr-4 whitespace-nowrap text-gray-600 dark:text-gray-300">{new Date(e.createdAt).toLocaleDateString()}</td>
                <td className="py-3 pr-4">
                  <span className="inline-flex items-center rounded-md border border-emerald-200/60 dark:border-emerald-800/60 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-0.5 text-[11px] font-medium text-emerald-700 dark:text-emerald-300">
                    {e.score}
                  </span>
                </td>
                <td className="py-3 pl-2 text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 group-hover:translate-x-1 transition-transform">→</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}


