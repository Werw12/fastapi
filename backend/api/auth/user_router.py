import logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.models import user as models
from backend.core.schemas import user as schemas
from backend.api.auth.utils import get_password_hash, verify_password
from backend.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.api.auth.user_token import create_access_token
from datetime import timedelta
from backend.api.auth.common import get_db
from backend.api.auth.common import router



@router.post("/register", response_model=schemas.User, operation_id="register_user")
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=hashed_password,
            email=user.email
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Not authenticated")

@router.post("/login", operation_id="login_user")
async def login_user(email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}