from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt
from typing import List
from ..schemas import ActOrgSchema, ActOrgUpdateSchema, ActivitySchema, OrganizationSchema
from ..utils import verify_api_key
from ..deps import get_db

from ..crud.act_org_crud import (
    create_act_org,
    get_activities_by_org_id,
    get_organizations_by_act_id,
    delete_act_org,
    update_act_org
)

router = APIRouter(
    prefix="/act_org",
    tags=["Activities/Organizations"],
)

@router.post("/organizations/{org_id}/activities/{activity_id}", response_model=ActOrgSchema, status_code=status.HTTP_201_CREATED)
async def create_act_org_endpoint(
    data: ActOrgSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для создания связи между организацией и видом деятальности.
    """
    return await create_act_org(data=data, db=db)

@router.get("/activities/{organization_id}", response_model=List[ActivitySchema], status_code=status.HTTP_200_OK)
async def get_activities_by_org_id_endpoint(
    organization_id: PositiveInt,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для получения видов деятельности организации.
    """
    return await get_activities_by_org_id(organization_id=organization_id, db=db)

@router.get("/organizations/{activity_id}", response_model=List[str], status_code=status.HTTP_200_OK)
async def get_organizations_by_act_id_endpoint(
    activity_id: PositiveInt,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для получения организаций с указанным видом деятельности.
    """
    return await get_organizations_by_act_id(activity_id=activity_id, db=db)