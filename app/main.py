from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.deps import get_db, engine
from app.routers import phones_router, organizations_router, buildings_router

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

@app.get("/")
async def get_start_page():
    return {"message": "Hello, FastAPI!"}

@app.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    # Проверим подключение и существование расширения ltree
    result = await db.execute(text("SELECT extname FROM pg_extension WHERE extname='ltree';"))
    ltree_installed = result.scalar() is not None

    # Проверим, есть ли таблицы (например, activities)
    result = await db.execute(text(
        "SELECT to_regclass('public.activities')"
    ))
    activities_table_exists = result.scalar() is not None

    return {
        "ltree_installed": ltree_installed,
        "activities_table_exists": activities_table_exists
    }