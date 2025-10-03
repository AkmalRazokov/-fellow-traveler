
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project.db.database import Base
from typing import Optional, List
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    is_driver: Mapped[bool] = mapped_column(Boolean, default=False)
    is_passenger: Mapped[bool] = mapped_column(Boolean, default=True)

    trips: Mapped[List["Trip"]] = relationship(back_populates="driver")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="passenger")
    reviews_received: Mapped[List["Review"]] = relationship(back_populates="reviewed_user",foreign_keys="Review.user_id") 
    reviews_given: Mapped[List["Review"]] = relationship(back_populates="reviewer",foreign_keys="Review.reviewer_id")


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int]=mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    origin: Mapped[str] = mapped_column(String)
    destination: Mapped[str] = mapped_column(String)
    departure_time: Mapped[datetime] = mapped_column(DateTime)
    seats_available: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    driver: Mapped["User"] = relationship(back_populates="trips")
    reviews: Mapped[List["Review"]] = relationship(back_populates="trip")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="trip", cascade="all, delete-orphan")
    # messages: Mapped[List["Message"]] = relationship("Message", back_populates="trip", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"))
    passenger_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    trip: Mapped["Trip"] = relationship(back_populates="bookings")
    passenger: Mapped["User"] = relationship(back_populates="bookings")




class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"))
    rating: Mapped[float] = mapped_column(Float)
    comment: Mapped[Optional[str]] = mapped_column(Text)

    trip: Mapped["Trip"] = relationship("Trip", back_populates="reviews")
    reviewer: Mapped["User"] = relationship(back_populates="reviews_given",foreign_keys=[reviewer_id])
    reviewed_user: Mapped["User"] = relationship(back_populates="reviews_received",foreign_keys=[user_id])




# class Message(Base):
#     __tablename__ = "messages"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"))
#     sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     content: Mapped[str] = mapped_column(Text)
#     timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
#     is_read: Mapped[bool] = mapped_column(Boolean, default=False)

#     trip = relationship("Trip", back_populates="messages")
#     sender = relationship("User", foreign_keys=[sender_id])
#     receiver = relationship("User", foreign_keys=[receiver_id])