from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import PositiveInt
from typing import List
from ..schemas import OrganizationSchema
from ..models import Building, Organization
from ..utils import organizations_to_list

async def get_organizations_by_building_id(building_id: int, db: AsyncSession) -> List:
    """
    Получает список организаций в указанном здании.
    """
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()
    if building is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Building with id {building_id} does not exist."
        )
    
    result = await db.execute(
        select(Organization)
        .where(Organization.building_id == building_id)
    )
    organizations = result.scalars().all()

    if not organizations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No organizations found for building_id {building_id}."
        )
    
    organizations_list = await organizations_to_list(organizations)

    return organizations_list