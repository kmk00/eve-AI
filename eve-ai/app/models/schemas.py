from sqlmodel import SQLModel, Field,  Relationship, Index
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, timezone
from enum import StrEnum

# =========== TYPES ===========

class AIMode(StrEnum):
    LOCAL = "local"
    REMOTE = "remote"
    
# =========== CONFIGURATION ===========

class Config(SQLModel, table=True):
    """Global configuration settings"""
    id: Optional[int] = Field(default=1, primary_key=True)
    
    #AI Settings
    mode:str = Field(default=AIMode.LOCAL, description="AI mode (local or remote)")
    model_name: str = Field(default="gemma3:latest", description="AI model name")
    gpu_layers: int = Field(default=60, description="Number of GPU layers")
    temperature: float = Field(default=0.7, description="AI temperature")
    max_tokens: int = Field(default=4096, description="AI max tokens")
    
    #API Keys
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")

    #Performance
    conversation_memory_length: int = Field(default=10, description="Conversation memory length")
    emotion_confidence_threshold: float = Field(default=0.6, description="Emotion confidence threshold")
    
    #Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    #Indexes
    __table_args__ = (Index("idx_config_mode", "id"),)

class Conversations(SQLModel, table=True):
    """Singular conversation session table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    #Relationships
    character_id: int = Field(foreign_key="characters.id", index=True)
    character: "Characters" = Relationship(back_populates="conversations")
    
    #Metadata
    title: Optional[str] = Field(default=None, description="Conversation title")
    message_count: int = Field(default=0, description="Number of messages in conversation")
    
    #Status
    is_active: bool = Field(default=True, index=True)
    
    #Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    #Indexes
    __table_args__ = (Index("idx_conversations_active","last_activity","character_id" ),)
    

# =========== CHARACTERS ===========
class Characters(SQLModel, table=True):
    """Characters table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    #Identity
    name: str = Field(default=None, description="Character name", max_length=50, unique=True, index=True)
    description: str = Field(default=None, description="Character description")
    personality: str = Field(default=None, description="Character personality")
    
    #Avatar
    avatar: str = Field(default=None, description="Character avatar")
    
    #Voice Settings
    voice_id: Optional[str] = Field(default=None, description="Voice ID")
    speech_rate: Optional[float] = Field(default=None, description="Speech rate")
    pitch: Optional[float] = Field(default=None, description="Pitch")
    
    #Emotions
    default_emotion: str = Field(default=None, description="Default emotion")
    enabled_emotions: str = Field(default="happy,sad,angry,neutral,pouting,embarrassed,talking", description="Enabled emotions")
    
    # Status
    is_active: bool = Field(default=True, index=True)
    is_default: bool = Field(default=False, index=True)
    
    #Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_interaction_at: datetime = Field(default=None)
    
    #Relationships
    conversations: List["Conversations"] = Relationship(back_populates="characters")
    emotion_keywords: List["EmotionKeywords"] = Relationship(back_populates="characters")
    
    #Indexes
    __table_args__ = (Index("idx_characters_active","is_active" ), Index("idx_characters_default", "is_default" ),)

class EmotionLogs(SQLModel, table=True):
    """Historia zmian emocji dla analytics"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    message_id: int = Field(foreign_key="messages.id", index=True)
    
    # Emotion data
    emotion: str = Field(max_length=50, index=True)
    confidence: float
    trigger_source: str = Field(max_length=50)  # keyword/ai/sentiment
    
    # Timestamps
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Indeksy
    __table_args__ = (
        Index("idx_emotion_timeseries", "timestamp", "emotion"),
    )
    
class Messages(SQLModel, table=True):
    """Single message table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    #Relationships
    conversation_id: int = Field(foreign_key="conversations.id")
    conversation: "Conversations" = Relationship(back_populates="messages")
    
    #Content
    role: str = Field(default=None, description="Message role",max_length=20)
    content: str = Field(default=None, description="Message content",max_length=20000)
    language: str = Field(default="en", description="Message language")
    
    #Emotion
    emotion: str = Field(default=None, description="Message emotion")
    emotion_confidence: float = Field(default=None, description="Message emotion confidence")
    ai_detected_emotion: str = Field(default=None, description="AI detected emotion")
    
    #Performance
    generation_time_ms: Optional[int] = Field(default=None, description="Message generation time in milliseconds")
    token_count : Optional[int] = Field(default=None, description="Message token count")
    
    #Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    

class EmotionKeywords(SQLModel, table=True):
    """Custom keywords per character dla emotion detection"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    character_id: int = Field(foreign_key="characters.id", index=True)
    character: "Characters" = Relationship(back_populates="emotion_keywords")
    
    # Keyword data
    emotion: str = Field(max_length=50, index=True)
    keyword: str = Field(max_length=100, index=True)
    weight: float = Field(default=1.0)
    language: str = Field(default="en", max_length=10)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Indeksy
    __table_args__ = (
        Index("idx_keyword_lookup", "character_id", "keyword", "language"),
    )

class VRMModelCache(SQLModel, table=True):
    """Cache informacji o modelach VRM dla szybszego loadingu"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    file_path: str = Field(unique=True, index=True)
    file_hash: str = Field(unique=True, index=True)
    
    # Metadata
    file_size: int
    vrm_version: str
    thumbnail_path: Optional[str] = None
    
    # Blend shape info
    blendshape_count: int
    blendshape_names: str = Field(max_length=2000)  # JSON serialized
    
    # Performance
    load_time_ms: int
    last_used: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    use_count: int = Field(default=1)
    
    # Indekses
    __table_args__ = (
        Index("idx_cache_usage", "last_used"),
    )