interface CharacterMenuElementProps {
  id: number;
  name: string;
  avatar: string;
}

const CharacterMenuElement = ({
  name,
  avatar,
  id,
}: CharacterMenuElementProps) => {
  // TODO: Change image
  const clipPath = () => {
    const randomShape = Math.floor(Math.random() * 4) + 1;

    switch (randomShape) {
      case 1:
        return "after:[clip-path:polygon(0%_0%,_100%_15%,_90%_100%,_10%_85%)]";
      case 2:
        return "after:[clip-path:polygon(10%_10%,_100%_0%,_85%_100%,_0%_90%)]";
      case 3:
        return "after:[clip-path:polygon(0%_5%,_95%_0%,_100%_85%,_15%_100%)]";
      case 4:
        return "after:[clip-path:polygon(5%_0%,_90%_10%,_100%_95%,_0%_100%)]";
    }
  };

  return (
    <button className="flex xl:w-fit xl:flex-col flex-row xl:items-end items-center justify-around xl:justify-start w-full">
      <p
        className={
          `text-secondary-dark font-expose xl:font-bold xl:ml-auto xl:text-xl text-4xl uppercase font-black relative z-10
        after:absolute after:left-[50%] after:bottom-0 after:-translate-x-[50%] after:translate-y-[5%] after:-z-10 after:xl:hidden
        after:h-[1em] after:w-[3em] after:bg-secondary after:rotate-6
        /* 2. Wycinamy kształt (x y) dla 4 punktów: Lewy-Góra, Prawy-Góra, Prawy-Dół, Lewy-Dół */
        ` + clipPath()
        }
      >
        {name}
      </p>
      <div
        style={{ backgroundImage: `url(${avatar})` }}
        className="-skew-x-12 shadow-[-10px_10px_0px_-2px_#04233b] hover:shadow-[-10px_10px_0px_-2px_#0caff7] transform duration-200 overflow-hidden w-40 h-40 transform-gpu"
      >
        <div className="w-full h-full skew-x-12 scale-125  bg-center bg-cover bg-no-repeat"></div>
      </div>
    </button>
  );
};

export default CharacterMenuElement;
