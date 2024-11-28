from fastapi import FastAPI
from backend.api.auth.user_router import router as auth_router
from backend.api.auth.password_reset import router as password_reset_router
from backend.api.auth.refresh_token import router as refresh_token_router
from backend.middleware.auth_middleware import auth_middleware

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(password_reset_router, prefix="/auth")
app.include_router(refresh_token_router, prefix="/auth")

app.middleware("http")(auth_middleware)

@app.get("/protected")
async def read_protected():
    return {"message": "This is a protected route"}

@app.get("/hello")
async def read_hello():
    return {"message": "Hello, World!"}