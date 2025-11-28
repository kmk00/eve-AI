from ast import Set
import json
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship, Index
from typing import Any, List, Optional, Dict, Set
from datetime import datetime, timezone
from enum import StrEnum

class AIMode(StrEnum):
    LOCAL = "local"
    REMOTE = "remote"
    
class MemoryRetensionPreference(StrEnum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"

class EmotionsFrequency(StrEnum):
    FREQUENTLY = "frequently"
    SOMETIMES = "sometimes"
    RARELY = "rarely"
    NEVER = "never"

class Emotion(StrEnum):
    """Available emotions"""
    # Default 
    NEUTRAL = "neutral"
    CONTENT = "content"
    JOYFUL = "joyful"
    CURIOUS = "curious"
    PROTECTIVE = "protective"
    EXCITED = "excited"
    
    # Negative 
    IRRITATED = "irritated"
    ANGRY = "angry"  # zamiast FURIOUS
    ANXIOUS = "anxious"
    EMBARRASSED = "embarrassed"
    DISAPPOINTED = "disappointed"
    SCARED = "scared"
    
    # Social
    SARCASTIC = "sarcastic"
    AFFECTIONATE = "affectionate"
    PLAYFUL = "playful"
    SMUG = "smug"
    VULNERABLE = "vulnerable"
    FLUSTERED = "flustered"
    
    # State
    TIRED = "tired"
    CONFUSED = "confused"


# =========== USER ===========

class User(SQLModel,table=True):
    "User profile"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    gender: Optional[str] = Field(default="")
    age: Optional[int] = Field(default=None)
    
    profile_json: str = Field(default='{"likes": [], "dislikes": [],"personality": []}"', description="User profile in JSON format")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    conversations: List["Conversation"] = Relationship(back_populates="user")
    
    @property
    def profile(self) -> Dict[str, Any]:
        try:
            return json.loads(self.profile_json)
        except json.JSONDecodeError:
            return {"likes": [], "dislikes": [],"personality": []}
        
    @property
    def topics_user_likes(self) -> List[str]:
        return self.profile.get("likes", [])
    
    @property
    def topics_user_dislikes(self) -> List[str]:
        return self.profile.get("dislikes", [])
    
    @property
    def personality(self) -> List[str]:
        return self.profile.get("personality", [])
        
    
# =========== CONFIG ===========
class Config(SQLModel, table=True):
    """Global configuration settings"""
    id: Optional[int] = Field(default=1, primary_key=True)
    mode: str = Field(default=AIMode.LOCAL, description="AI mode (local or remote)")
    model_name: str = Field(default="gemma3:latest", description="AI model name")
    gpu_layers: int = Field(default=60, description="Number of GPU layers")
    temperature: float = Field(default=0.7, description="AI temperature")
    max_tokens: int = Field(default=4096, description="AI max tokens")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    conversation_memory_length: int = Field(default=10, description="Conversation memory length")
    emotion_confidence_threshold: float = Field(default=0.6, description="Emotion confidence threshold")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    __table_args__ = (Index("idx_config_mode", "id"),)



# =========== CHARACTER ===========
def get_emotion_check():
    emotions = "', '".join([e.value for e in Emotion])
    return f"CHECK (emotion IN ('{emotions}'))"


class Character(SQLModel, table=True):
    """Characters table"""
    
    # Main fields
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, index=True)
    description: str = Field(default="")
    personality: str = Field(default="")
    avatar: str = Field(default="")
    vrm_path: str = Field(default="")
    
    # World settings
    role_in_world: Optional[str] = Field(default="")
    world_context: Optional[str] = Field(default="")
    
    # Behavior settings
    speech_pattern: Optional[str] = Field(default="")
    favorite_phrases_json: str = Field(default="")   
    sentence_length_preference: Optional[str] = Field(default="medium")
    response_length_default: Optional[int] = Field(default="1-2 sentences")
    ask_questions_frequency: float = Field(default=0.2, ge=0.0, le=1.0)
    emoticons_frequency: str = Field(default=EmotionsFrequency.RARELY.value)
    memory_retention_preference: Optional[str] = Field(default=MemoryRetensionPreference.SHORT_TERM.value) 
    
    # Emotion settings    
    default_emotion: str = Field(default=Emotion.NEUTRAL.value)
    enabled_emotions_json: str = Field(default='["neutral","joyful","curious","protective","irritated","angry","anxious","embarrassed","disappointed","scared","sarcastic","affectionate","playful","smug","vulnerable","flustered","tired","confused"]')
    
    # Voice settings
    voice_id: Optional[str] = None
    speech_rate: Optional[float] = None
    pitch: Optional[float] = None
    
    # Status fields
    is_active: bool = Field(default=True)
    is_default: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_interaction_at: Optional[datetime] = None

    # Relationships
    conversations: List["Conversation"] = Relationship(back_populates="character")
    
    @field_validator("default_emotion","sentence_length_preference","response_length_default","emoticons_frequency","memory_retention_preference")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        return value.strip() if value else value
    
    @field_validator("enabled_emotions_json")
    @classmethod
    def validate_emotions_json(cls, value: str) -> str:
        try:
            emotions = json.loads(value)
            
            if not isinstance(emotions, list):
                raise ValueError("enabled_emotions_json must be a list of strings")
            for em in emotions:
                if em not in [e.value for e in Emotion]:
                    raise ValueError(f"Invalid emotion: {em}")
            return json.dumps(emotions)
        except json.JSONDecodeError as e:
            raise ValueError("enabled_emotions_json must be a valid JSON list of strings") from e
    
    @property
    def favorite_phrases(self) -> List[str]:
        try:
            return json.loads(self.favorite_phrases_json)
        except json.JSONDecodeError:
            return []          
    @favorite_phrases.setter
    def favorite_phrases(self, value: List[str]):
        self.favorite_phrases_json = json.dumps(value)
        
    @property
    def enabled_emotions(self) -> Set[Emotion]:
        try:
            return {Emotion(e) for e in json.loads(self.enabled_emotions_json)}
        except:
            return {Emotion.NEUTRAL}
        
    @enabled_emotions.setter
    def enabled_emotions(self, emotions: Set[Emotion]):
        invalid = emotions - set(Emotion)
        if invalid:
            raise ValueError(f"Invalid emotions: {[e.value for e in invalid]}")
        self.enabled_emotions_json = json.dumps([e.value for e in emotions])
    
    __table_args__ = (
        Index("idx_character_active", "is_active"),
        Index("idx_character_default", "is_default"),
    )

# =========== CONVERSATION ===========
class Conversation(SQLModel, table=True):
    """Singular conversation session table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    character_id: int = Field(foreign_key="character.id", index=True)
    character: Character = Relationship(back_populates="conversations")
    
    user_id: int = Field(foreign_key="user.id", index=True)
    user: User = Relationship(back_populates="conversations")
    
    relationship_type: str = Field(default="friend")
    
    user_intent: str = Field(default="casual_chat")
    world_state: str = Field(default="")
    
    # Conversation settings    
    title: Optional[str] = None
    message_count: int = Field(default=0)
    is_active: bool = Field(default=True, index=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    memory_notes: List["MemoryNote"] = Relationship(back_populates="conversation")
    messages: List["Message"] = Relationship(back_populates="conversation")

    @property
    def last_interactions_summary(self, max_messages=5):
        raise NotImplementedError
    
    __table_args__ = (Index("idx_conversation_activity", "last_activity", "character_id"),)

# =========== MESSAGE ===========
class Message(SQLModel, table=True):
    """Single message table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    conversation: Conversation = Relationship(back_populates="messages")
    role: str = Field(max_length=20)
    content: str = Field(max_length=20000)
    language: str = Field(default="en")
    
    # Emotions
    emotion: Optional[str] = Field(default=None, index=True)
    emotion_confidence: Optional[float] = Field(default=None,ge=0.0,le=1.0)
    emotion_intensity: float = Field(default=0.5,ge=0.0,le=1.0)
    
    #Meta
    ai_detected_emotion: Optional[str] = None
    generation_time_ms: Optional[int] = None
    token_count: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    memory_note: Optional["MemoryNote"] = Relationship(back_populates="message")
    
    # Validation
    @field_validator("emotion")
    @classmethod
    def validate_emotion(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v not in [e.value for e in Emotion]:
            raise ValueError(f"Invalid emotion: {v}")
        return v
    
    @property
    def full_emotion(self) -> str:
        """Full emotion name with intensity"""
        if not self.emotion:
            return Emotion.NEUTRAL.value
        
        if self.emotion_intensity >= 0.8:
            return f'extremely_{self.emotion}'
        elif self.emotion_intensity >= 0.6:
            return f'very_{self.emotion}'
        elif self.emotion_intensity >= 0.3:
            return f'{self.emotion}'
        elif self.emotion_intensity >= 0.1:
            return f'slightly_{self.emotion}'
        return Emotion.NEUTRAL
    

# =========== MEMORY NOTE ===========
class MemoryNote(SQLModel, table=True):
    """Important memory to be referenced later"""
    id: Optional[int] = Field(default=None, primary_key=True)
    character_id: int = Field(foreign_key="character.id", index=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    conversation: Conversation = Relationship(back_populates="memory_notes")
    
    content: str = Field(max_length=500)
    source_message_id: Optional[int] = Field(foreign_key="message.id")
    
    importance_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_referenced: Optional[datetime] = None
    
    message: Optional["Message"] = Relationship(back_populates="memory_note")
    
    __table_args__ = (
        Index("idx_memory_importance", "character_id", "importance_score"),
    )