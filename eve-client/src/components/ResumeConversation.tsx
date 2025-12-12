const ResumeConversation = () => {
  const ai_name = "EVE";
  const ai_image = "/character_image.png";

  return (
    <div className="xl:-mt-14 group relative xl:w-120 md:w-100 md:h-100 w-80 h-80 xl:h-120 rounded-full">
      <button
        onClick={() => {}}
        className="xl:w-120 md:w-100 md:h-100 w-80 h-80 rounded-full xl:h-120  relative"
      >
        <div
          className={`xl:w-120 md:w-100 md:h-100 w-80 h-80 xl:h-120  bg-[url('${ai_image}')] bg-center bg-cover bg-no-repeat rounded-full`}
        ></div>

        <div className="xl:w-120 md:w-100 md:h-100 w-80 h-80 xl:h-120 top-0 left-0 absolute group-hover:bg-secondary-dark/40 bg-secondary-dark/0 transition-colors duration-200 rounded-full flex items-end justify-start md:pb-10 pl-10 pb-14 ">
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
