from sqlmodel import SQLModel, Field, Relationship, Index
from typing import List, Optional
from datetime import datetime, timezone
from enum import StrEnum

class AIMode(StrEnum):
    LOCAL = "local"
    REMOTE = "remote"

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
class Character(SQLModel, table=True):
    """Characters table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, index=True)
    description: str = Field(default="")
    personality: str = Field(default="")
    avatar: str = Field(default="")
    voice_id: Optional[str] = None
    speech_rate: Optional[float] = None
    pitch: Optional[float] = None
    default_emotion: str = Field(default="neutral")
    enabled_emotions: str = Field(default="happy,sad,angry,neutral,pouting,embarrassed,talking")
    is_active: bool = Field(default=True)
    is_default: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_interaction_at: Optional[datetime] = None

    conversations: List["Conversation"] = Relationship(back_populates="character")
    emotion_keywords: List["EmotionKeyword"] = Relationship(back_populates="character")
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
    title: Optional[str] = None
    message_count: int = Field(default=0)
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    messages: List["Message"] = Relationship(back_populates="conversation")
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
    emotion: Optional[str] = None
    emotion_confidence: Optional[float] = None
    ai_detected_emotion: Optional[str] = None
    generation_time_ms: Optional[int] = None
    token_count: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# =========== EMOTION KEYWORD ===========
class EmotionKeyword(SQLModel, table=True):
    """Custom keywords per character dla emotion detection"""
    id: Optional[int] = Field(default=None, primary_key=True)
    character_id: int = Field(foreign_key="character.id")
    character: Character = Relationship(back_populates="emotion_keywords")
    emotion: str = Field(max_length=50, index=True)
    keyword: str = Field(max_length=100)
    weight: float = Field(default=1.0)
    language: str = Field(default="en", max_length=10)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    __table_args__ = (Index("idx_keyword_lookup", "character_id", "keyword", "language"),)

# =========== EMOTION LOG ===========
class EmotionLog(SQLModel, table=True):
    """Historia zmian emocji dla analytics"""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    message_id: int = Field(foreign_key="message.id", index=True)
    emotion: str = Field(max_length=50)
    confidence: float
    trigger_source: str = Field(max_length=50)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    __table_args__ = (Index("idx_emotion_timeseries", "timestamp", "emotion"),)

# =========== VRM MODEL CACHE ===========
class VRMModelCache(SQLModel, table=True):
    """Cache informacji o modelach VRM dla szybszego loadingu"""
    id: Optional[int] = Field(default=None, primary_key=True)
    file_path: str = Field(unique=True, index=True)
    file_hash: str = Field(unique=True, index=True)
    file_size: int
    vrm_version: str
    thumbnail_path: Optional[str] = None
    blendshape_count: int
    blendshape_names: str = Field(max_length=2000)
    load_time_ms: int
    last_used: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    use_count: int = Field(default=1)
    __table_args__ = (Index("idx_cache_usage", "last_used"),)