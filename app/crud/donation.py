# app/crud/donation.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    """
    CRUD операции для пожертвований.
    """

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id: int
    ):
        """
        Получить пожертвования пользователя по его ID.
        """
        query = select(Donation).where(Donation.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
