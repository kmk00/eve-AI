import AddNewCharacter from "@/components/AddNewCharacter";
import CharacterListButton from "@/components/CharacterListButton";
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
      <CurrentDate />
      <ConfigSettings />
      <div className="flex flex-col gap-12 items-center justify-center">
        <ResumeConversation />
        <div className="xl:hidden block">
          <CharacterListButton />
        </div>
      </div>
      <div className="hidden xl:block absolute right-6 top-[50%] transform-y-[50%]">
        <CharacterListButton />
      </div>
      <AddNewCharacter />
      <div className="absolute bottom-0 left-[50%] translate-x-[-50%] translate-y-[95%] w-400 h-400 bg-secondary-dark rounded-full"></div>
    </div>
  );
}
