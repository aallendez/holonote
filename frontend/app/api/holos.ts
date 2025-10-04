import { fetchWithAuth } from "./auth";

const RAW_API_BASE = (import.meta as any).env?.VITE_API_BASE_URL || "http://localhost:5001";
const API_BASE_URL = RAW_API_BASE.replace(/\/$/, "");

export interface HoloConfig {
  holo_id: string;
  user_id: string;
  questions: string[];
}

export interface HoloDaily {
  holo_daily_id: string;
  holo_id: string;
  entry_date: string;
  score: number;
  answers: Record<string, boolean>;
}

export interface HoloDailyCreate {
  entry_date: string;
  score: number;
  answers: Record<string, boolean>;
}

export interface AvgScoreResponse {
  avg_score: number | null;
}

// Get holo config for current user
export async function getHoloConfig(): Promise<HoloConfig> {
  console.log('🌐 getHoloConfig: Starting...');
  console.log('🌐 getHoloConfig: URL:', `${API_BASE_URL}/holos/holo`);
  
  const response = await fetchWithAuth(`${API_BASE_URL}/holos/holo`);
  console.log('🌐 getHoloConfig: Response status:', response.status);

  if (!response.ok) {
    if (response.status === 404) {
      console.log('🌐 getHoloConfig: 404 - No config found');
      throw new Error('No holo configuration found');
    }
    const errorText = await response.text();
    console.error('🌐 getHoloConfig: Error response:', errorText);
    throw new Error(`Failed to fetch holo config: ${response.status} ${response.statusText} - ${errorText}`);
  }

  const result = await response.json();
  console.log('🌐 getHoloConfig: Success:', result);
  return result;
}

// Create holo config for current user
export async function createHoloConfig(questions: string[]): Promise<HoloConfig> {
  const response = await fetchWithAuth(`${API_BASE_URL}/holos/holo`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ questions }),
  });

  if (!response.ok) {
    throw new Error(`Failed to create holo config: ${response.statusText}`);
  }

  return response.json();
}

// Get holo daily by date
export async function getHoloDaily(entryDate: string): Promise<HoloDaily | null> {
  const response = await fetchWithAuth(`${API_BASE_URL}/holos/daily?entry_date=${entryDate}`);

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`Failed to fetch holo daily: ${response.statusText}`);
  }

  return response.json();
}

// Get latest holo daily
export async function getLatestHoloDaily(): Promise<HoloDaily | null> {
  const response = await fetchWithAuth(`${API_BASE_URL}/holos/daily/latest`);

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`Failed to fetch latest holo daily: ${response.statusText}`);
  }

  return response.json();
}

// Create holo daily
export async function createHoloDaily(holoDaily: HoloDailyCreate): Promise<HoloDaily> {
  const response = await fetchWithAuth(`${API_BASE_URL}/holos/daily`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(holoDaily),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to create holo daily: ${response.status} ${response.statusText} - ${errorText}`);
  }

  return response.json();
}

// Get average score
export async function getAvgScore(): Promise<AvgScoreResponse> {
  const response = await fetchWithAuth(`${API_BASE_URL}/holos/avg-score`);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to fetch average score: ${response.status} ${response.statusText} - ${errorText}`);
  }

  return response.json();
}
