import CharacterElement from "./CharacterElement";
// Ensure you import your CSS file here if it's not global
// import "./scrollbar.css";

const CharactersList = () => {
  return (
    <div className="flex flex-col gap-16 py-20 pr-20 xl:max-h-screen overflow-y-auto cyber-scrollbar ">
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
