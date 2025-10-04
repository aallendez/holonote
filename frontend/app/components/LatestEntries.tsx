import type { Entry } from "../api/entries";
import { LoadingSpinner } from "./LoadingSpinner";
import { useNavigate } from "react-router";

type LatestEntriesProps = {
  entries: Entry[];
  loading?: boolean;
};

export function LatestEntries({ entries, loading = false }: LatestEntriesProps) {
  const navigate = useNavigate();
  const latest = [...entries]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white/60 dark:bg-gray-900/60 backdrop-blur p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold tracking-tight">Latest Entries</h3>
        <button onClick={() => navigate("/dashboard")} className="text-xs cursor-not-allowed text-gray-600 dark:text-gray-300 group hover:underline mr-2">See all entries (coming soon...) <p className="inline-block ml-1 transition-transform -rotate-45 group-hover:translate-x-1 group-hover:-translate-y-1">→</p></button>
      </div>
      <div className="mt-3 overflow-x-auto min-h-[120px] flex items-center justify-center">
        {loading ? (
          <LoadingSpinner label="Loading entries..." />
        ) : (
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 dark:text-gray-400">
              <th className="py-2 pr-4 font-medium">Title</th>
              <th className="py-2 pr-4 font-medium">Date</th>
              <th className="py-2 pl-2"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
            {latest.length === 0 && (
              <tr>
                <td colSpan={3} className="py-3 text-gray-500 dark:text-gray-400">No entries yet.</td>
              </tr>
            )}
            {latest.map((e) => (
              <tr
                key={e.entry_id}
                className="group hover:bg-gray-50/60 dark:hover:bg-gray-900/60 transition-colors cursor-pointer"
                onClick={() => navigate(`/entries?entry=${encodeURIComponent(e.entry_id)}`)}
              >
                <td className="py-3 pr-4 font-medium truncate max-w-[280px] text-gray-900 dark:text-gray-100">{e.title}</td>
                <td className="py-3 pr-4 whitespace-nowrap text-gray-600 dark:text-gray-300">{new Date(e.created_at).toLocaleDateString()}</td>
                <td className="py-3 pl-2 text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 group-hover:translate-x-1 transition-transform">→</td>
              </tr>
            ))}
          </tbody>
        </table>
        )}
      </div>
    </div>
  );
}


