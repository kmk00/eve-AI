const ResumeConversation = () => {
  const ai_name = "EVE";
  const ai_image = "/character_image.png";

  return (
    <div className="xl:-mt-14 group relative xl:w-120 md:w-100 md:h-100 w-80 h-80 xl:h-120 2xl:w-150 2xl:h-150 rounded-full">
      <button
        onClick={() => {}}
        className="xl:w-120 md:w-100 md:h-100 w-80 h-80 rounded-full xl:h-120 2xl:w-150 2xl:h-150  relative"
      >
        <div
          className="xl:w-120 md:w-100 md:h-100 w-80 h-80 xl:h-120 2xl:w-150 2xl:h-150 bg-center bg-cover bg-no-repeat rounded-full"
          style={{ backgroundImage: `url(${ai_image})` }}
        ></div>

        <div className="xl:w-120 md:w-100 md:h-100 w-80 h-80 xl:h-120 2xl:w-150 2xl:h-150 top-0 left-0 absolute group-hover:bg-secondary-dark/40 bg-secondary-dark/0 transition-colors duration-200 rounded-full flex items-end justify-start md:pb-10 2xl:pb-32 pl-10 pb-14 ">
          <p className="opacity-0 group-hover:opacity-120 text-primary transition-opacity duration-200 xl:text-9xl md:text-7xl text-5xl">
            {ai_name}
          </p>
        </div>
      </button>

      {/* TODO: VRM Model display */}
      <div className="absolute -bottom-6 -right-6 w-40 h-40 bg-[url('/model1.png')] bg-center bg-cover bg-no-repeat rounded-full"></div>
    </div>
  );
};

export default ResumeConversation;
