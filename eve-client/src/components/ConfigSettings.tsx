const ConfigSettings = () => {
  return (
    <div className="absolute top-4 right-4 md:top-6 md:right-6 pb-8">
      <div className="relative">
        <img
          src="/settings.svg"
          alt="settings"
          className="w-14 h-14 md:w-20 md:h-20 relative z-10"
        />
        <div className=" w-60 h-60 md:w-80 md:h-80 top-0 right-0 translate-x-[55%] translate-y-[-55%] rounded-full bg-secondary-dark absolute"></div>
      </div>
    </div>
  );
};

export default ConfigSettings;
