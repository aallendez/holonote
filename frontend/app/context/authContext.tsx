import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { onAuthStateChanged, type User } from "firebase/auth";
let authClient: import("firebase/auth").Auth | undefined;
if (typeof window !== "undefined") {
  // Lazy import to avoid initializing Firebase during SSR
  const { auth } = await import("../lib/firebase");
  authClient = auth;
}

type AuthContextType = {
  user: User | null;
  loading: boolean;
};

const AuthContext = createContext<AuthContextType>({ user: null, loading: true });

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authClient) {
      // SSR or no window - mark as not loading but unauthenticated
      setLoading(false);
      return;
    }
    const unsub = onAuthStateChanged(authClient, (u) => {
      setUser(u);
      setLoading(false);
    });
    return unsub;
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
