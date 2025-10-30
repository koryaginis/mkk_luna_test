from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import PositiveInt
from typing import List
from ..schemas import ActOrgSchema, ActivitySchema, OrganizationSchema
from ..models import Organization, Activity, organizations_activities
from ..utils import organizations_to_list

async def create_act_org(data: ActOrgSchema, db: AsyncSession) -> ActOrgSchema:
    """
    Создает новую связь между видом деятельности и организацией.
    """
    result = await db.execute(select(Organization).where(Organization.id == data.organization_id))
    organization = result.scalar_one_or_none()
    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Organization with id {data.organization_id} does not exist."
        )

    result = await db.execute(select(Activity).where(Activity.id == data.activity_id))
    activity = result.scalar_one_or_none()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Activity with id {data.activity_id} does not exist."
        )

    await db.execute(
        organizations_activities.insert().values(
            organization_id=data.organization_id,
            activity_id=data.activity_id
        )
    )
    await db.commit()

    return ActOrgSchema(organization_id=organization.id, activity_id=activity.id)

async def get_activities_by_org_id(organization_id: int, db: AsyncSession) -> List[ActivitySchema]:
    """
    Получает виды деятельности организации.
    """
    result = await db.execute(select(Organization).where(Organization.id == organization_id))
    organization = result.scalar_one_or_none()
    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Organization with id {organization_id} does not exist."
        )
    
    result = await db.execute(
        select(Activity)
        .join(organizations_activities, Activity.id == organizations_activities.c.activity_id)
        .where(organizations_activities.c.organization_id == organization_id)
    )
    activities = result.scalars().all()

    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No activities found for organization id {organization_id}."
        )

    return [ActivitySchema(id=activity.id, name=activity.name, parent_id=None) for activity in activities]

async def get_organizations_by_act_id(activity_id: int, db: AsyncSession) -> List:
    """
    Получает организации по указанному виду деятельности.
    Если указан родительский вид деятельности, возвращает организации всех дочерних активностей.
    """
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Activity with id {activity_id} does not exist."
        )

    pattern = f"{activity.path}%"
    result = await db.execute(
        select(Activity.id).where(Activity.path.like(pattern))
    )
    activity_ids = [row[0] for row in result.all()]

    result = await db.execute(
        select(Organization)
        .join(organizations_activities, Organization.id == organizations_activities.c.organization_id)
        .where(organizations_activities.c.activity_id.in_(activity_ids))
        .distinct()
    )
    organizations = result.scalars().all()

    if not organizations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No organizations found for activity id {activity_id}."
        )
    
    organizations_list = await organizations_to_list(organizations)

    return organizations_list

async def get_act_org():
    ...
    return

async def delete_act_org():
    ...
    return

async def update_act_org():
    ...
    return