import ConfigSettings from "@/components/ConfigSettings";
import CurrentDate from "@/components/CurrentDate";
import ResumeConversation from "@/components/ResumeConversation";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: App,
});

function App() {
  return (
    <div className="md:max-h-screen h-screen relative overflow-hidden">
      {/* <div> */}
      <CurrentDate />
      <ConfigSettings />
      {/* </div> */}
      <div className="flex items-center justify-center">
        <ResumeConversation />
      </div>
    </div>
  );
}
