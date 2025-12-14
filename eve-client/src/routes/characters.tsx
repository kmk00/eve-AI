import CharactersList from "@/components/CharactersList";
import CharTrait from "@/components/CharTrait";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/characters")({
  component: RouteComponent,
});

function RouteComponent() {
  const desc = "A sarcastic but caring with a sharp wit";
  const name = "Eve";
  const arr = [
    "Affectionate",
    "playful",
    "smug",
    "Affectionate",
    "playful",
    "smug",
  ];

  return (
    <div className="h-screen relative flex flex-col overflow-hidden">
      <div className="absolute z-10 -top-20 -right-20 content-['fdsa'] w-220 h-220 bg-[url('/character_image.png')] after:bg-secondary after:w-220 after:h-220 after:z-10 after:absolute after:top-0 after:right-0 after:rounded-full after:opacity-40 bg-cover bg-center rounded-full before:w-80 before:h-80 before:bg-primary before:opacity-100 before:z-20 before:absolute before:top-0 before:right-0 before:rounded-full"></div>
      <div className="flex justify-between items-start gap-12 mt-4 mb-8 px-4 relative z-50">
        <CharactersList />
        <div className="flex items-center">
          <div className="grid grid-cols-2 h-fit gap-8 items-center rotate-8">
            {arr.map((item, index) => (
              <CharTrait name={item} index={index} />
            ))}
          </div>
          <div className="flex flex-col justify-end gap-4">
            <div className="flex ml-auto">
              <p className="text-vertical text-9xl text-secondary-dark">
                {name}
              </p>
              <div className="w-60 h-100 bg-red-400"></div>
            </div>
            <p className="text-6xl text-primary text-right max-w-md">{desc}</p>
          </div>
        </div>
      </div>
      <div className="absolute bottom-4 right-4 md:bottom-0 md:right-0 pb-8 z-50">
        <div className="relative">
          <img
            src="/settings.svg"
            alt="settings"
            className="w-14 h-14 md:w-20 md:h-20 relative z-10"
          />
          <div className=" w-60 h-60 md:w-60 md:h-60 top-[50%] right-[50%] translate-x-[50%] translate-y-[-50%] rounded-full bg-secondary-dark absolute"></div>
        </div>
      </div>
    </div>
  );
}
