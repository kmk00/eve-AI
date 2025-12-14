interface CharTraitProps {
  name: string;
  index: number;
}

const CharTrait = ({ name, index }: CharTraitProps) => {
  return (
    <div
      className={`relative px-2 text-center w-fit ml-auto z-60 text-secondary-dark text-3xl 2xl:text-4xl after:2xl:h-12 before:2xl:h-12 before:content-[''] before:w-full before:h-8  before:absolute before:top-[70%] before:left-[50%] before:-translate-x-[50%] before:-z-10 before:-translate-y-[50%]  before:bg-primary
      after:content-[''] after:w-full after:h-8  after:absolute after:top-[80%] after:left-[50%] after:-translate-x-[50%] after:-z-20 after:-translate-y-[50%] after: after:bg-secondary-dark after:rotate-5 text-stroke-3
      
      ${index % 2 === 0 ? "mt-8" : ""}`}
      key={index}
    >
      {name}
    </div>
  );
};

export default CharTrait;
