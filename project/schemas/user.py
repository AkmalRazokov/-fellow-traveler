from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from datetime import datetime


class UserRegisterSchema(BaseModel):
    username: str
    phone: str = Field(..., pattern = r"^\+992\d{9}$")
    password: str = Field(..., min_length=6)

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    phone: str = Field(..., pattern=r"^\+992\d{9}$")
    password: str

    class Config:
        from_attributes = True


class UserReadSchema(BaseModel):
    id: int
    username: str
    email: Optional[str]
    phone: str
    photo_url: Optional[str]
    rating: float
    is_driver: bool
    is_passenger: bool


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    email: Optional[str]
    photo_url: Optional[str]

    class Config:
        from_attributes = True