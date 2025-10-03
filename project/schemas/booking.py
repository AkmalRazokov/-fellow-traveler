from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from project.schemas.user import UserReadSchema
from project.schemas.trip import TripReadSchema


class BookingReadSchema(BaseModel):
    id: int
    trip: TripReadSchema
    passenger: UserReadSchema
    confirmed: bool


    class Config:
        from_attributes = True


class BookingCreateSchema(BaseModel):
    trip_id: int

    class Config:
        from_attributes = True


class BookingUpdateSchema(BaseModel):
    confirmed: Optional[bool]

    class Config:
        from_attributes = True



