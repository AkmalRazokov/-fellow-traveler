from project.services.verification import generate_verification_code
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from project.db.database import get_db
from project.models.models import User
from project.services.verification import verification_codes, assign_code, check_code
from project.schemas.user import UserRegisterSchema, UserLoginSchema, UserReadSchema, UserUpdateSchema
from project.utils.hashing import hash_password
from project.auth.auth_handler import generate_token
from project.auth.auth_bearer import JWTBearer
from project.utils.hashing import verify_password
from project.services.sms_service import send_sms
from project.settings.config import DEBUG


router = APIRouter()

@router.post("/auth/verify-code")
def verify_code(phone: str, code: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user.is_verified:
        return {"message":"Пользователь уже подтверждён"}

    if not check_code(phone, code):
        raise HTTPException(status_code=400, detail="Неверный код")

    user.is_verified = True
    db.commit()
    verification_codes.pop(phone, None)

    return {"message":"Пользователь успешно подтверждён"}



@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegisterSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = User(
        username=user_data.username,
        phone=user_data.phone,
        hashed_password=hash_password(user_data.password),
        is_verified=False,
        rating=5.0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    code = assign_code(new_user.phone)
    send_sms(new_user.phone, code)

    return {"message": "Пользователь успешно зарегистрирован", "code": code}




@router.post("/auth/login")
def login(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone==user_data.phone).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный номер или пароль")
    
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Пользователь не подтверждён")

    return generate_token(user.id)




@router.get("/me", response_model=UserReadSchema)
def get_my_profile(db: Session = Depends(get_db),user_id:int=Depends(JWTBearer())):
    user = db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserReadSchema)
def update_my_profile(user_data: UserUpdateSchema,db: Session = Depends(get_db),user_id: int = Depends(JWTBearer())):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_data.username or user.username
    user.email = user_data.email or user.email
    user.photo_url = user_data.photo_url or user.photo_url

    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserReadSchema)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user