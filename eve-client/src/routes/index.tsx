import CurrentDate from "@/components/CurrentDate";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: App,
});

function App() {
  return (
    <div className="md:max-h-screen relative">
      <CurrentDate />
    </div>
  );
}
