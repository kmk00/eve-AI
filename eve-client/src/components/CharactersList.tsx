interface CharactersListProps {
  characters: Character[];
  onClick: (index: number) => void;
}

import type { Character } from "@/types";
import CharacterElement from "./CharacterElement";

const CharactersList = ({ characters, onClick }: CharactersListProps) => {
  return (
    <div className="flex flex-col gap-16 py-20 xl:pr-20 pr-4 sm:w-2/3 w-full xl:w-fit xl:max-h-screen m-auto mt-14 xl:mt-4 max-h-[50vh] overflow-y-auto overflow-x-hidden cyber-scrollbar md">
      {characters.map((item) => (
        <CharacterElement
          onClick={onClick}
          index={item.id}
          key={item.id}
          name={item.name}
          trait={item.personality}
          // messagesNumber={item.messagesNumber}
          lastMessageDate={item.last_interaction_at}
          avatar={item.avatar}
        />
      ))}
    </div>
  );
};

export default CharactersList;
