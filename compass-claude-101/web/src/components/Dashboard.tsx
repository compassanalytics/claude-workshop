import { EventTable } from "./EventTable";

export function Dashboard() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold mb-4">Events</h1>
      <EventTable />
    </div>
  );
}
