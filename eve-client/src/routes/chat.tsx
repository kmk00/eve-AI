import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/chat")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div className="h-screen flex flex-col xl:flex-row">
      {/* AI Model */}
      <div className="bg-red-200 w-full h-full"></div>
      {/* Chat */}
      <div className="bg-secondary-light w-full h-full bg-cover bg-center relative after:bg-[url('/chat-bg.svg')] after:bg-cover after:bg-center after:bg-no-repeat after:w-full after:h-full after:z-10 overflow-x-hidden telative">
        <div className="relative z-10 text-4xl flex justify-center items-center mt-4">
          <select>
            <option>Chat title 1</option>
            <option>Chat title 2</option>
            <option>Chat title 3</option>
          </select>
        </div>
        <div className="absolute z-0 top-0 left-0 w-full h-full ">
          <img
            src="/chat-bg.svg"
            alt="chat-bg"
            className="w-full h-full object-cover object-bottom-left"
          />
        </div>
      </div>
    </div>
  );
}
