from fastapi import HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from backend.core.models.user import User
from backend.api.auth.user_token import create_password_reset_token
from backend.utils.email import send_email
from backend.api.auth.utils import get_password_hash
from backend.core.config import SECRET_KEY, ALGORITHM
from backend.api.auth.common import get_db, templates
from backend.core.schemas.user import PasswordResetRequest
from backend.api.auth.common import router

@router.post("/password-reset-request", operation_id="password_reset_request")
async def password_reset_request(request: Request, password_reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == password_reset_request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_password_reset_token(password_reset_request.email)
    reset_link = f"http://localhost:8080/reset-password?token={token}"

    # Render the HTML template with the reset link
    html_content = templates.TemplateResponse("reset_password.html", {"request": request, "reset_link": reset_link})
    await send_email(password_reset_request.email, "Password Reset Request", html_content.body.decode("utf-8"))

    return {"msg": "Password reset email sent"}

@router.get("/reset-password", response_class=HTMLResponse, operation_id="reset_password_form")
async def reset_password_form(request: Request, token: str):
    return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})

@router.post("/reset-password", operation_id="reset_password")
async def reset_password(token: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(new_password)
    db.commit()

    return {"msg": "Password reset successful"}