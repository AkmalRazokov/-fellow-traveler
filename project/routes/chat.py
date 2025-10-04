from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from project.db.database import get_db
from project.models.models import Message, User, Trip
from project.schemas.message import MessageCreateSchema, MessageReadSchema
from project.auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/", response_model=MessageReadSchema)
def send_message(message_data: MessageCreateSchema,db: Session = Depends(get_db),sender_id: int = Depends(JWTBearer())):
    receiver = db.query(User).filter(User.id == message_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    if message_data.trip_id:
        trip = db.query(Trip).filter(Trip.id == message_data.trip_id).first()
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")

    message = Message(
        trip_id=message_data.trip_id,
        sender_id=sender_id,
        receiver_id=message_data.receiver_id,
        content=message_data.content,
        timestamp=datetime.utcnow()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/conversation/{user_id}", response_model=List[MessageReadSchema])
def get_conversation_with_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(JWTBearer())
):
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user_id))
    ).order_by(Message.timestamp).all()

    return messages
