import { fetchWithAuth } from "./auth";

const RAW_API_BASE = (import.meta as any).env?.VITE_API_BASE_URL || "http://localhost:5001";
const API_BASE = RAW_API_BASE.replace(/\/$/, "");
const BASE_URL = `${API_BASE}/entries`;

export interface Entry {
  entry_id: string;
  user_id: string;
  title: string;
  content: string;
  entry_date: string;
  created_at: string;
  updated_at: string;
  deleted_at?: string;
}

export async function getEntries() {
  const res = await fetchWithAuth(BASE_URL);
  return res.json();
}

export async function createEntry(entry: {
  entry_date: string; // ISO string (new Date().toISOString())
  title: string;
  content: string;
}) {
  const res = await fetchWithAuth(BASE_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(entry),
  });
  return res.json();
}

export async function updateEntry(entry_id: string, entry: {
  title: string;
  content: string;
}) {
  const res = await fetchWithAuth(`${BASE_URL}/${entry_id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(entry),
  });
  return res.json();
}

export async function deleteEntry(entry_id: string) { // Deleted_at is set in the backend
  const res = await fetchWithAuth(`${BASE_URL}/${entry_id}`, {
    method: "DELETE",
  });
  return res.json();
}