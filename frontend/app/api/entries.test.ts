import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { getEntries, createEntry, updateEntry, deleteEntry } from "./entries";

const originalFetch = global.fetch;
const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL || "http://localhost:5001";
const BASE_URL = `${API_BASE}/api/entries`;

describe("entries API", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch as any;
    vi.restoreAllMocks();
  });

  it("getEntries calls GET and returns json", async () => {
    const mockJson = [{ id: "1" }];
    (global.fetch as any).mockResolvedValueOnce({ json: () => Promise.resolve(mockJson) });

    const result = await getEntries();

    expect(global.fetch).toHaveBeenCalledWith(BASE_URL);
    expect(result).toEqual(mockJson);
  });

  it("createEntry posts and returns json", async () => {
    const payload = {
      user_id: "u1",
      entry_date: new Date().toISOString(),
      title: "t",
      content: "c",
      score: 5,
    };
    const mockJson = { id: "123", ...payload };
    (global.fetch as any).mockResolvedValueOnce({ json: () => Promise.resolve(mockJson) });

    const result = await createEntry(payload);

    expect(global.fetch).toHaveBeenCalledWith(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    expect(result).toEqual(mockJson);
  });

  it("updateEntry puts and returns json", async () => {
    const id = "abc";
    const payload = { title: "t2", content: "c2", score: 3 };
    const mockJson = { id, ...payload };
    (global.fetch as any).mockResolvedValueOnce({ json: () => Promise.resolve(mockJson) });

    const result = await updateEntry(id, payload);

    expect(global.fetch).toHaveBeenCalledWith(`${BASE_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    expect(result).toEqual(mockJson);
  });

  it("deleteEntry deletes and returns json", async () => {
    const id = "del1";
    const mockJson = { success: true };
    (global.fetch as any).mockResolvedValueOnce({ json: () => Promise.resolve(mockJson) });

    const result = await deleteEntry(id);

    expect(global.fetch).toHaveBeenCalledWith(`${BASE_URL}/${id}`, {
      method: "DELETE",
    });
    expect(result).toEqual(mockJson);
  });
});


