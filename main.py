from fastapi import FastAPI
import uvicorn
from project.routes.users import router as user_router
from project.routes.trips import router as trip_router
from project.routes.bookings import router as booking_router
from project.routes.reviews import router as review_router
from project.routes.search_trip import router as search_trip_router
from project.routes.history_trips_driver import router as history_driver_router
from project.routes.history_trips_passenger import router as history_passenger_router
from project.routes.chat import router as chat_router
from project.midlewar.midleware import AdvancedMiddleware


app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(trip_router, prefix="/trips", tags=["trips"])
app.include_router(search_trip_router, prefix="/search", tags=["search"])
app.include_router(booking_router, prefix="/bookings", tags=["bookings"])
app.include_router(review_router, prefix="/reviews", tags=["reviews"])
app.include_router(history_driver_router, prefix="/history_driver", tags=["history_driver"])
app.include_router(history_passenger_router, prefix="/history_passenger", tags=["history_passenger"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.add_middleware(AdvancedMiddleware)






if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=True)
