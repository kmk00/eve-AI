export const getConversations = async (characterId: string) => {
  const response = await fetch(
    `${import.meta.env.VITE_API_URL}/chat/${characterId}/conversations_list`
  );
  const data = await response.json();

  console.log(data);

  return data;
};
