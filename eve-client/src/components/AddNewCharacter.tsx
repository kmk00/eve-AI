const AddNewCharacter = () => {
  // TODO : ADD animations

  return (
    <button
      onClick={() => {}}
      className="xl:absolute bottom-28 left-6 md:bottom-14 md:left-10 xl:bottom-28 xl:left-14"
    >
      <div className="relative">
        {/* TEXT */}
        <div className="relative xl:text-5xl md:text-4xl text-3xl text-secondary-dark -rotate-12 z-10">
          ADD NEW
        </div>

        {/* Triangle */}
        <div className="absolute z-0 -top-2 left-4 md:top-0 md:left-0 xl:-top-6 xl:left-2 inline-block w-0 h-0 border-solid rotate-290 border-t-0 border-r-100 border-b-100 xl:border-r-171 md:border-r-120 border-l-0 xl:border-b-171 md:border-b-120 border-l-transparent border-r-secondary/80 border-t-transparent border-b-transparent"></div>

        {/* Circle */}

        <div className=" absolute -z-10 w-20 h-20 md:w-24 md:h-24 xl:w-32 xl:h-32 xl:-top-10 xl:right-4 md:-top-6 md:right-2 -top-4 right-0 rounded-full bg-transparent border-2 border-secondary-dark"></div>
      </div>
    </button>
  );
};

export default AddNewCharacter;
