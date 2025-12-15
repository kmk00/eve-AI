import type { Character } from "@/types";
import CharTrait from "./CharTrait";

interface SelectedCharacterDetailsProps {
  character: Character;
}

const SelectedCharacterDetails = ({
  character,
}: SelectedCharacterDetailsProps) => {
  console.log(character);
  return (
    <div className="relative flex xl:flex flex-col-reverse w-full xl:w-auto xl:flex-row xl:items-center">
      <div className="flex flex-col h-fit gap-8 2xl:gap-14 items-center justify-end rotate-8 -mt-8 xl:mt-0 mr-4">
        {character.enabled_emotions?.map((item, index) => (
          <CharTrait key={index} name={item} index={index} />
        ))}
      </div>
      <div className="flex flex-col justify-end gap-4">
        <div className="flex ml-auto">
          <p className="xl:text-vertical text-6xl 2xl:text-[5rem] text-secondary-dark text-left">
            {character.name}
          </p>
          <div className="xl:block hidden w-60 h-100 2xl:w-80 2xl:h-120 bg-red-400"></div>
        </div>
        <p className="text-6xl 2xl:text-7xl text-primary ml-auto  xl:mt-2 text-right max-w-md 2xl:max-w-2xl">
          {character.description}
        </p>
      </div>
      {/* <div className="xl:hidden absolute bottom-0 left-0 flex items-center justify-center after:xl:w-80 after:w-40 after:h-40 after:z-0 after:bg-secondary-dark after:opacity-100  after:absolute after:top-[50%] after:right-[50%] after:translate-x-[50%] after:translate-y-[-50%] after:rounded-full">
        <img
          src="/settings.svg"
          alt="settings"
          className="w-20 h-20 relative z-10"
        />
      </div> */}
    </div>
  );
};

export default SelectedCharacterDetails;
