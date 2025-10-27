from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Building
from app.schemas import BuildingBaseSchema, BuildingSchema, BuildingUpdateSchema

async def create_building(building_data: BuildingBaseSchema, db: AsyncSession) -> BuildingSchema:
    """
    Создает новое здание.
    """
    db_building = Building(
        country=building_data.country,
        city=building_data.city,
        street=building_data.street,
        house_number=building_data.house_number,
        latitude=building_data.latitude,
        longitude=building_data.longitude
    )

    db.add(db_building)
    await db.commit()
    await db.refresh(db_building)

    return BuildingSchema.model_validate(db_building)

async def get_building(building_id: int, db: AsyncSession) -> BuildingSchema:
    """
    Получает здание по его id.
    Если здание не найдено, возвращает HTTP 404.
    """
    result = await db.execute(
    select(Building).where(Building.id == building_id))
    db_building = result.scalar_one_or_none()

    if db_building is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Building with id {building_id} not found."
        )

    return BuildingSchema.model_validate(db_building)

async def get_buildings_list(db: AsyncSession) -> list[BuildingSchema]:
    """
    Получает список всех зданий.
    """
    result = await db.execute(select(Building))

    buildings = result.scalars().all()

    return [BuildingSchema.model_validate(building) for building in buildings]

async def delete_building(building_id: int, db: AsyncSession) -> BuildingSchema:
    result = await db.execute(select(Building).where(Building.id == building_id))
    db_building = result.scalar_one_or_none()

    if db_building is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Building with id {building_id} not found."
        )
    
    await db.delete(db_building)
    await db.commit()

    return {"detail": f"Building with id {building_id} deleted successfully."}

async def update_building(
    building_id: int,
    update_data: BuildingUpdateSchema,
    db: AsyncSession
) -> BuildingSchema:
    """
    Обновляет здание по id.
    Если здание не найдено — 404.
    Обновляет только переданные поля.
    """
    result = await db.execute(select(Building).where(Building.id == building_id))
    db_building = result.scalar_one_or_none()

    if db_building is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Building with id {building_id} not found."
        )

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_building, field, value)

    db.add(db_building)
    await db.commit()
    await db.refresh(db_building)

    return BuildingSchema.model_validate(db_building)