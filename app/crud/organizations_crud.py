from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import Organization, Building
from app.schemas import OrganizationBaseSchema, OrganizationSchema, OrganizationUpdateSchema

async def create_organization(organization_data: OrganizationBaseSchema, db: AsyncSession) -> OrganizationSchema:
    """
    Создает новую организацию.
    Если указан building_id, проверяет, что такое здание существует.
    """
    if organization_data.building_id is not None:
        result = await db.execute(select(Building).where(Building.id == organization_data.building_id))
        building = result.scalar_one_or_none()
        if building is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Building with id {organization_data.building_id} does not exist."
            )

    db_organization = Organization(
        name=organization_data.name,
        building_id=organization_data.building_id
    )

    db.add(db_organization)
    await db.commit()
    await db.refresh(
        db_organization,
        attribute_names=['phones', 'activities']
    )

    return OrganizationSchema.model_validate(db_organization)

async def get_organization(organization_id: int, db: AsyncSession) -> OrganizationSchema:
    """
    Получает организацию по ее id.
    Если организация не найдена, возвращает HTTP 404.
    """
    result = await db.execute(
    select(Organization)
    .options(
        selectinload(Organization.phones),
        selectinload(Organization.activities),
        selectinload(Organization.building)
    )
    .where(Organization.id == organization_id)
    )
    db_organization = result.scalar_one_or_none()

    if db_organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {organization_id} not found."
        )

    return OrganizationSchema.model_validate(db_organization)

async def get_organization_list(db: AsyncSession) -> list[OrganizationSchema]:
    """
    Получает список всех организаций.
    """
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
            selectinload(Organization.building)
        )
    )

    organizations = result.scalars().all()

    return [OrganizationSchema.model_validate(org) for org in organizations]

async def delete_organization(organization_id: int, db: AsyncSession):
    """
    Удаляет организацию по ее id.
    Если организация не найдена, возвращает HTTP 404.
    """
    result = await db.execute(select(Organization).where(Organization.id == organization_id))
    db_organization = result.scalar_one_or_none()

    if db_organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {organization_id} not found."
        )

    await db.delete(db_organization)
    await db.commit()

    return {"detail": f"Organization with id {organization_id} deleted successfully."}

async def update_organization(
    organization_id: int,
    update_data: OrganizationUpdateSchema,
    db: AsyncSession
) -> OrganizationSchema:
    """
    Обновляет организацию по id.
    Если организация не найдена, возвращает 404.
    """
    result = await db.execute(select(Organization).where(Organization.id == organization_id))
    db_organization = result.scalar_one_or_none()

    if db_organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {organization_id} not found."
        )

    if update_data.building_id is not None:
        result = await db.execute(select(Building).where(Building.id == update_data.building_id))
        building = result.scalar_one_or_none()
        if building is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Building with id {update_data.building_id} does not exist."
            )

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_organization, field, value)

    db.add(db_organization)
    await db.commit()
    await db.refresh(
        db_organization,
        attribute_names=['phones', 'activities']
    )

    return OrganizationSchema.model_validate(db_organization)