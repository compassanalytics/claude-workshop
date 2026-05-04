import { useState } from "react";

interface LoginInput {
  email: string;
  password: string;
}

interface UseAuthResult {
  user: { id: string } | undefined;
  isLoading: boolean;
  error: string | undefined;
  login: (input: LoginInput) => Promise<boolean>;
  logout: () => void;
}

export function useAuth(): UseAuthResult {
  const [user, setUser] = useState<{ id: string } | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();

  async function login(input: LoginInput): Promise<boolean> {
    setIsLoading(true);
    setError(undefined);
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      });
      if (!res.ok) {
        setError("Invalid email or password");
        return false;
      }
      const json = (await res.json()) as { access_token: string };
      const sub = JSON.parse(atob(json.access_token.split(".")[1])).sub as string;
      setUser({ id: sub });
      return true;
    } catch {
      setError("Could not reach server");
      return false;
    } finally {
      setIsLoading(false);
    }
  }

  function logout() {
    setUser(undefined);
  }

  return { user, isLoading, error, login, logout };
}
