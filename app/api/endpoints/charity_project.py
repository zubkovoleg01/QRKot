# app/api/endpoints/charity_project.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount, check_fully_invested,
    check_invested_amount_exists, check_name_duplicate,
    check_project_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.invest import investing

router = APIRouter()

# Получение сессии
async def get_session() -> AsyncSession:
    async with get_async_session() as session:
        yield session

# Проверка проекта
async def check_project(project_id: int, session: AsyncSession = Depends(get_session)) -> CharityProjectDB:
    project = await get_project(project_id, session)
    await check_fully_invested(project.fully_invested)
    return project

# Получение проекта по id
async def get_project(project_id: int, session: AsyncSession = Depends(get_session)) -> CharityProjectDB:
    return await check_project_exists(project_id, session)


# Создание новго проекта
@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_session),
):
    await check_name_duplicate(charity_project.name, session)
    project = await charity_project_crud.create(charity_project, session)
    investing_objects = await investing(project, session)
    session.add(project)
    if investing_objects:
        session.add_all(investing_objects)
    await session.commit()
    await session.refresh(project)
    return project

# Получение всех проектов
@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_session),
):
    return await charity_project_crud.get_multi(session)

# Частичное обновление проекта
@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        project: CharityProjectDB = Depends(get_project),
        session: AsyncSession = Depends(get_session),
):
    """Только для суперюзеров."""
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount(project.invested_amount, obj_in.full_amount)
    project = await charity_project_crud.update(project, obj_in, session)
    return project

# Удаление проекта
@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project: CharityProjectDB = Depends(check_project),
        session: AsyncSession = Depends(get_session),
):
    project = await charity_project_crud.remove(project, session)
    return project
