import AIVRMModel from "./AIVRMModel";

const AIModelWrapper = () => {
  return (
    <div className="w-full h-full relative">
      <AIVRMModel />
      <button className="xl:block hidden absolute xl:bottom-4 xl:left-4 bottom-0 right-0 pb-8 z-50">
        <img
          src="/settings.svg"
          alt="settings"
          className="w-14 h-14 md:w-20 md:h-20 relative z-10"
        />
      </button>
      <button className="absolute top-4 left-4">
        <img src="/arrow.svg" alt="AI Model" className="w-full h-full" />
      </button>
    </div>
  );
};

export default AIModelWrapper;
