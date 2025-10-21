from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.settings import DB_URL
from typing import AsyncGenerator

engine = create_async_engine(DB_URL, echo=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Возвращает сессию БД.
    """
    async with AsyncSessionLocal() as session:
        yield session
