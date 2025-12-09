from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session
from app.models.database import get_session
from app.models.schemas import AIMode, Config

router = APIRouter()


class ConfigResponse(BaseModel):
    """Model odpowiedzi z konfiguracją"""
    id: int
    mode: str
    model_name: str
    gpu_layers: int
    temperature: float
    max_tokens: int
    openai_api_key: Optional[str]
    anthropic_api_key: Optional[str]
    conversation_memory_length: int
    emotion_confidence_threshold: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ConfigUpdateRequest(BaseModel):
    """Model do częściowej aktualizacji konfiguracji"""
    mode: Optional[str] = None
    model_name: Optional[str] = None
    gpu_layers: Optional[int] = Field(None, ge=0, le=200)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=32000)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    conversation_memory_length: Optional[int] = Field(None, ge=1, le=100)
    emotion_confidence_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)

@router.get("",response_model=ConfigResponse)
async def get_config(session: Session=Depends(get_session)):
    
    config = session.get(Config,1)
    
    if not config: 
        raise HTTPException(status_code=404, detail="Config not found")
    
    return config


