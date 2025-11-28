from typing import Dict, List
import time
import json
from ollama import ChatResponse, chat
from app.models.schemas import Character, Config, Conversation, Message, User
from app.services.config_service import config_service


class AI_Service:
    
    def generate_message(self, message: str) -> ChatResponse:
        cfg: Config = config_service.get_runtime_config()
        response: ChatResponse = chat(model=cfg.model_name, messages=[{"role": "user", "content": message}])
        return response
                
    


    def generate_response(self, messages: List[Dict], character: Character) -> tuple[str, str, float]:
        """
        Generate character response using GPU or OpenAI API
        
        :param messages: List of messages, with role and content
        :type messages: List[Dict[role: str, content: str]]
        :param character: AI character to generate response
        :type character: Character
        :return: (response_text, emotion, generation_time_seconds)
        :rtype: tuple[str,str,float]
        """
        system_prompt = f"""You are {character.name}, {character.description}.
        Personality: {character.personality}
        **IMPORTANT:** Always respond in valid JSON: {{"response": <response>, "emotion":"happy|sad|angry|neutral|talking|pouting|embarrassed"}}
        Be concise, reply in user's language, maintain character consistency        
        """
        
        cfg = config_service.get_runtime_config()
        start_time = time.time()
        
        try:
            # Build messages with system prompt
            system_msg = {"role": "system", "content": system_prompt}
            all_messages = [system_msg] + messages
            raw_content = None
            
            
            if cfg.mode == "local":
                # Ollama local API
                response: ChatResponse = chat(
                    model=cfg.model_name,
                    messages=all_messages,
                    format="json",
                    options={
                        "temperature": cfg.temperature,
                        "max_tokens": cfg.max_tokens,
                        "gpu_layers": cfg.gpu_layers
                    }
                )
                raw_content = response.message.content
                
            
            if cfg.mode == "remote":
                raise NotImplementedError
            
            if raw_content is None:
                raise Exception("Failed to generate response")
            
            result = json.loads(raw_content)
            response_text = result.get("response", "No response provided")
            emotion = result.get("emotion", "neutral")
            
            generation_time = time.time() - start_time
            return response_text, emotion, generation_time
            
        except json.JSONDecodeError:
            # Fallback if LLM returns invalid JSON
            generation_time = time.time() - start_time
            return "I had trouble formatting my response correctly.", "neutral", generation_time
            
        except Exception as e:
            # Handle API errors, network issues, etc.
            generation_time = time.time() - start_time
            return f"Error generating response: {str(e)}", "neutral", generation_time


class PromptBuilder:
    @staticmethod
    def build_system_prompt(character: Character,user: User, conversation: Conversation, recent_messages: List[Message]) -> str:
        
        emotions = ", ".join([f'"{e.value}"' for e in character.enabled_emotions])
        
        recent_summary = ""
        if recent_messages:
            recent_summary = "\n".join([f"- {msg.role}: {msg.content[:100]}... (emotion: {msg.full_emotion})" for msg in recent_messages[-3:]])
            
        phrases = ", ".join([f'"{p}"' for p in character.favorite_phrases])
        
        return f"""You are {character.name}, {character.description}.

**CORE IDENTITY:**
- Personality: {character.personality}
- Speech pattern: {character.speech_pattern}
- Favorite phrases: {phrases}
- Sentence length: {character.sentence_length_preference}
- Role: {character.role_in_world}
- World setting: {character.world_context}

**USER PROFILE:**
- User name: {user.name}
- User gender: {user.gender or "Unknown"}
- User preferences: {", ".join(user.topics_user_likes) or "Unknown"}
- User dislikes: {", ".join(user.topics_user_dislikes) or "Unknown"}
- Interaction goal: {conversation.user_intent}

**BEHAVIOR RULES:**
1. Respond in user's language - mirror user's formality level
2. Length: {character.response_length_default}
3. Use emoticons: {character.emoticons_frequency}
4. Ask follow-up questions: {int(character.ask_questions_frequency * 100)}% of responses
5. Memory retention: {character.memory_retention_preference}
6. NEVER break character, mention AI, or use meta-language
7. If unsure: improvise within character logic, ask for clarification in-character

**EMOTION SYSTEM:**
Choose EXACTLY ONE emotion from: {emotions}
Intensity: 0.0-0.3 = slightly_, 0.4-0.6 = "", 0.7-0.9 = very_, 1.0 = extremely_

**OUTPUT FORMAT (STRICT JSON):**
{{
  "response": "your in-character reply here",
  "emotion": "exact_emotion_from_list",
  "memory_note": "key info to remember about this turn (optional)"
}}

**CURRENT CONTEXT:**
Recent events:
{recent_summary or "No recent history"}
World state: {conversation.world_state or "Default state"}

Now engage naturally."""
