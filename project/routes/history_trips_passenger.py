from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from project.db.database import get_db
from project.models.models import Trip, Booking
from project.schemas.trip import TripReadSchema
from project.auth.auth_bearer import JWTBearer

router = APIRouter()


@router.get("/passenger", response_model=List[TripReadSchema])
def get_passenger_trip_history(
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer())
):
    bookings = db.query(Booking).join(Trip).filter(
        Booking.passenger_id == user_id,
        Trip.departure_time < datetime.utcnow(),
        Booking.confirmed == True
    ).all()

    trips = [booking.trip for booking in bookings]
    return trips
