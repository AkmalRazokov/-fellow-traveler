from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from project.db.database import get_db
from project.models.models import Trip
from project.schemas.trip import TripReadSchema

router = APIRouter()


@router.get("/search", response_model=List[TripReadSchema])
def search_trips(
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Trip)

    if origin:
        query = query.filter(Trip.origin.ilike(f"%{origin}%"))

    if destination:
        query = query.filter(Trip.destination.ilike(f"%{destination}%"))

    if date:
        start_dt = datetime.combine(date, datetime.min.time())
        end_dt = datetime.combine(date, datetime.max.time())
        query = query.filter(Trip.departure_time.between(start_dt, end_dt))

    trips = query.all()
    return trips
