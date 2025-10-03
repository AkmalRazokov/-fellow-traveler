from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime, timedelta
from project.schemas.user import UserReadSchema

class TripReadSchema(BaseModel):
    id: int
    driver: UserReadSchema
    origin: str
    destination: str
    departure_time: datetime
    seats_available: int
    price: float
    description: Optional[str] | None = None

    class Config:
        from_attributes = True



class TripCreateSchema(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    seats_available: int
    price: float
    description: Optional[str] = None


    class Config:
        from_attributes = True