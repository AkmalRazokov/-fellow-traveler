from pydantic import BaseModel, Field
from typing import Optional
from project.schemas.user import UserReadSchema
from project.schemas.trip import TripReadSchema


class ReviewCreateSchema(BaseModel):
    trip_id: int
    user_id: int  
    rating: float = Field(..., ge=0.0, le=5.0)
    comment: Optional[str] = None


class ReviewReadSchema(BaseModel):
    id: int
    reviewer: UserReadSchema
    reviewed_user: UserReadSchema
    trip: TripReadSchema
    rating: float
    comment: Optional[str] = None

    class Config:
        from_attributes = True
