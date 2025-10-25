from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Phone

async def create_phone(session: AsyncSession, phone):
    """
    Сохраняет новый телефон в БД.
    """
    db_phone = Phone(id=phone.id, number=str(phone.number), organization_id=phone.organization_id)
    session.add(db_phone)
    await session.commit()
    await session.refresh(db_phone)
    return db_phone

async def get_phone_by_id(session: AsyncSession, phone_id: int):
    """
    Возвращает телефон по его id.
    """
    return await session.get(Phone, phone_id)
