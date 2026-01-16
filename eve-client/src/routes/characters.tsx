import { getCharacters } from "@/api/characters";
import CharactersList from "@/components/CharactersList";
import SelectedCharacterDetails from "@/components/SelectedCharacterDetails";
import type { Character } from "@/types";
import { useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";

const charactersQueryOptions = {
  queryKey: ["characters"],
  queryFn: () => getCharacters(),
};

export const Route = createFileRoute("/characters")({
  component: RouteComponent,
  loader: () => charactersQueryOptions,
});

function RouteComponent() {
  const characterListQuery = useSuspenseQuery(charactersQueryOptions);
  const characters = characterListQuery.data;
  const [selectedCharacter, setSelectedCharacter] = useState<Character>(
    characters[0]
  );

  const handleClick = (id: number) => {
    const character = characters.find((c) => c.id === id);
    if (character) {
      setSelectedCharacter(character);
    }
  };

  // TODO! Change image

  return (
    <div className="xl:h-screen relative flex flex-col overflow-hidden">
      <div className="absolute z-10 -top-20 -right-20 content-['fdsa'] w-220 2xl:w-300 2xl:h-300 h-220 bg-[url('/character_image.png')] after:bg-secondary after:w-220 after:2xl:w-300 after:2xl:h-300 after:h-220 after:z-10 after:absolute after:top-0 after:right-0 after:rounded-full after:opacity-40 bg-cover bg-center rounded-full before:xl:w-80 before:xl:h-80 before:h-50 before:w-50 before:bg-primary before:opacity-100 before:z-20 before:absolute before:top-0 before:right-0 before:rounded-full"></div>
      <div className="flex flex-col-reverse xl:flex-row justify-between items-start gap-12 mt-4 mb-8 px-4 relative z-50">
        <CharactersList onClick={handleClick} characters={characters} />
        <SelectedCharacterDetails character={selectedCharacter} />
      </div>
      {/* <div className="xl:block hidden absolute xl:bottom-4 xl:right-4 bottom-0 right-0 pb-8 z-50">
        <div className="relative">
          <img
            src="/settings.svg"
            alt="settings"
            className="w-14 h-14 md:w-20 md:h-20 relative z-10"
          />
          <div className=" w-60 h-60 md:w-60 md:h-60 top-[50%] right-[50%] xl:bottom-0 xl:right-0 translate-x-[50%] translate-y-[-50%] rounded-full bg-secondary-dark absolute"></div>
        </div>
      </div> */}
    </div>
  );
}
