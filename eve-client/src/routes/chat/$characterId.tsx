import { getSpecificCharacter } from "@/api/characters";
import AIChat from "@/components/AIChat";
import AIModelWrapper from "@/components/AIModelWrapper";
import { queryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";

const specificCharacterQueryOptions = (characterId: number) =>
  queryOptions({
    queryKey: ["specificCharacter", characterId],
    queryFn: () => getSpecificCharacter(characterId),
  });

export const Route = createFileRoute("/chat/$characterId")({
  component: RouteComponent,

  loader: ({ context: { queryClient }, params }) => {
    return queryClient.ensureQueryData(
      specificCharacterQueryOptions(Number(params.characterId))
    );
  },
});

function RouteComponent({}) {
  const { characterId } = Route.useParams();

  const { data: character } = useSuspenseQuery(
    specificCharacterQueryOptions(Number(characterId))
  );

  if (!character) {
    return <div>Character not found</div>;
  }

  return (
    <div className="h-screen flex flex-col xl:flex-row">
      {/* AI Model */}
      <AIModelWrapper />
      {/* Chat */}
      <AIChat characterId={characterId} />
    </div>
  );
}
