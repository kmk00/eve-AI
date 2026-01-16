import type { Character } from "@/types";

async function getDefaultCharacter(): Promise<Character> {
  const url = new URL(`${import.meta.env.VITE_API_URL}/characters/default`);

  const res = await fetch(url.toString(), {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch default character");
  }

  return res.json();
}

async function getCharacters(limit?: number): Promise<Character[]> {
  const url = new URL(`${import.meta.env.VITE_API_URL}/characters`);
  if (limit) url.searchParams.append("limit", limit.toString());

  const res = await fetch(url.toString(), {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch characters");
  }

  return res.json();
}

async function getSpecificCharacter(id: number): Promise<Character> {
  const url = new URL(`${import.meta.env.VITE_API_URL}/characters/${id}`);

  const res = await fetch(url.toString(), {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch character");
  }

  return res.json();
}

export { getDefaultCharacter, getCharacters, getSpecificCharacter };
