interface UserMessageProps {
  message: string;
}

const UserMessage = ({ message }: UserMessageProps) => {
  return (
    <div className="relative">
      <div className="w-full bg-primary ">
        <p className="xl:text-3xl text-xl text-secondary-dark px-3 py-2">
          {message}
        </p>
      </div>

      <div
        className="absolute top-0 -right-2 xl:-right-5
                   w-0 h-0 
                   border-t-0 border-t-transparent
                   border-b-30 border-b-transparent
                   border-l-20 border-primary"
      />
    </div>
  );
};

export default UserMessage;
