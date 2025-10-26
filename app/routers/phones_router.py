from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas import PhoneSchema, PhoneBaseSchema, PhoneUpdateSchema
from ..utils import verify_api_key
from ..deps import get_db

from ..crud.phones_crud import (
    get_phones_list,
    get_phone,
    create_phone,
    update_phone,
    delete_phone,
)

router = APIRouter(
    prefix="/phones",
    tags=["Phones"],
)

@router.post("/", response_model=PhoneSchema, status_code=status.HTTP_201_CREATED)
async def create_phone_endpoint(
    phone_data: PhoneBaseSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для создания нового телефона.
    """
    return await create_phone(phone_data=phone_data, db=db)

@router.get("/{phone_id}", response_model=PhoneSchema, status_code=status.HTTP_200_OK)
async def get_phone_endpoint(
    phone_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    """
    Эндпоинт для получения организации по id.
    """
    return await get_phone(phone_id=phone_id, db=db)

@router.get("/", response_model=List[PhoneSchema], status_code=status.HTTP_200_OK)
async def get_phones_list_endpoint(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для получения всех телефонов.
    """
    return await get_phones_list(db=db)

@router.delete("/{phone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_phone_endpoint(
    phone_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для удаления телефона по id.
    """
    return await delete_phone(phone_id=phone_id, db=db)

@router.put("/{phone_id}", response_model=PhoneSchema, status_code=status.HTTP_200_OK)
async def update_phone_endpoint(
    phone_id: int,
    update_data: PhoneUpdateSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для обновления телефона по id.
    """
    return await update_phone(phone_id=phone_id, update_data=update_data, db=db)