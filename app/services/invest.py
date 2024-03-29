# app/services/invest.py
from typing import Union
from datetime import datetime
from app.models import CharityProject, Donation
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from sqlalchemy.ext.asyncio import AsyncSession


async def investing(
        new_object: Union[CharityProject, Donation],
        session: AsyncSession
) -> Union[CharityProject, Donation]:

    all_changed_objects = []

    if new_object.invested_amount is None:
        new_object.invested_amount = 0

    crud_model = donation_crud if isinstance(new_object, CharityProject) else charity_project_crud

    projects_to_invest = await crud_model.get_not_fully_invested(session)

    for project in projects_to_invest:
        free_amount = min(
            (project.full_amount - project.invested_amount),
            (new_object.full_amount - new_object.invested_amount)
        )

        project.invested_amount += free_amount
        new_object.invested_amount += free_amount

        if new_object.invested_amount == new_object.full_amount:
            new_object.fully_invested = True
            new_object.close_date = datetime.utcnow()

        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()

        all_changed_objects.append(project)

        if new_object.fully_invested:
            break

    return all_changed_objects
