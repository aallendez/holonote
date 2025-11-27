import { useEffect, useState } from "react";
import { useAuth } from "../context/authContext";

/**
 * Custom hook for making authenticated API calls
 * Handles authentication state and provides a clean interface for components
 */
export function useAuthenticatedApi<T>(
  apiCall: () => Promise<T>,
  dependencies: any[] = [],
) {
  const { user, loading: authLoading } = useAuth();
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const execute = async () => {
    if (!user) {
      setData(null);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const result = await apiCall();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Unknown error"));
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading) {
      execute();
    }
  }, [authLoading, user, ...dependencies]);

  return {
    data,
    loading: authLoading || loading,
    error,
    refetch: execute,
    isAuthenticated: !!user,
  };
}
