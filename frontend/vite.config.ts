import { reactRouter } from "@react-router/dev/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [tailwindcss(), reactRouter(), tsconfigPaths()],
  ssr: {
    noExternal: ["firebase"],
  },
  test: {
    environment: "happy-dom",
    globals: true,
    setupFiles: [],
    include: ["app/**/*.test.{ts,tsx}"],
  },
});
