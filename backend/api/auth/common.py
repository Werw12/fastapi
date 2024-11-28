# backend/api/auth/common.py
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from backend.database.database import SessionLocal
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../../templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()