import AddNewCharacter from "@/components/AddNewCharacter";
import CharacterListButton from "@/components/CharacterListButton";
import CharacterMenuElement from "@/components/CharacterMenuElement";
import ConfigSettings from "@/components/ConfigSettings";
import CurrentDate from "@/components/CurrentDate";
import ResumeConversation from "@/components/ResumeConversation";
import type { Character } from "@/types";
import { useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";

async function getCharacters(limit: number): Promise<Character[]> {
  const url = new URL("http://127.0.0.1:8000/api/v1/characters");
  url.searchParams.append("limit", limit.toString());

  const res = await fetch(url.toString(), {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch characters");
  }

  return res.json();
}

const charactersQueryOptions = {
  queryKey: ["characters"],
  queryFn: () => getCharacters(3),
};

export const Route = createFileRoute("/")({
  component: App,
  loader: ({ context: { queryClient } }) =>
    queryClient.ensureQueryData(charactersQueryOptions),
});

function App() {
  const charactersQuery = useSuspenseQuery(charactersQueryOptions);
  const characters = charactersQuery.data;

  console.log(characters);

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
            {characters?.map((character) => (
              <CharacterMenuElement
                key={character.id}
                name={character.name}
                id={character.id}
                avatar={character.avatar}
              />
            ))}
          </div>
          <CharacterListButton />
        </div>
        <div className="hidden xl:block">
          <AddNewCharacter />
        </div>
        <div className="flex xl:hidden flex-col items-end gap-4 mt-12 mb-8 px-4">
          {characters?.map((character) => (
            <CharacterMenuElement
              key={character.id}
              name={character.name}
              id={character.id}
              avatar={character.avatar}
            />
          ))}
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
