import AIModelWrapper from "@/components/AIModelWrapper";
import AIResponseMessage from "@/components/AIResponseMessage";
import UserMessage from "@/components/UserMessage";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/chat")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div className="h-screen flex flex-col xl:flex-row">
      {/* AI Model */}
      <AIModelWrapper />
      {/* Chat */}
      <div className="bg-secondary-light w-full h-full pb-8 bg-cover bg-center relative after:bg-[url('/chat-bg.svg')] after:bg-cover after:bg-center after:bg-no-repeat after:w-full after:h-full after:z-10 overflow-x-hidden overflow-hidden telative">
        <div className="relative z-10 text-4xl flex justify-center items-center mt-4">
          <select>
            <option>Chat title 1</option>
          </select>
        </div>
        <div className="relative overflow-y-auto overflow-x-hidden z-50 pb-10 pr-8 cyber-scrollbar xl:w-5/6 h-3/4 mx-auto px-4">
          {/* Messages */}
        </div>
        <div className="flex relative xl:mt-40 mt-4 z-50 px-10">
          <form className="relative w-full">
            <div className="" />
            <input
              className="w-full h-20 bg-primary px-2 py-2 border-secondary-dark border-4  focus:outline-none shadow-[0px_15px_0px_-5px_#04233b]"
              type="text"
              placeholder="Type your message.."
            />
          </form>
          <div className="flex flex-col gap-4 mx-10 ">
            <button
              className={`text-primary  font-expose font-black  text-4xl uppercase relative z-10 text-stroke-dark
        after:absolute after:left-[50%] after:bottom-0 after:-translate-x-[50%] after:translate-y-[5%] after:-z-10 after:h-[1em] after:w-[3em] after:bg-secondary-dark after:rotate-6 after:[clip-path:polygon(0%_0%,_100%_15%,_90%_100%,_10%_85%)]
        `}
            >
              Send
            </button>
            <button className="bg-primary text-secondary-dark px-2 py-2 border-secondary-dark border-t-4 border-b-4 border-r-4 focus:outline-none">
              Clear
            </button>
          </div>
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
