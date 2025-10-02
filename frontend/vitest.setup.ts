import { vi } from 'vitest';

// Mock Firebase configuration for tests
const mockFirebaseConfig = {
  apiKey: "test-api-key",
  authDomain: "test-project.firebaseapp.com",
  projectId: "test-project",
  storageBucket: "test-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "test-app-id",
  measurementId: "test-measurement-id",
};

// Mock Firebase auth
const mockAuth = {
  currentUser: {
    getIdToken: vi.fn().mockResolvedValue("mock-token"),
  },
};

// Mock Firebase app
const mockApp = {};

// Mock Firebase modules
vi.mock('firebase/app', () => ({
  initializeApp: vi.fn().mockReturnValue(mockApp),
  getApp: vi.fn().mockReturnValue(mockApp),
  getApps: vi.fn().mockReturnValue([]),
}));

vi.mock('firebase/auth', () => ({
  getAuth: vi.fn().mockReturnValue(mockAuth),
  GoogleAuthProvider: vi.fn().mockImplementation(() => ({})),
}));

vi.mock('firebase/analytics', () => ({
  getAnalytics: vi.fn().mockReturnValue({}),
  isSupported: vi.fn().mockResolvedValue(false),
}));

// Mock environment variables
Object.defineProperty(import.meta, 'env', {
  value: {
    VITE_FIREBASE_API_KEY: mockFirebaseConfig.apiKey,
    VITE_FIREBASE_AUTH_DOMAIN: mockFirebaseConfig.authDomain,
    VITE_FIREBASE_PROJECT_ID: mockFirebaseConfig.projectId,
    VITE_FIREBASE_STORAGE_BUCKET: mockFirebaseConfig.storageBucket,
    VITE_FIREBASE_MSG_SENDER_ID: mockFirebaseConfig.messagingSenderId,
    VITE_FIREBASE_APP_ID: mockFirebaseConfig.appId,
    VITE_FIREBASE_MEASUREMENT_ID: mockFirebaseConfig.measurementId,
    VITE_API_BASE_URL: "http://localhost:5001",
  },
  writable: true,
});
