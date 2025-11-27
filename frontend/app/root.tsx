import {
  isRouteErrorResponse,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "react-router";

import type { Route } from "./+types/root";
import "./app.css";

import React from "react";
import { AuthProvider } from "./context/authContext";
import { Footer } from "./components/Footer";

// Defensive wrapper: avoid crashing if framework context isn't ready yet on first load
class SafeHead extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch() {
    // Intentionally swallow head render errors on first client boot.
  }

  render() {
    if (this.state.hasError) return null;
    return this.props.children as React.ReactElement;
  }
}

export const links: Route.LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <SafeHead>
          <>
            <Meta />
            <Links />
          </>
        </SafeHead>
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
        <Footer />
      </body>
    </html>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Outlet />
    </AuthProvider>
  );
}

// Rendered while the client hydrates; avoids route tree hooks running before framework context exists
export function HydrateFallback() {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100dvh",
      }}
    >
      <span>Loading…</span>
    </div>
  );
}

// Intentionally not exporting a root ErrorBoundary to avoid framework hooks executing
// before the router context is established on the first client load in dev.
