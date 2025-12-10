from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlmodel import Session, asc, desc, select

from app.models.database import get_session
from app.models.schemas import Conversation, Message
from app.services.ai_service import AI_Service

router = APIRouter()

class MessageCreateRequest(BaseModel):
    """Model dla nowej wiadomości wysyłanej przez użytkownika"""
    content: str = Field(..., min_length=1, description="Treść wiadomości użytkownika")

class MessageResponse(BaseModel):
    """Standardized response model for a Message object"""
    id: int
    role: str
    content: str
    created_at: datetime
    emotion: Optional[str] = None
    emotion_intensity: Optional[float] = None
    generation_time_ms: Optional[int] = None
    # token_count: Optional[int] = None

    class Config:
        from_attributes = True
        
class PaginatedHistoryResponse(BaseModel):
    """Metadata wrapper for paginated message history"""
    total: int
    limit: int
    offset: int
    messages: List[MessageResponse]

def get_valid_conversation(
    character_id: int, conversation_id: int, session: Session
) -> Conversation:
    """
    Helper function to validate if a conversation belongs to a character
    """
    conversation = session.get(Conversation, conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=404, detail="Conversation not found"
        )
    
    if conversation.character_id != character_id: raise HTTPException(status_code=404, detail="Conversation does not belong to this character")
        
    return conversation


ai_service=AI_Service()

@router.post("/{character_id}/{conversation_id}",response_model=MessageResponse)
async def send_message(
    message_data: MessageCreateRequest,
    character_id: int = Path(..., description="ID postaci"),
    conversation_id: int = Path(..., description="ID konwersacji, do której wysyłamy"),
    session: Session = Depends(get_session)
):
    """
    Send a new message to a specific conversation for a character
    Generate a response from the AI service
    Save the response to the database
    """
    get_valid_conversation(character_id, conversation_id, session)

    try:

        ai_message_model, generation_time_s = ai_service.generate_response(
            message_text=message_data.content,
            conversation_id=conversation_id,
            session=session
        )
        
        return ai_message_model

    except ValueError as ve:
        # Obsługa błędów logiki biznesowej (np. pusta odpowiedź z LLM, błędne ID w serwisie)
        print(f"Business logic error in generate_response: {ve}")
        # Zwracamy 400 Bad Request dla błędów walidacji logicznej
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Obsługa nieoczekiwanych błędów (np. awaria bazy danych, awaria API Ollama)
        print(f"Critical error in send_message endpoint: {e}")
        # W produkcji nie pokazujemy surowego błędu klientowi
        raise HTTPException(status_code=500, detail="Internal server error during message generation.")

@router.get("/{character_id}/{conversation_id}/messages",response_model=PaginatedHistoryResponse)
async def get_chat_history(
    character_id: int = Path(..., description="Character ID"),
    conversation_id: int = Path(..., description="Conversation ID"),
    limit: int = Query(50, ge=1, le=200, description="Number of messages to return"),
    offset: int = Query(0, ge=0, description="Number of messages to skip"),
    sort_desc: bool = Query(False, description="Sort messages in descending order, default is ascending"),
    session: Session = Depends(get_session)
):
    """
    Downloads history of a conversation for a character
    """
    get_valid_conversation(character_id, conversation_id, session)

    query = select(Message).where(Message.conversation_id == conversation_id)

    count_query = select(func.count()).select_from(query.subquery())
    total_messages = session.exec(count_query).one()

    if sort_desc:
        query = query.order_by(desc(Message.created_at))
    else:
        query = query.order_by(asc(Message.created_at))

    messages = session.exec(query.offset(offset).limit(limit)).all()

    return {
        "total": total_messages,
        "limit": limit,
        "offset": offset,
        "messages": messages
    }
    
    
@router.delete("/{character_id}/{conversation_id}", status_code=204)
async def delete_conversation(
    character_id: int = Path(..., description="ID postaci"),
    conversation_id: int = Path(..., description="ID konwersacji do usunięcia"),
    session: Session = Depends(get_session)
):
    """
    Deletes a conversation
    """
    conversation = get_valid_conversation(character_id, conversation_id, session)

    try:
        session.delete(conversation)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Failed to delete conversation {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete conversation due to database error.")

    return None
