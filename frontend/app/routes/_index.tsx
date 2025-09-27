import { useAuth } from "../context/authContext";

export default function Index() {
  const { user } = useAuth();
  
  // Extract first name from displayName
  const firstName = user?.displayName?.split(' ')[0];
  
  return <h1>Hello, {firstName}!</h1>;
}