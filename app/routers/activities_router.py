from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas import ActivitySchema, ActivityBaseSchema, ActivityUpdateSchema, ActivityTreeSchema
from ..utils import verify_api_key
from ..deps import get_db

from ..crud.activities_crud import (
    create_activity,
    get_activity,
    get_activities_list,
    get_activity_tree,
    delete_activity,
    update_activity
)

router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
)

@router.post("/", response_model=ActivitySchema, status_code=status.HTTP_201_CREATED)
async def create_activity_endpoint(
    activity_data: ActivityBaseSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для создания нового вида деятальности.
    """
    return await create_activity(activity_data=activity_data, db=db)

@router.get("/{activity_id}", response_model=ActivitySchema, status_code=status.HTTP_200_OK)
async def get_activity_endpoint(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для получения вида деятальности по id.
    """
    return await get_activity(activity_id=activity_id, db=db)

@router.get("/{activity_id}/tree", response_model=ActivityTreeSchema, status_code=status.HTTP_200_OK)
async def get_activity_tree_endpoint(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для получения вида деятельности со вложенной структурой по id.
    """
    return await get_activity_tree(activity_id=activity_id, db=db)

@router.get("/", response_model=List[ActivityTreeSchema], status_code=status.HTTP_200_OK)
async def get_activities_list_endpoint(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для получения всех видов деятельности со вложенной структурой.
    """
    return await get_activities_list(db=db)

@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity_endpoint(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для удаления вида деятальности по id.
    """
    return await delete_activity(activity_id=activity_id, db=db)

@router.put("/{activity_id}", response_model=ActivitySchema, status_code=status.HTTP_200_OK)
async def update_activity_endpoint(
    activity_id: int,
    update_data: ActivityUpdateSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для обновления вида деятальности по id.
    """
    return await update_activity(activity_id=activity_id, update_data=update_data, db=db)