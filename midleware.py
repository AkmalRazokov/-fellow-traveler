from starlette.middleware.base import BaseHTTPMiddleware
import time
from fastapi import Request, status
from starlette.responses import Response


class AdvancedMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.limit_per_sc = {}
        self.secret_token = "secret_token"

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")

        if auth_header:
            if auth_header.startswith("Bearer "):
                token = auth_header.split("Bearer ")[1]
                if token == self.secret_token:
                    return await call_next(request)
            
            return Response(content="Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)


        current_time = time.time()
        ip_address = request.client.host

        data = self.limit_per_sc.get(ip_address)

        if data:
            last_time = data["start_time"]
            requests = data["requests"]

            if current_time - last_time <= 20:
                if len(requests) >= 10:
                    return Response(content="Too many requests", status_code=429)
                else:
                    requests.append(current_time)
            else:
                self.limit_per_sc[ip_address] = {
                    "start_time": current_time,
                    "requests": [current_time]
                }
        else:
            self.limit_per_sc[ip_address] = {
                "start_time": current_time,
                "requests": [current_time]
            }

        response = await call_next(request)
        return response
