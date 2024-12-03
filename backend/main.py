from fastapi import FastAPI, BackgroundTasks
from backend.api.auth.user_router import router as auth_router
from backend.api.auth.password_reset import router as password_reset_router
from backend.api.auth.refresh_token import router as refresh_token_router
from backend.middleware.auth_middleware import auth_middleware
from backend.parsers.parsers import run_spider
from backend.core.schemas.scrapy import ScrapyRequest

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

@app.post("/run_spider")
async def run_spider_endpoint(scrapy_request: ScrapyRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_spider, scrapy_request.url)
    return {"message": "Spider is running in the background"}