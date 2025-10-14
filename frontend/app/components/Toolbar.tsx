import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router";
import { signOut } from "firebase/auth";
import { auth } from "../lib/firebase";
import { useAuth } from "../context/authContext";
import { LoadingSpinner } from "./LoadingSpinner";
import logo from "../../public/logo.svg";

type ToolbarProps = {
  onCreate?: () => void; 
  onSearch: (query: string) => void;
};

export function Toolbar({ onCreate, onSearch }: ToolbarProps) {
  const [query, setQuery] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement | null>(null);
  const navigate = useNavigate();
  const { user, loading } = useAuth();
  const photoUrl =
    user?.photoURL ||
    user?.providerData[0]?.photoURL ||
    undefined;



  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      if (!menuRef.current) return;
      if (!menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, []);

  async function handleLogout() {
    try {
      await signOut(auth);
      navigate("/");
    } catch (err) {
      console.error("Failed to sign out", err);
    }
  }

  function getUserName() {
    const firstName = user?.displayName?.split(" ")[0];
    return firstName;
  }

  return (
    <div className="relative z-[9999] flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between rounded-xl border border-gray-200 dark:border-gray-800 bg-white/60 dark:bg-gray-900/60 backdrop-blur p-4">
      <div className="flex items-center gap-3 text-lg font-semibold tracking-tight">
        <Link to="/" className="hover:translate-x-1 transition-transform duration-300">
          <img src={logo} alt="Journal" className="w-10 h-10" />
        </Link>
        {loading ? (
          <LoadingSpinner label="Loading..." size={16} />
        ) : (
          <span><span className="font-bold">{getUserName()}'s</span> Journal</span>
        )}
      </div>
      <div className="flex w-full sm:w-auto items-center gap-4">
        <div className="relative flex-1 sm:flex-initial">
          <input
            value={query}
            onChange={(e) => {
              const v = e.target.value;
              setQuery(v);
              onSearch(v);
            }}
            placeholder="Search entries..."
            className="w-full sm:w-72 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-700"
          />
          <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">⌘K</div>
        </div>
        <button
          onClick={() => navigate("/new-entry")}
          className="inline-flex items-center justify-center whitespace-nowrap rounded-lg bg-gray-900 text-white dark:bg-white dark:text-gray-900 px-3 py-2 text-sm font-medium shadow-sm hover:opacity-90 active:opacity-80"
        >
          New Entry
        </button>
        <div className="relative flex items-center justify-center" ref={menuRef}>
          <button
            aria-label="Account menu"
            onClick={() => setMenuOpen((o) => !o)}
            className="inline-flex items-center justify-center w-9 h-9 rounded-full  bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            {photoUrl ? (
              <img src={photoUrl} alt={user?.displayName || "Account"} className="w-9 h-9 rounded-full object-cover" />
            ) : (
              <svg viewBox="0 0 24 24" className="w-5 h-5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M20 21a8 8 0 0 0-16 0" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            )}
          </button>
          {menuOpen && (
            <div className="absolute right-0 top-10 mt-5 w-56 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shadow-lg p-2 z-[10000]">
              <div className="px-3 py-2 text-sm text-gray-600 dark:text-gray-300">
                {user?.displayName || user?.email || "Signed in"}
              </div>
              <button
                onClick={() => {
                  setMenuOpen(false);
                  navigate("/settings");
                }}
                className="w-full text-left px-3 py-2 text-sm rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                Settings
              </button>
              <div className="my-1 border-t border-gray-200 dark:border-gray-800" />
              <button
                onClick={handleLogout}
                className="w-full text-left px-3 py-2 text-sm rounded-md text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
              >
                Log out
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


