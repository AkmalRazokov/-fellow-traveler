
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from project.auth.auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> int:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

        payload = decode_jwt(credentials.credentials)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid or expired token.")

        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=403, detail="Invalid token payload.")

        return user_id