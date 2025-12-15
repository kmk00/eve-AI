// ================= ENUMS =================

export enum AIMode {
  LOCAL = "local",
  REMOTE = "remote",
}

export enum MemoryRetensionPreference {
  SHORT_TERM = "short_term",
  LONG_TERM = "long_term",
}

export enum EmotionsFrequency {
  FREQUENTLY = "frequently",
  SOMETIMES = "sometimes",
  RARELY = "rarely",
  NEVER = "never",
}

export enum Emotion {
  // Default
  NEUTRAL = "neutral",
  CONTENT = "content",
  JOYFUL = "joyful",
  CURIOUS = "curious",
  PROTECTIVE = "protective",
  EXCITED = "excited",

  // Negative
  IRRITATED = "irritated",
  ANGRY = "angry",
  ANXIOUS = "anxious",
  EMBARRASSED = "embarrassed",
  DISAPPOINTED = "disappointed",
  SCARED = "scared",

  // Social
  SARCASTIC = "sarcastic",
  AFFECTIONATE = "affectionate",
  PLAYFUL = "playful",
  SMUG = "smug",
  VULNERABLE = "vulnerable",
  FLUSTERED = "flustered",

  // State
  TIRED = "tired",
  CONFUSED = "confused",
}

export interface UserProfilePayload {
  likes: string[];
  dislikes: string[];
  personality: string[];
}

export interface User {
  id: number;
  name: string;
  gender?: string;
  age?: number;

  /** Raw JSON string from DB */
  profile_json: string;

  created_at: string; // ISO Date
  updated_at: string; // ISO Date

  // Relationships
  conversations?: Conversation[];

  // Computed properties (if included in API response)
  profile?: UserProfilePayload;
  topics_user_likes?: string[];
  topics_user_dislikes?: string[];
  personality?: string[];
}

/**
 * Global configuration settings
 */
export interface Config {
  id: number;
  mode: AIMode | string;
  model_name: string;
  gpu_layers: number;
  temperature: number;
  max_tokens: number;
  openai_api_key?: string | null;
  anthropic_api_key?: string | null;
  conversation_memory_length: number;
  emotion_confidence_threshold: number;
  created_at: string; // ISO Date
  updated_at: string; // ISO Date
}

/**
 * Characters table
 */
export interface Character {
  // Main fields
  id: number;
  name: string;
  description: string;
  personality: string;
  avatar: string;
  model_image?: string;
  vrm_path: string;

  // World settings
  role_in_world?: string;
  world_context?: string;

  // Behavior settings
  speech_pattern?: string;
  /** Raw JSON string representing List<str> */
  favorite_phrases_json: string;
  sentence_length_preference?: string;
  response_length_default?: string | number; // Python definition implies int, but default is string "1-2 sentences" in code provided?
  ask_questions_frequency: number;
  emoticons_frequency: EmotionsFrequency | string;
  memory_retention_preference?: MemoryRetensionPreference | string;

  // Emotion settings
  default_emotion: Emotion | string;
  /** Raw JSON string representing List<Emotion> */
  enabled_emotions_json: string;

  // Voice settings
  voice_id?: string | null;
  speech_rate?: number | null;
  pitch?: number | null;

  // Status fields
  is_active: boolean;
  is_default: boolean;

  // Timestamps
  created_at: string; // ISO Date
  updated_at: string; // ISO Date
  last_interaction_at?: string | null; // ISO Date

  // Relationships
  conversations?: Conversation[];

  // Computed/Parsed (helpers for frontend usage)
  favorite_phrases?: string[];
  enabled_emotions?: Emotion[];
}

/**
 * Singular conversation session table
 */
export interface Conversation {
  id: number;
  character_id: number;
  character?: Character;

  user_id: number;
  user?: User;

  relationship_type: string;
  user_intent: string;
  world_state: string;

  // Conversation settings
  title?: string | null;
  message_count: number;
  is_active: boolean;

  // Timestamps
  created_at: string; // ISO Date
  updated_at: string; // ISO Date
  last_activity: string; // ISO Date

  // Relationships
  memory_notes?: MemoryNote[];
  messages?: Message[];
}

/**
 * Single message table
 */
export interface Message {
  id: number;
  conversation_id: number;
  // conversation?: Conversation; // Usually omitted in nested message lists to avoid circular depth

  role: "user" | "assistant" | "system" | string;
  content: string;
  language: string;

  // Emotions
  emotion?: Emotion | string | null;
  emotion_confidence?: number | null;
  emotion_intensity: number;

  // Meta
  generation_time_ms?: number | null;
  token_count?: number | null;
  created_at: string; // ISO Date

  // Relationships
  memory_note?: MemoryNote;

  // Computed
  full_emotion?: string;
}

/**
 * Important memory to be referenced later
 */
export interface MemoryNote {
  id: number;
  character_id: number;
  conversation_id: number;
  // conversation?: Conversation;

  content: string;
  source_message_id?: number | null;

  importance_score: number;
  created_at: string; // ISO Date

  message?: Message;
}
