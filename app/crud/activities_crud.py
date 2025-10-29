from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models import Activity
from app.schemas import ActivityBaseSchema, ActivitySchema, ActivityUpdateSchema, ActivityTreeSchema
from app.utils import get_path, build_activity_tree

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

async def get_activities_list(db: AsyncSession):
    """
    Возвращает все виды деятельности в виде древовидной структуры.
    """
    result = await db.execute(select(Activity))
    all_activities = result.scalars().all()

    if all_activities is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activities not found."
        )

    trees = []
    for activity in all_activities:
        tree = await get_activity_tree(activity_id=activity.id, db=db)
        trees.append(tree)

    return trees

async def get_activity_tree(activity_id: int, db: AsyncSession) -> ActivityTreeSchema:
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

async def delete_activity(activity_id: int, db: AsyncSession):
    """
    Удаляет вид деятельности и все его дочерние виды.
    """
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    db_activity = result.scalar_one_or_none()

    if db_activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with id {activity_id} not found."
        )
    
    path_pattern = f"{db_activity.path}%"

    await db.execute(delete(Activity).where(Activity.path.like(path_pattern)))
    await db.commit()

    return {"detail": f"Activity '{db_activity.name}' and its descendants have been deleted."}

async def update_activity() -> ActivitySchema:
    ...
    return

"""При обновлении path у вида деятельности необходимо менять пути у всех его дочерних элементов"""

# async def update_activity(
#     activity_id: int,
#     update_data: ActivityUpdateSchema,
#     db: AsyncSession
# ) -> ActivitySchema:
#     """
#     Обновляет вид деятельности по id.
#     Если вид деятельности не найден — 404.
#     Обновляет только переданные поля.
#     """
#     result = await db.execute(select(Activity).where(Activity.id == activity_id))
#     db_activity = result.scalar_one_or_none()

#     if db_activity is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Activity with id {activity_id} not found."
#         )
    
#     update_data.name = db_activity.name
    
#     update_data = ActivityBaseSchema(
#         name=db_activity.name,
#         path=await get_path(update_data, db)
#     )

#     for field, value in update_data.model_dump(exclude_unset=True).items():
#         setattr(db_activity, field, value)

#     db.add(db_activity)
#     await db.commit()
#     await db.refresh(db_activity)

#     return ActivitySchema.model_validate(db_activity)
