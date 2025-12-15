from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlmodel import Session, select
from app.models.database import get_session
from app.models.schemas import Character
router = APIRouter()

class FetchCharactersRequest(BaseModel):
    limit: Optional[int] = None
    
class CharacterResponse(BaseModel):
    id: int
    name: str
    description: str
    avatar: str
    model_image: Optional[str]
    vrm_path: str
    
    enabled_emotions: List[str] 
    favorite_phrases: List[str]
    
    default_emotion: str
    is_active: bool

    # To jest kluczowe! Pozwala Pydanticowi czytać dane z obiektu ORM (SQLModel)
    model_config = ConfigDict(from_attributes=True)

class CharacterFullResponse(BaseModel):
    id: int
    name: str
    
    description: str
    personality: str
    avatar: str
    model_image: Optional[str] = None
    vrm_path: str = ""
    
    role_in_world: Optional[str] = ""
    world_context: Optional[str] = ""
    
    speech_pattern: Optional[str] = ""
    sentence_length_preference: str
    response_length_default: str
    ask_questions_frequency: float
    emoticons_frequency: str
    memory_retention_preference: str
    
    default_emotion: str
    voice_id: Optional[str] = None
    speech_rate: Optional[float] = None
    pitch: Optional[float] = None
    
    is_active: bool
    is_default: bool
    

    favorite_phrases: List[str] 
    enabled_emotions: List[str] 

    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[CharacterResponse])
async def get_characters(
    limit: Optional[int] = Query(default=None), 
    session: Session = Depends(get_session)
):
    statement = select(Character)
    
    if limit is not None:
        statement = statement.limit(limit)
        
    characters = session.exec(statement).all()
    return characters

@router.get("/default", response_model=CharacterResponse)
async def get_default_character(session: Session = Depends(get_session)):
    
    statement = select(Character).where(Character.is_default == True)
    character = session.exec(statement).one_or_none()
    
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character