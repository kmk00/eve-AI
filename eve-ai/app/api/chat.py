from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import Session, asc, desc, select

from app.models.database import get_session
from app.models.schemas import Conversation, Message

router = APIRouter()

class MessageResponse(BaseModel):
    """Standardized response model for a Message object"""
    id: int
    role: str
    content: str
    created_at: datetime
    emotion: Optional[str] = None
    emotion_intensity: Optional[float] = None
    # token_count: Optional[int] = None
    # generation_time_ms: Optional[int] = None

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
