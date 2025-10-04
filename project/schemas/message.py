from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageCreateSchema(BaseModel):
    trip_id: Optional[int]  
    sender_id: int
    receiver_id: int
    content: str

    class Config:
        from_attributes = True


class MessageReadSchema(BaseModel):
    id: int
    trip_id: Optional[int]
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime
    is_read: bool

    class Config:
        from_attributes = True
