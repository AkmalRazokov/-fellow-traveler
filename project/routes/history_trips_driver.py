from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from project.db.database import get_db
from project.models.models import Trip
from project.schemas.trip import TripReadSchema
from project.auth.auth_bearer import JWTBearer

router = APIRouter()
@router.get("/driver", response_model=List[TripReadSchema])
def get_driver_trip_history(
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer())
):
    trips = db.query(Trip).filter(
        Trip.driver_id == user_id,
        Trip.departure_time < datetime.utcnow() 
    ).all()
    return trips
