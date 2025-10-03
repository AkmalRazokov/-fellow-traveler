
from project.db.database import engine, Base
from fastapi import FastAPI
import uvicorn
from project.routes.users import router as user_router
from project.routes.trips import router as trip_router
from project.routes.bookings import router as booking_router
from project.routes.reviews import router as review_router
from project.routes.search_trip import router as search_trip_router
from midleware import AdvancedMiddleware


app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(trip_router, prefix="/trips", tags=["trips"])
app.include_router(search_trip_router, prefix="/search", tags=["search"])
app.include_router(booking_router, prefix="/bookings", tags=["bookings"])
app.include_router(review_router, prefix="/reviews", tags=["reviews"])
app.add_middleware(AdvancedMiddleware)






if __name__ == "__main__":
    uvicorn.run("project.main:app", host="localhost", port=8000, reload=True)
