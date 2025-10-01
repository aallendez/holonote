import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { fetchWithAuth } from "./auth";

// Mock firebase auth module used inside auth.ts
vi.mock("../lib/firebase", () => {
  return {
    auth: {
      currentUser: null as any,
    },
  };
});

const { auth } = await import("../lib/firebase");

const originalFetch = global.fetch;

describe("fetchWithAuth", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch as any;
    (auth as any).currentUser = null;
    vi.restoreAllMocks();
  });

  it("throws if no user", async () => {
    await expect(fetchWithAuth("/x")).rejects.toThrow("Not authenticated");
  });

  it("adds bearer token and forwards options", async () => {
    (auth as any).currentUser = {
      getIdToken: vi.fn().mockResolvedValue("FAKE_TOKEN"),
    };

    (global.fetch as any).mockResolvedValueOnce({ ok: true });

    const options = { method: "POST", headers: { "X-Test": "1" } };
    await fetchWithAuth("/api/test", options);

    expect(global.fetch).toHaveBeenCalledWith("/api/test", {
      method: "POST",
      headers: { ...options.headers, Authorization: "Bearer FAKE_TOKEN" },
    });
  });
});


