interface CharacterMenuElementProps {
  name: string;
}

const CharacterMenuElement = ({
  name = "Character",
}: CharacterMenuElementProps) => {
  // TODO: ADD BACKROUND

  return (
    <button className="flex xl:w-fit xl:flex-col flex-row xl:items-end items-center justify-around xl:justify-start w-full">
      <p className="text-secondary-dark font-expose xl:font-bold xl:ml-auto xl:text-xl text-6xl uppercase font-black">
        {name}
      </p>
      <div className="-skew-x-12 shadow-[-10px_10px_0px_-2px_#04233b] hover:shadow-[-10px_10px_0px_-2px_#0caff7] transform duration-200 overflow-hidden w-40 h-40 transform-gpu">
        <div className="w-full h-full skew-x-12 scale-125 bg-[url('/model2.png')] bg-center bg-cover bg-no-repeat"></div>
      </div>
    </button>
  );
};

export default CharacterMenuElement;
