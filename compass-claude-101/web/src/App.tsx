import { Dashboard } from "./components/Dashboard";
import { LoginForm } from "./components/LoginForm";
import { useAuth } from "./hooks/useAuth";

export function App() {
  const { user } = useAuth();
  return (
    <div className="min-h-screen bg-gray-50">
      {user ? <Dashboard /> : <LoginForm />}
    </div>
  );
}
