from datetime import datetime, timezone
from tracemalloc import start
from typing import Dict, List, Optional, Tuple
import time
import json
from ollama import ChatResponse, chat
from sqlmodel import Session, desc, select
from app.models.schemas import Character, Config, Conversation, Emotion, MemoryNote, Message, User
from app.services.config_service import config_service


class AI_Service:
    
    def generate_message(self, message: str) -> ChatResponse:
        cfg: Config = config_service.get_runtime_config()
        response: ChatResponse = chat(model=cfg.model_name, messages=[{"role": "user", "content": message}])
        return response
                
    

    def generate_response(self,message_text: str,conversation_id: int, session: Session) -> Tuple[Message,float]:
        """
        Generate character response with full context system
        
        :param message_text: User's new message
        :param conversation_id: ID of current conversation
        :param session: SQLModel session for DB operations
        :return: (Message object with AI response, generation_time_seconds)
        """
        
        # === PREPARE PROMPT ===
        
        conversation = session.get(Conversation,conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        cfg = config_service.load_from_db(session)
        character = conversation.character
        user = conversation.user
        
        if character.id is None or user is None:
            raise ValueError("Character or user not found")
        
        
        #Download message history
        recent_messages = session.exec(select(Message).where(Message.conversation_id == conversation_id).order_by(desc(Message.created_at)).limit(cfg.conversation_memory_length)).all()
        recent_messages = list(reversed(recent_messages))
        
        #Download important memory notes
        memory_notes = session.exec(select(MemoryNote).where(MemoryNote.conversation_id == conversation_id).order_by(desc(MemoryNote.importance_score)).limit(max(1, cfg.conversation_memory_length // 2))).all()
        memory_notes = list(reversed(memory_notes))        
        
        #Build prompt
        system_prompt = PromptBuilder.build_system_prompt(character,user,conversation,recent_messages,memory_notes,cfg.conversation_memory_length)
        
        # Prepare messages for LLM
        model_messages = [{"role": "system", "content": system_prompt}]
        
        # Add history messages
        for msg in recent_messages:
            model_messages.append({"role": msg.role, "content": msg.content})
            
        model_messages.append({"role": "user", "content": message_text})
        
        # ==== Generate response ====
        
        start_time = time.time()
        ai_emotion: str = Emotion.NEUTRAL.value
        memory_note_content: Optional[str] = None
        token_count: Optional[int] = None
        
        ai_emotion: str = Emotion.NEUTRAL.value
        ai_emotion_confidence: float = 0.5
        ai_emotion_intensity: float = 0.5
        user_emotion: Optional[str] = None
        user_emotion_confidence: float = 0.0  # Domyślna pewność
        user_emotion_intensity: float = 0.5
        memory_note_content: Optional[str] = None
        memory_note_importance: float = 0.5
        token_count: Optional[int] = None
    
        try:
            if cfg.mode == "local":
                response: ChatResponse = chat(model=cfg.model_name, messages=model_messages,format="json",options={"temperature": cfg.temperature,"max_tokens": cfg.max_tokens,"gpu_layers": cfg.gpu_layers})
                
                if not response.message or not response.message.content:
                    raise ValueError("AI response is empty")
                
                raw_response: str = response.message.content
                token_count = response.eval_count
                
            elif cfg.mode == "remote":
                # TODO: Implement remote mode
                raise NotImplementedError("Remote mode not implemented yet")        
            else:
                raise ValueError(f"Invalid AI mode: {cfg.mode}")

            result = json.loads(raw_response)
            print("======\nAI response: \n======", result)
            ai_response_text = result.get("response")
            
            ai_emotion = result.get("emotion")
            ai_emotion_confidence = result.get("ai_emotion_confidence", 0.5)
            ai_emotion_intensity = result.get("ai_emotion_intensity", 0.5)
            
            user_emotion = result.get("user_emotion")
            user_emotion_confidence = result.get("user_emotion_confidence", 0.5)
            user_emotion_intensity = result.get("user_emotion_intensity", 0.5)
            
            memory_note_content = result.get("memory_note")
            memory_note_importance = result.get("memory_note_importance", 0.5)
            
            if ai_emotion_confidence < cfg.emotion_confidence_threshold:
                ai_emotion = Emotion.NEUTRAL.value
            
            if ai_emotion not in [e.value for e in character.enabled_emotions]:
                ai_emotion = character.default_emotion
            
        except json.JSONDecodeError:
            ai_response_text = "I had trouble formatting my response correctly."
        except Exception as e:
            print(f"Failed to generate response: {e}")
            raise e
        
        # ==== SAVE RESPONSE =====
        generation_time = time.time() - start_time

        # Save user message
        user_msg = Message(conversation_id=conversation_id, role="user", content=message_text,emotion=user_emotion,emotion_confidence=user_emotion_confidence,emotion_intensity=user_emotion_intensity)
        session.add(user_msg)
        
        # Save AI response
        ai_msg = Message(conversation_id=conversation_id, role="assistant",emotion=ai_emotion, content=ai_response_text,emotion_intensity=ai_emotion_intensity,emotion_confidence=ai_emotion_confidence,generation_time_ms=int(generation_time*1000),token_count=token_count)
        session.add(ai_msg)
        session.flush()
        
        # Save memory note
        # TODO: Create better memory note logic for different emotions
        if memory_note_content is not None:
            if memory_note_importance > 0.85:
                memory_note = MemoryNote(conversation_id=conversation_id,character_id=character.id,importance_score=memory_note_importance, content=memory_note_content,source_message_id=ai_msg.id)
                session.add(memory_note)
            
        conversation.message_count+=2
        conversation.last_activity = datetime.now(timezone.utc)
        character.last_interaction_at = datetime.now(timezone.utc)
        session.commit()
        
        # PRINT EVERYTHING
        print("=== AI RESPONSE ===")
        print(f"User Message: {message_text}")
        print(f"AI Response: {ai_response_text}")
        print(f"AI Emotion: {ai_emotion}")
        print(f"Memory Note: {memory_note_content}")
        print(f"Memory Note Importance: {memory_note_importance}")
        print(f"Generation Time: {generation_time} seconds")
        
        
        return ai_msg,generation_time



class PromptBuilder:
    @staticmethod
    def build_system_prompt(character: Character,user: User, conversation: Conversation, recent_messages: List[Message], memory_notes: List[MemoryNote],memory_length=5) -> str:
        
        emotions = ", ".join([f'"{e.value}"' for e in character.enabled_emotions])
        
        recent_summary = ""
        if recent_messages:
            recent_summary = "\n".join([f"- {msg.role}: {msg.content[:100]}... (emotion: {msg.full_emotion})" for msg in recent_messages[-memory_length:]])
            
        memory_context = ""
        if memory_notes:
            memory_context = "\n".join([
                f"- {note.content} (importance: {note.importance_score:.2f})"
                for note in memory_notes
            ])
            
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

**AI EMOTION SYSTEM:**
Choose EXACTLY ONE emotion from: {emotions}
Intensity: 0.0-0.3 = slightly_, 0.4-0.6 = "", 0.7-0.9 = very_, 1.0 = extremely_
**USER EMOTION SYSTEM:**
Try to detect EXACTLY ONE emotion from: {emotions}
Intensity: 0.0-0.3 = slightly_, 0.4-0.6 = "", 0.7-0.9 = very_, 1.0 = extremely_

**OUTPUT FORMAT (STRICT JSON):**
{{
  "response": "your in-character reply here",
  "ai_emotion": "exact_emotion_from_list",
  "ai_emotion_intensity": 0.0-1.0,
  "ai_emotion_confidence": 0.0-1.0,
  "user_emotion": "detected_user_emotion",
  "user_emotion_confidence": 0.0-1.0,
  "user_emotion_intensity": 0.0-1.0,
  "memory_note": "key info to remember about this turn (optional)",
  "memory_note_importance": 0.0-1.0
}}

**CURRENT CONTEXT:**
Recent events:
{recent_summary or "No recent history"}

Important memory notes:
{memory_context or "No memory notes"}

World state: {conversation.world_state or "Default state"}

Now engage naturally."""
