import CharacterElement from "./CharacterElement";

const CharactersList = () => {
  return (
    <div className="flex flex-col gap-16 py-20 xl:pr-20 pr-4 sm:w-2/3 w-full xl:w-fit xl:max-h-screen m-auto mt-14 xl:mt-4 max-h-[50vh] overflow-y-auto overflow-x-hidden cyber-scrollbar md">
      {Array.from({ length: 10 }).map((_, index) => (
        <CharacterElement
          index={index}
          key={index}
          name="Eleven"
          trait="Sarcastic"
          messagesNumber={5}
          lastMessageDate="28.07.2023"
          avatar="/character_image.png"
        />
      ))}
    </div>
  );
};

export default CharactersList;
