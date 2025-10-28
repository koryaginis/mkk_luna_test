from fastapi import FastAPI
from sqlalchemy import text
from app.deps import engine
from app.routers import (
    phones_router, 
    organizations_router, 
    buildings_router, 
    activities_router
)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Создает расширение ltree при инициализации приложения.
    """
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS ltree;"))

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(phones_router.router, prefix="/api")
app.include_router(organizations_router.router, prefix="/api")
app.include_router(buildings_router.router, prefix="/api")
app.include_router(activities_router.router, prefix="/api")