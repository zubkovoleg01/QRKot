# app/crud/charity_project.py
from typing import Optional, List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """
    CRUD операции для благотворительных проектов.
    """

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """
        Получить ID проекта по его имени.
        """
        query = select(CharityProject.id).where(CharityProject.name == project_name)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_closed_projects(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:
        """
        Получить закрытые проекты, отсортированные по времени закрытия.
        """
        query = select(CharityProject).where(CharityProject.fully_invested)\
            .order_by(func.julianday(CharityProject.close_date) - func.julianday(CharityProject.create_date))
        result = await session.execute(query)
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
