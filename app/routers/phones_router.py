from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import PhoneSchema
from ..crud.phones_crud import create_phone
from ..utils import verify_api_key
from ..deps import get_db

router = APIRouter()

@router.post("/phones", response_model=PhoneSchema)
async def create_phone_endpoint(phone: PhoneSchema, 
                    x_api_key: str = Header(...), 
                    session: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для добавления нового телефона.
    """
    verify_api_key(x_api_key)

    return await create_phone(session, phone)