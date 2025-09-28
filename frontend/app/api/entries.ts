
const BASE_URL = "http://localhost:5001/api/entries";

export interface Entry {
  id: string;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
}

export async function getEntries() {
  const res = await fetch(BASE_URL);
  return res.json();
}

export async function createEntry(entry: {
    user_id: string;
    entry_date: string; // ISO string (new Date().toISOString())
    title: string;
    content: string;
    score: number;
  }) {
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entry),
    });
    return res.json();
}

export async function updateEntry(id: string, entry: {
    title: string;
    content: string;
    score: number;
  }) {
    const res = await fetch(`${BASE_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entry),
    });
    return res.json();
}

export async function deleteEntry(id: string) { // Deleted_at is set in the backend
    const res = await fetch(`${BASE_URL}/${id}`, {
      method: "DELETE",
    });
    return res.json();
  }