from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt
from typing import List
from ..schemas import OrganizationSchema
from ..utils import verify_api_key
from ..deps import get_db
from ..crud.act_org_crud import get_organizations_by_act_id
from ..logic.main_logic import get_organizations_by_building_id
from ..crud.organizations_crud import (get_organization_by_id, 
                                       get_organization_by_name, 
                                       get_organizations_in_rectangle)

router = APIRouter(
    prefix="/main_logic",
    tags=["Главный функционал"],
)

@router.get("/organizations_by_building_id/{building_id}", response_model=List[str], status_code=status.HTTP_200_OK)
async def get_organizations_by_building_id_endpoint(
    building_id: PositiveInt,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для получения списка организаций в указанном здании.
    """
    return await get_organizations_by_building_id(building_id=building_id, db=db)

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

@router.get("/org_by_id/{organization_id}", response_model=OrganizationSchema, status_code=status.HTTP_200_OK)
async def get_organization_by_id_endpoint(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для получения организации по id.
    """
    return await get_organization_by_id(organization_id=organization_id, db=db)

@router.get("/org_by_name/{organization_name}", response_model=OrganizationSchema, status_code=status.HTTP_200_OK)
async def get_organization_by_name_endpoint(
    organization_name: str,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для получения организации по его имени.
    """
    return await get_organization_by_name(organization_name=organization_name, db=db)

@router.get("/orgs_in_rectangle", response_model=List[str], status_code=status.HTTP_200_OK)
async def get_organizations_in_rectangle_endpoint(
    lat_min: float,
    lon_min: float,
    lat_max: float,
    lon_max: float,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для получения организаций, находящихся в прямоугольной области.
    Адреса и координаты зданий из тестовой БД совпадают с реальными зданиями Томска,
    поэтому можно использовать реальные координаты для тестирования.
        Параметры:
        - lat_min, lon_min — юго-западная точка
        - lat_max, lon_max — северо-восточная точка
    """
    return await get_organizations_in_rectangle(
        lat_min=lat_min,
        lon_min=lon_min,
        lat_max=lat_max,
        lon_max=lon_max,
        db=db
    )