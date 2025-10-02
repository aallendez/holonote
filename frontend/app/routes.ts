import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/_index.tsx"),           // maps to "/"
  route("/auth/log-in", "routes/login.tsx"), // maps to "/login"
  route("/auth/sign-up", "routes/signup.tsx"), // maps to "/signup"
  route("/dashboard", "routes/dashboard.tsx"), // maps to "/dashboard"
  route("/new-entry", "routes/new-entry.tsx"), // maps to "/new-entry"
  route("/entries", "routes/entries.tsx"), // maps to "/entries"
] satisfies RouteConfig;
