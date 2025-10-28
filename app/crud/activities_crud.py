from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from app.models import Activity
from app.schemas import ActivityBaseSchema, ActivitySchema, ActivityUpdateSchema
from app.utils import transliterate, get_path, build_activity_tree

MAX_ACTIVITY_DEPTH = 3  # Максимальный 3 уровня вложенности

async def create_activity(activity_data: ActivityBaseSchema, db: AsyncSession) -> ActivitySchema:
    """
    Создает новый вид деятельности.
    """
    path = await get_path(activity_data, db)

    db_activity = Activity(
        name=activity_data.name,
        path=path
    )

    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)

    return ActivitySchema.model_validate(db_activity)

async def get_activity(activity_id: int, db: AsyncSession) -> ActivitySchema:
    """
    Получает вид деятельности по его id.
    Если вид деятельности не найден, возвращает HTTP 404.
    """
    result = await db.execute(
    select(Activity).where(Activity.id == activity_id))
    db_activity = result.scalar_one_or_none()

    if db_activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with id {activity_id} not found."
        )

    return ActivitySchema.model_validate(db_activity)

async def get_activities_list(activity_id: int, db: AsyncSession) -> ActivitySchema:
    """
    Получает все виды деятельности вместе со вложенной структурой.
    """
    result = await db.execute(
    select(Activity).where(Activity.id == activity_id))
    db_activity = result.scalar_one_or_none()

    if db_activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with id {activity_id} not found."
        )
    
    descendants_result = await db.execute(
    select(Activity).where(Activity.path.like(f"{db_activity.path}%")))
    descendants = descendants_result.scalars().all()

    activity_tree = await build_activity_tree(descendants, root_path="")

    return activity_tree

async def delete_activity() -> ActivitySchema:
    ...
    return

async def update_activity() -> ActivitySchema:
    ...
    return

async def get_activity_tree(activity_id: int, db: AsyncSession) -> ActivitySchema:
    """
    Получает вид деятельности по его id вместе со вложенной структурой.
    """
    result = await db.execute(
    select(Activity).where(Activity.id == activity_id))
    db_activity = result.scalar_one_or_none()

    if db_activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with id {activity_id} not found."
        )
    
    descendants_result = await db.execute(
    select(Activity).where(Activity.path.like(f"{db_activity.path}%")))
    descendants = descendants_result.scalars().all()

    activity_tree = await build_activity_tree(descendants, root_path=db_activity.path)

    return activity_tree