import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/_index.tsx"),           // maps to "/"
  route("/auth/login", "routes/login.tsx"), // maps to "/login"
  route("/auth/signup", "routes/signup.tsx"), // maps to "/signup"
  route("/home", "routes/home.tsx"), // maps to "/home"
] satisfies RouteConfig;
