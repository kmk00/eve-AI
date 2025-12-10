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


@router.patch(f"",response_model=ConfigResponse)
def update_config(
    update_data: ConfigUpdateRequest,
    session: Session = Depends(get_session)
):
    """
    Update config in database
    
    At least one property must be provided in the request body.
    
    Args:
        mode: str
        model_name: str
        gpu_layers: int
        temperature: float
        max_tokens: int
        openai_api_key: Optional[str]
        anthropic_api_key: Optional[str]
        conversation_memory_length: int
        emotion_confidence_threshold: float
    """
    # Walidacja, że nie jest pusty request
    if not any(value is not None for value in update_data.model_dump().values()):
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided for update"
        )
    
    config = session.get(Config, 1)
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuration not found"
        )
    
    # Aktualizujemy tylko podane pola
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(config, key, value)
    
    config.updated_at = datetime.now(timezone.utc)
    
    try:
        session.commit()
        session.refresh(config)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update configuration: {str(e)}"
        )
    
    return config   



@router.post(f"",response_model=ConfigResponse)
def reset_config(
    session: Session = Depends(get_session)
):
    """
    Reset config in database
    """
    config = session.get(Config, 1)
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuration not found"
        )
        
    config.mode = AIMode.LOCAL
    config.model_name = "gemma3:latest"
    config.gpu_layers = 60
    config.temperature = 0.7
    config.max_tokens = 4096
    config.conversation_memory_length = 10
    config.emotion_confidence_threshold = 0.6
    config.updated_at = datetime.now(timezone.utc)    
    
    try:
        session.commit()
        session.refresh(config)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reset configuration: {str(e)}"
        )
    
    return config