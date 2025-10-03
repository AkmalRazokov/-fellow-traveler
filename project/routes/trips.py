from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from project.db.database import get_db
from project.models.models import Trip, User
from project.schemas.trip import TripCreateSchema, TripReadSchema
from project.auth.auth_bearer import JWTBearer
from project.auth.auth_handler import decode_jwt

router = APIRouter()


@router.get("/", response_model=List[TripReadSchema])
def get_all_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).all()
    return trips


@router.get("/{trip_id}", response_model=TripReadSchema)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip



@router.post("/", response_model=TripReadSchema)
def create_trip(trip_data: TripCreateSchema, db: Session = Depends(get_db), user_id: int = Depends(JWTBearer())):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_driver:
        raise HTTPException(status_code=403, detail="Only drivers can create trips")

    new_trip = Trip(
        driver_id=user_id,
        origin=trip_data.origin,
        destination=trip_data.destination,
        departure_time=trip_data.departure_time,
        seats_available=trip_data.seats_available,
        price=trip_data.price,
        description=trip_data.description
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip



@router.put("/{trip_id}", response_model=TripReadSchema)
def update_trip(
    trip_id: int,
    trip_data: TripCreateSchema,
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer())
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.driver_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this trip")
    
    trip.origin = trip_data.origin
    trip.destination = trip_data.destination
    trip.departure_time = trip_data.departure_time
    trip.seats_available = trip_data.seats_available
    trip.price = trip_data.price
    trip.description = trip_data.description

    db.commit()
    db.refresh(trip)
    return trip



@router.delete("/{trip_id}")
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer())
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.driver_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this trip")

    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted successfully"}



@router.put("/users/{user_id}/role/driver")
def update_driver_status(
    user_id: int,
    is_driver: bool,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(JWTBearer())
):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="You can only change your own role")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_driver = is_driver
    db.commit()
    return {"message": f"Driver status updated to {is_driver}"}

