#app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    if await charity_project_crud.get_project_id_by_name(project_name, session):
        raise HTTPException(
            status_code=400,
            detail='Проект с таким названием уже существует!',
        )

async def check_invested_amount_exists(
        invested_amount: int,
) -> None:
    if invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='Удаление невозможно!',
        )

async def check_fully_invested(
        fully_invested: bool,
) -> None:
    if fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Редактирование закрытого проекта невозможно!',
        )

async def check_full_amount(
        project_invested_amount: int,
        new_full_amount: int,
) -> None:
    if new_full_amount < project_invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Сумма меньше собранной!',
        )

async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Данный проект не найден!',
        )
    return project