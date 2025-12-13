import AddNewCharacter from "@/components/AddNewCharacter";
import CharacterListButton from "@/components/CharacterListButton";
import CharacterMenuElement from "@/components/CharacterMenuElement";
import ConfigSettings from "@/components/ConfigSettings";
import CurrentDate from "@/components/CurrentDate";
import ResumeConversation from "@/components/ResumeConversation";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: App,
});

function App() {
  return (
    <>
      <div className="h-screen relative xl:overflow-y-hidden overflow-x-hidden">
        <CurrentDate />
        <ConfigSettings />
        <div className="flex flex-col gap-12 items-center justify-center">
          <ResumeConversation />
          <div className="xl:hidden block">
            <CharacterListButton />
          </div>
        </div>
        <div className="hidden xl:block absolute right-6 top-[20%] transform-y-[50%]">
          <div className="flex flex-col items-end gap-4 mb-16">
            <CharacterMenuElement name="Eleven" />
            <CharacterMenuElement name="Riko" />
            <CharacterMenuElement name="Eve" />
          </div>
          <CharacterListButton />
        </div>
        <div className="hidden xl:block">
          <AddNewCharacter />
        </div>
        <div className="flex xl:hidden flex-col items-end gap-4 mt-12 mb-8 px-4">
          <CharacterMenuElement name="Eleven" />
          <CharacterMenuElement name="Riko" />
          <CharacterMenuElement name="Eve" />
        </div>
        <div className="xl:hidden flex flex-col items-center mt-20 ">
          <AddNewCharacter />
        </div>
        <img
          src="/circle-b.svg"
          className="hidden xl:block m-auto xl:absolute xl:-bottom-4 left-[50%] translate-x-[-50%] "
        ></img>
      </div>
    </>
  );
}
