import React, { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
} from "firebase/auth";
import { auth, googleProvider } from "../lib/firebase";
import type { Route } from "./+types/login";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Login" },
    { name: "description", content: "Login to your account" },
  ];
}

const Login: React.FC = () => {
  const [user, setUser] = useState<any>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const navigate = useNavigate();

  // --- handlers ---
  async function handleGoogleLogin() {
    setErr(null);
    try {
      const result = await signInWithPopup(auth, googleProvider);
      setUser(result.user);
      navigate("/dashboard");
    } catch (e: any) {
      setErr(e.message);
    }
  }

  async function handleEmailSignIn(e: FormEvent) {
    e.preventDefault();
    setErr(null);
    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      setUser(result.user);
      navigate("/dashboard");
    } catch (e: any) {
      setErr(e.message);
    }
  }

  async function handleEmailSignUp() {
    setErr(null);
    try {
      const result = await createUserWithEmailAndPassword(auth, email, password);
      setUser(result.user);
      navigate("/dashboard");
    } catch (e: any) {
      setErr(e.message);
    }
  }

  return (
    <div className="min-h-[100dvh] grid place-items-center px-4">
      <div className="w-full max-w-md">
        <div className="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white/70 dark:bg-gray-900/50 backdrop-blur p-8 shadow-xl">
          <div className="w-full flex items-center justify-center mb-6">
            <img src="/holonote-t.png" alt="HoloNote" className="h-16 w-16 rounded" />
          </div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-2xl font-semibold tracking-tight">
              Welcome to HoloNote
            </h1>
          </div>

          <p className="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
            Sign in to continue and sync your notes securely across devices.
          </p>

          {/* Google login */}
          <button
            onClick={handleGoogleLogin}
            className="group relative inline-flex w-full items-center justify-center gap-3 rounded-lg bg-gray-900 text-white dark:bg-white dark:text-gray-900 px-5 py-3 font-medium transition-colors hover:bg-gray-800 dark:hover:bg-gray-100"
          >
            <span className="absolute inset-0 -z-10 rounded-lg bg-gradient-to-r from-indigo-500/20 via-fuchsia-500/20 to-emerald-500/20 blur-md opacity-0 group-hover:opacity-100 transition-opacity" />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              className="h-5 w-5"
            >
              <path
                fill="#EA4335"
                d="M12 10.2v3.7h5.3c-.2 1.2-1.6 3.6-5.3 3.6-3.2 0-5.8-2.6-5.8-5.8S8.8 6 12 6c1.8 0 3 .8 3.7 1.5l2.5-2.4C16.9 3.7 14.7 2.8 12 2.8 6.9 2.8 2.8 6.9 2.8 12S6.9 21.2 12 21.2c6 0 9.9-4.2 9.9-10 0-.7-.1-1.1-.2-1.6H12z"
              />
            </svg>
            Continue with Google
          </button>

          {/* Email/password form */}
          <form onSubmit={handleEmailSignIn} className="mt-6 space-y-3">
            <input
              type="email"
              placeholder="Email"
              className="w-full rounded-lg border border-gray-300 dark:border-gray-700 px-4 py-2"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full rounded-lg border border-gray-300 dark:border-gray-700 px-4 py-2"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              type="submit"
              className="w-full rounded-lg bg-indigo-600 text-white px-4 py-2 font-medium hover:bg-indigo-700"
            >
              Sign in
            </button>
          </form>

          <Link
            to="/auth/sign-up"
            className="mt-3 block w-full rounded-lg bg-gray-200 dark:bg-gray-700 px-4 py-2 text-center font-medium hover:bg-gray-300 dark:hover:bg-gray-600"
          >
            Create account
          </Link>

          {/* Display signed-in user */}
          {user && (
            <div className="mt-6 rounded-lg border border-gray-200 dark:border-gray-800 p-4 text-sm">
              <div className="font-medium">Signed in as</div>
              <div className="mt-1 text-gray-600 dark:text-gray-300 truncate">
                {user.email}
              </div>
            </div>
          )}

          {/* Errors */}
          {err && (
            <p className="mt-4 text-sm text-red-500 dark:text-red-400">{err}</p>
          )}

          <div className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
            By continuing you agree to our
            <a href="#" className="mx-1 underline underline-offset-4">
              Terms
            </a>
            and
            <a href="#" className="ml-1 underline underline-offset-4">
              Privacy Policy
            </a>
            .
          </div>
        </div>

      </div>
    </div>
  );
};

export default Login;
