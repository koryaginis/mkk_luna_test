from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Phone, Organization
from app.schemas import PhoneBaseSchema, PhoneSchema, PhoneUpdateSchema

async def create_phone(phone_data: PhoneBaseSchema, db: AsyncSession) -> PhoneSchema:
    """
    Создает новый телефон.
    """
    if phone_data.organization_id is not None:
        result = await db.execute(select(Organization).where(Organization.id == phone_data.organization_id))
        organization = result.scalar_one_or_none()
        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization with id {phone_data.organization_id} does not exist."
            )
    
    db_phone = Phone(
        number=phone_data.number,
        organization_id=phone_data.organization_id
    )

    db.add(db_phone)
    await db.commit()
    await db.refresh(db_phone)

    return PhoneSchema.model_validate(db_phone)

async def get_phone(phone_id: int, db: AsyncSession) -> PhoneSchema:
    """
    Получает телефон по его id.
    Если телефон не найден, возвращает HTTP 404.
    """
    result = await db.execute(
    select(Phone).where(Phone.id == phone_id))
    db_phone = result.scalar_one_or_none()

    if db_phone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Phone with id {phone_id} not found."
        )

    return PhoneSchema.model_validate(db_phone)

async def get_phones_list(db: AsyncSession) -> list[PhoneSchema]:
    """
    Получает список всех телефонов.
    """
    result = await db.execute(select(Phone))

    phones = result.scalars().all()

    return [PhoneSchema.model_validate(phone) for phone in phones]

async def delete_phone(phone_id: int, db: AsyncSession) -> PhoneSchema:
    result = await db.execute(select(Phone).where(Phone.id == phone_id))
    db_phone = result.scalar_one_or_none()

    if db_phone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Phone with id {phone_id} not found."
        )
    
    await db.delete(db_phone)
    await db.commit()

    return {"detail": f"Phone with id {phone_id} deleted successfully."}

async def update_phone(
    phone_id: int,
    update_data: PhoneUpdateSchema,
    db: AsyncSession
) -> PhoneSchema:
    """
    Обновляет телефон по id.
    Если телефон не найден — 404.
    Обновляет только переданные поля.
    """
    result = await db.execute(select(Phone).where(Phone.id == phone_id))
    db_phone = result.scalar_one_or_none()

    if db_phone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Phone with id {phone_id} not found."
        )

    if update_data.organization_id is not None:
        result = await db.execute(select(Organization).where(Organization.id == update_data.organization_id))
        organization = result.scalar_one_or_none()
        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization with id {update_data.organization_id} does not exist."
            )

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_phone, field, value)

    db.add(db_phone)
    await db.commit()
    await db.refresh(db_phone)

    return PhoneSchema.model_validate(db_phone)

