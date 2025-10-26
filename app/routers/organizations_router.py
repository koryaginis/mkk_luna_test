from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..schemas import OrganizationSchema, OrganizationBaseSchema, OrganizationUpdateSchema
from ..utils import verify_api_key
from ..deps import get_db
from ..models import Organization

from ..crud.organizations_crud import (
    get_organization_list,
    get_organization,
    create_organization,
    update_organization,
    delete_organization,
)

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)

@router.post("/", response_model=OrganizationSchema, status_code=status.HTTP_201_CREATED)
async def create_organization_endpoint(
    organization_data: OrganizationBaseSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для создания новой организации.
    """
    return await create_organization(organization_data=organization_data, db=db)

@router.get("/{organization_id}", response_model=OrganizationSchema, status_code=status.HTTP_200_OK)
async def get_organization_endpoint(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для получения организации по id.
    """
    return await get_organization(organization_id=organization_id, db=db)

@router.get("/", response_model=List[OrganizationSchema], status_code=status.HTTP_200_OK)
async def get_organization_list_endpoint(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для получения всех организаций.
    """
    return await get_organization_list(db=db)

@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization_endpoint(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для удаления организации по id.
    Возвращает 204 No Content при успешном удалении.
    """
    result = await db.execute(select(Organization).where(Organization.id == organization_id))
    db_organization = result.scalar_one_or_none()

    if db_organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {organization_id} not found."
        )

    await delete_organization(organization_id=organization_id, db=db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{organization_id}", response_model=OrganizationSchema, status_code=status.HTTP_200_OK)
async def update_organization_endpoint(
    organization_id: int,
    update_data: OrganizationUpdateSchema,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """
    Эндпоинт для обновления организации по id.
    """
    return await update_organization(
        organization_id=organization_id,
        update_data=update_data,
        db=db
    )