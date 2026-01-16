interface AIResponseMessageProps {
  name: string;
  image: string;
  message: string;
  date: string;
}

const AIResponseMessage = ({
  name,
  image,
  message,
  date,
}: AIResponseMessageProps) => {
  // Formatowanie daty (bez zmian)
  const formatedDate = new Date(date);
  const day = String(formatedDate.getDate()).padStart(2, "0");
  const monthNum = String(formatedDate.getMonth() + 1).padStart(2, "0");
  const dateString = `${day}.${monthNum}`;

  const hour = String(formatedDate.getHours()).padStart(2, "0");
  const minute = String(formatedDate.getMinutes()).padStart(2, "0");
  const timeString = `${hour}:${minute}`;

  const polygonShape = "polygon(12% 39%, 93% 43%, 100% 100%, 0% 100%)";

  return (
    <div className="w-full mb-4">
      <p className="text-right">
        {dateString} {timeString}
      </p>

      <div className="flex items-start gap-4">
        <div className="relative -mt-12 ml-3 w-36 h-36">
          <div
            className="absolute inset-0 bg-secondary-dark translate-x-2 translate-y-2 z-0"
            style={{ clipPath: polygonShape }}
          />

          <div
            className="relative xl:w-36 w-24 h-full  z-10 bg-white"
            style={{ clipPath: polygonShape }}
          >
            <img
              src={image}
              alt={name}
              className="w-full h-full object-cover scale-110 translate-y-12"
            />
          </div>
        </div>
        <div className="relative">
          <div className="w-full bg-secondary-dark p-6">
            <p className="xl:text-3xl text-xl text-primary">{message}</p>
          </div>

          <div className="absolute top-0 -left-5 w-0 h-0 border-t-0 border-t-transparent border-b-30 border-b-transparent border-r-20 border-r-secondary-dark" />
        </div>
      </div>
    </div>
  );
};

export default AIResponseMessage;
