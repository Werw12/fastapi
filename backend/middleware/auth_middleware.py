from fastapi import Request, HTTPException
from jose import JWTError, jwt
from backend.core.config import SECRET_KEY, ALGORITHM

async def auth_middleware(request: Request, call_next):
    protected_routes = ["/protected"]

    if request.url.path in protected_routes:
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")

        token = token[len("Bearer "):]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Not authenticated")

    response = await call_next(request)
    return response