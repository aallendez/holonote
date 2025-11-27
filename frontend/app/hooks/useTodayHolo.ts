import { useAuthenticatedApi } from "./useAuthenticatedApi";
import { getHoloDaily, type HoloDaily } from "../api/holos";

/**
 * Custom hook for checking if there's a holo for today
 */
export function useTodayHolo() {
  const today = new Date().toISOString().split("T")[0];

  return useAuthenticatedApi<HoloDaily | null>(
    () => getHoloDaily(today),
    [today], // Re-run when date changes
  );
}
