import CharactersList from "@/components/CharactersList";
import CharTrait from "@/components/CharTrait";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/characters")({
  component: RouteComponent,
});

function RouteComponent() {
  const desc = "A sarcastic but caring with a sharp wit";
  const name = "Avangarda";
  const arr = [
    "Affectionate",
    "playful",
    "smug",
    "Affectionate",
    "playful",
    "smug",
  ];

  return (
    <div className="xl:h-screen relative flex flex-col overflow-hidden">
      <div className="absolute z-10 -top-20 -right-20 content-['fdsa'] w-220 2xl:w-300 2xl:h-300 h-220 bg-[url('/character_image.png')] after:bg-secondary after:w-220 after:2xl:w-300 after:2xl:h-300 after:h-220 after:z-10 after:absolute after:top-0 after:right-0 after:rounded-full after:opacity-40 bg-cover bg-center rounded-full before:xl:w-80 before:xl:h-80 before:h-50 before:w-50 before:bg-primary before:opacity-100 before:z-20 before:absolute before:top-0 before:right-0 before:rounded-full"></div>
      <div className="flex flex-col-reverse xl:flex-row justify-between items-start gap-12 mt-4 mb-8 px-4 relative z-50">
        <CharactersList />
        <div className="relative flex xl:flex flex-col-reverse w-full xl:w-auto xl:flex-row xl:items-center">
          <div className="flex flex-col h-fit gap-8 2xl:gap-14 items-center justify-end rotate-8 -mt-8 xl:mt-0 mr-4">
            {arr.map((item, index) => (
              <CharTrait name={item} index={index} />
            ))}
          </div>
          <div className="flex flex-col justify-end gap-4">
            <div className="flex ml-auto">
              <p className="xl:text-vertical text-6xl 2xl:text-[5rem] text-secondary-dark text-left">
                {name}
              </p>
              <div className="xl:block hidden w-60 h-100 2xl:w-80 2xl:h-120 bg-red-400"></div>
            </div>
            <p className="text-6xl 2xl:text-8xl text-primary ml-auto  xl:mt-2 text-right max-w-md 2xl:max-w-2xl">
              {desc}
            </p>
          </div>
          <div className="xl:hidden absolute bottom-0 left-0 flex items-center justify-center after:xl:w-80 after:w-40 after:h-40 after:z-0 after:bg-secondary-dark after:opacity-100  after:absolute after:top-[50%] after:right-[50%] after:translate-x-[50%] after:translate-y-[-50%] after:rounded-full">
            <img
              src="/settings.svg"
              alt="settings"
              className="w-20 h-20 relative z-10"
            />
          </div>
        </div>
      </div>
      <div className="xl:block hidden absolute xl:bottom-4 xl:right-4 bottom-0 right-0 pb-8 z-50">
        <div className="relative">
          <img
            src="/settings.svg"
            alt="settings"
            className="w-14 h-14 md:w-20 md:h-20 relative z-10"
          />
          <div className=" w-60 h-60 md:w-60 md:h-60 top-[50%] right-[50%] xl:bottom-0 xl:right-0 translate-x-[50%] translate-y-[-50%] rounded-full bg-secondary-dark absolute"></div>
        </div>
      </div>
    </div>
  );
}
