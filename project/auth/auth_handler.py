import time
from typing import Dict
from project.models.models import User
from project.db.database import SessionLocal
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }



def generate_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)




def decode_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None




