from fastapi import FastAPI

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Выполняет действия при инициализации приложения.
    """
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_start_page():
    return {"message": "Hello, FastAPI!"}