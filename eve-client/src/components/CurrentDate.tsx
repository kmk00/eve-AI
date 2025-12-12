import { useEffect, useState } from "react";

const CurrentDate = () => {
  const [date, setDate] = useState(new Date());

  useEffect(() => {
    // Aktualizuj datę co minutę (aby obsłużyć zmianę dnia bez odświeżania strony)
    const timer = setInterval(() => setDate(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  const day = String(date.getDate()).padStart(2, "0");
  const monthNum = String(date.getMonth() + 1).padStart(2, "0");
  const dateString = `${day}.${monthNum}`;

  const monthName = date
    .toLocaleString("en-US", { month: "short" })
    .toUpperCase();

  return (
    <div>
      <div className="translate flex flex-col pl-6 pt-6 relative">
        <p className="relative z-10 text-secondary-dark w-fit text-6xl md:text-8xl xl:text-9xl tracking-tighter">
          {dateString}
        </p>
        <p className="relative z-10 text-secondary text-4xl md:6xl xl:text-7xl w-fit -mt-3 md:-mt-5">
          {monthName}
        </p>
        <div className="bg-primary rounded-full w-100 h-100 md:w-150 md:h-150 xl:w-200 xl:h-200 absolute top-0 left-0 translate-x-[-50%] translate-y-[-50%]"></div>
      </div>
    </div>
  );
};

export default CurrentDate;
