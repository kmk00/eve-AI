interface CharacterElementProps {
  index: number;
  name: string;
  trait: string;
  messagesNumber: number;
  lastMessageDate: string;
  avatar: string;
}

const CharacterElement = ({
  name,
  trait,
  messagesNumber,
  lastMessageDate,
  avatar,
  index,
}: CharacterElementProps) => {
  const margin = () => {
    switch (index % 6) {
      case 0:
        return "20px";
      case 1:
        return "40px";
      case 2:
        return "60px";
      case 3:
        return "40px";
      case 4:
        return "20px";
    }
  };

  return (
    <div
      style={{ marginLeft: margin() }}
      className={`bg-secondary-dark text-primary w-120 p-1`}
    >
      <div className="flex justify-between">
        <div className="w-36 h-20 relative">
          <img
            src={avatar}
            alt={name}
            className="w-36 h-36 -mt-12 ml-3 object-cover border-4 border-secondary-dark"
          />
        </div>
        <div className="flex justify-between flex-1 ml-3">
          <p className="text-8xl -mb-4">{messagesNumber}</p>
          <div className="flex flex-col justify-between">
            <p className="text-right">{lastMessageDate}</p>
            <p className="text-4xl">{trait}</p>
          </div>
        </div>
      </div>
      <p className="bg-primary text-secondary-dark text-center p-1 text-2xl mx-1 mb-1">
        {name}
      </p>
    </div>
  );
};

export default CharacterElement;
