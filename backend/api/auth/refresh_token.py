from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from backend.core.config import SECRET_KEY, ALGORITHM
from backend.api.auth.common import get_db
from backend.core.models.user import User
from backend.api.auth.user_token import create_access_token, create_refresh_token
from backend.api.auth.common import router



@router.post("/refresh-token", operation_id="refresh_token")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_access_token(data={"sub": user.email})
    new_refresh_token = create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": new_refresh_token}