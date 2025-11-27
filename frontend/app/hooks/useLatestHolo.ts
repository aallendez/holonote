import { useAuthenticatedApi } from "./useAuthenticatedApi";
import { getLatestHoloDaily, type HoloDaily } from "../api/holos";

/**
 * Custom hook for fetching the latest holo with authentication handling
 */
export function useLatestHolo(refreshTrigger?: boolean) {
  return useAuthenticatedApi<HoloDaily | null>(
    () => getLatestHoloDaily(),
    [refreshTrigger],
  );
}
