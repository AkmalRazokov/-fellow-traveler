from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from project.db.database import get_db
from project.models.models import Booking, Trip, User
from project.schemas.booking import BookingCreateSchema, BookingReadSchema
from project.auth.auth_bearer import JWTBearer
from project.services.email_config import send_email

router = APIRouter()

@router.get("/", response_model=List[BookingReadSchema])
def get_all_bookings(upcoming_only: bool = False,db: Session = Depends(get_db),user_id: int = Depends(JWTBearer())):
    query = db.query(Booking).join(Trip).filter(Booking.passenger_id == user_id)
    if upcoming_only:
        query = query.filter(Trip.departure_time >= datetime.utcnow())

    return query.all()


@router.post("/", response_model=BookingReadSchema)
def create_booking(
    booking_data: BookingCreateSchema,
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer())
):
    trip = db.query(Trip).filter(Trip.id == booking_data.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.seats_available <= 0:
        raise HTTPException(status_code=400, detail="No available seats")

    if trip.driver_id == user_id:
        raise HTTPException(status_code=400, detail="Driver cannot book their own trip")

    existing_booking = db.query(Booking).filter(Booking.trip_id == trip.id,Booking.passenger_id == user_id).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="You have already booked this trip")

    booking = Booking(trip_id=trip.id,passenger_id=user_id,confirmed=False)

    db.add(booking)
    trip.seats_available -= 1
    db.commit()
    db.refresh(booking)
    return booking


@router.put("/{booking_id}/confirm")
async def confirm_booking(booking_id: int,db: Session = Depends(get_db),user_id: int = Depends(JWTBearer())):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    trip = booking.trip
    if trip.driver_id != user_id:
        raise HTTPException(status_code=403, detail="Only the driver can confirm bookings")

    booking.confirmed = True
    db.commit()

    passenger_email = booking.passenger.email
    if passenger_email:
        trip_info = f"{trip.origin} → {trip.destination} at {trip.departure_time}"
        await send_email(subject="Booking Confirmed",email_to=passenger_email,body=f"Your booking for the trip {trip_info} has been confirmed!")

    return {"message": "Booking confirmed"}


@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer())
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")


    if booking.passenger_id != user_id and booking.trip.driver_id != user_id:
        raise HTTPException(status_code=403, detail="You don't have permission to cancel this booking")


    trip = booking.trip
    trip.seats_available = min(trip.seats_available + 1, 10) 
    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled successfully"}
