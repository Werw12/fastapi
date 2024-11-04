from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    async def read_root():
        return {"message": "Hello, World!"}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)