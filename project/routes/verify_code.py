from fastapi import HTTPException, Depends, APIRouter
from project.db.database import get_db
from project.services.verification import verification_codes
from project.models.models import User
from datetime import datetime
from project.db.database import SessionLocal

router = APIRouter()

@router.post("/auth/verify-code")
def verify_code(phone: str, code: str):
    entry = verification_codes.get(phone)
    if not entry or entry["expires_at"] < datetime.utcnow():
        return {"message": "Код истёк или не найден"}

    if entry["code"] != code:
        return {"message": "Неверный код"}


    db = SessionLocal()
    user = db.query(User).filter(User.phone == phone).first()
    if user:
        user.is_verified = True
        db.commit()
        db.close()
        return {"message": "Номер подтверждён"}
    return {"message": "Пользователь не найден"}
