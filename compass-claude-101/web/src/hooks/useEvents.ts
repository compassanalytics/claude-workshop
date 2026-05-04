import { useEffect, useState } from "react";

interface Event {
  id: number;
  name: string;
}

interface UseEventsResult {
  data: Event[] | undefined;
  isLoading: boolean;
  error: string | undefined;
}

interface UseEventsArgs {
  limit?: number;
  offset?: number;
}

export function useEvents({ limit = 50, offset = 0 }: UseEventsArgs = {}): UseEventsResult {
  const [data, setData] = useState<Event[] | undefined>();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | undefined>();

  useEffect(() => {
    let cancelled = false;
    async function run() {
      setIsLoading(true);
      try {
        const res = await fetch(`/api/events?limit=${limit}&offset=${offset}`);
        if (!res.ok) throw new Error("request_failed");
        const json = (await res.json()) as Event[];
        if (!cancelled) setData(json);
      } catch {
        if (!cancelled) setError("Could not load events");
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }
    void run();
    return () => {
      cancelled = true;
    };
  }, [limit, offset]);

  return { data, isLoading, error };
}
