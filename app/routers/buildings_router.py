from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas import BuildingSchema, BuildingBaseSchema, BuildingUpdateSchema
from ..utils import verify_api_key
from ..deps import get_db

from ..crud.buildings_crud import (
    create_building,
    get_building,
    get_buildings_list,
    delete_building,
    update_building
)

router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
)

@router.post("/", response_model=BuildingSchema, status_code=status.HTTP_201_CREATED)
async def create_building_endpoint(
    building_data: BuildingBaseSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для создания нового здания.
    """
    return await create_building(building_data=building_data, db=db)

@router.get("/{building_id}", response_model=BuildingSchema, status_code=status.HTTP_200_OK)
async def get_building_endpoint(
    building_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для получения здания по id.
    """
    return await get_building(building_id=building_id, db=db)

@router.get("/", response_model=List[BuildingSchema], status_code=status.HTTP_200_OK)
async def get_buildings_list_endpoint(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для получения всех зданий.
    """
    return await get_buildings_list(db=db)

@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building_endpoint(
    building_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для удаления здания по id.
    """
    return await delete_building(building_id=building_id, db=db)

@router.put("/{building_id}", response_model=BuildingSchema, status_code=status.HTTP_200_OK)
async def update_building_endpoint(
    building_id: int,
    update_data: BuildingUpdateSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для обновления здания по id.
    """
    return await update_building(building_id=building_id, update_data=update_data, db=db)