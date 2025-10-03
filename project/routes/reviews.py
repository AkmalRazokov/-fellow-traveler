from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from project.db.database import get_db
from project.auth.auth_bearer import JWTBearer
from project.models.models import Review, Trip, User, Booking
from project.schemas.review import ReviewCreateSchema, ReviewReadSchema
from typing import List

router = APIRouter()

@router.post("/", response_model=ReviewReadSchema)
def create_review(review_data: ReviewCreateSchema,db: Session = Depends(get_db),user_id: int = Depends(JWTBearer())):
    trip = db.query(Trip).filter(Trip.id == review_data.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    booking = db.query(Booking).filter(
    Booking.trip_id == review_data.trip_id,
    Booking.passenger_id == user_id,
    Booking.confirmed == True
    ).first()
    if not booking:
        raise HTTPException(status_code=403, detail="You did not participate in this trip")
    existing_review = db.query(Review).filter_by(
        trip_id=review_data.trip_id,
        reviewer_id=user_id
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this trip")

    review = Review(
        trip_id=review_data.trip_id,
        reviewer_id=user_id,
        user_id=trip.driver_id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    db.add(review)

    driver = db.query(User).filter(User.id == trip.driver_id).first()
    driver_reviews = db.query(Review).filter(Review.user_id == driver.id).all()
    total_rating = sum([r.rating for r in driver_reviews]) + review_data.rating
    review_count = len(driver_reviews) + 1
    driver.rating = round(total_rating / review_count, 2)

    db.commit()
    db.refresh(review)

    return review

@router.get("/trip/{trip_id}", response_model=List[ReviewReadSchema])
def get_reviews_for_trip(trip_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.trip_id == trip_id).all()

@router.get("/user/{user_id}", response_model=List[ReviewReadSchema])
def get_reviews_for_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.user_id == user_id).all()
