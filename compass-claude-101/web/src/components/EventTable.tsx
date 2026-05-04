import { useEvents } from "../hooks/useEvents";

interface EventTableProps {
  limit?: number;
}

export function EventTable({ limit = 50 }: EventTableProps) {
  const { data, isLoading, error } = useEvents({ limit });

  if (isLoading) return <p className="text-gray-500">Loading…</p>;
  if (error) return <p className="text-red-600">Could not load events</p>;
  if (!data?.length) return <p className="text-gray-500">No events yet</p>;

  return (
    <table className="w-full border-collapse">
      <thead className="bg-gray-100">
        <tr>
          <th className="text-left p-2">ID</th>
          <th className="text-left p-2">Name</th>
        </tr>
      </thead>
      <tbody>
        {data.map((evt) => (
          <tr key={evt.id} className="border-t">
            <td className="p-2">{evt.id}</td>
            <td className="p-2">{evt.name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
