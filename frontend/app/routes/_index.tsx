import { useEffect } from "react";
import { Navigate } from "react-router";
import { useAuth } from "../context/authContext";

export default function Index() {
  const { user, loading } = useAuth();
  if (loading) {
    return null;
  }
  if (user) return <Navigate to="/dashboard" replace />;
  return <Navigate to="/auth/log-in" replace />;
}