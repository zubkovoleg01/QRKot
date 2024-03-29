# app/api/endpoints/donation.py

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationAdminDB
)
from app.services.invest import investing

router = APIRouter()

async def get_session() -> AsyncSession:
    async with get_async_session() as session:
        yield session

async def process_donation(donation: DonationCreate, user: User, session: AsyncSession) -> DonationDB:
    donation_instance = await donation_crud.create(donation, session, user)
    investing_objects = await investing(donation_instance, session)
    session.add(donation_instance)
    if investing_objects:
        session.add_all(investing_objects)
    await session.commit()
    await session.refresh(donation_instance)
    return donation_instance

@router.get('/', response_model=List[DonationAdminDB], response_model_exclude_none=True, dependencies=[Depends(current_superuser)])
async def get_all_donations(session: AsyncSession = Depends(get_session)):
    return await donation_crud.get_multi(session)

@router.post('/', response_model=DonationDB, response_model_exclude_none=True, dependencies=[Depends(current_user)])
async def create_new_donation(donation: DonationCreate, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    return await process_donation(donation, user, session)

@router.get('/my', response_model=List[DonationDB], response_model_exclude_none=True, dependencies=[Depends(current_user)])
async def get_user_donations(session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    return await donation_crud.get_by_user(session, user.id)


