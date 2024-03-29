# app/schemas/charity_project.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """
    Базовая схема для благотворительных проектов.
    """
    name: str = Field(..., max_length=100, description="Название проекта")
    description: str = Field(..., description="Описание проекта")
    full_amount: PositiveInt = Field(..., example=100, description="Полная сумма для проекта")

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """
    Схема для создания благотворительного проекта.
    """
    pass


class CharityProjectUpdate(CharityProjectBase):
    """
    Схема для обновления благотворительного проекта.
    """
    name: Optional[str] = Field(max_length=100, description="Новое название проекта")
    description: Optional[str] = Field(description="Новое описание проекта")
    full_amount: Optional[PositiveInt] = Field(example=100, description="Новая сумма проекта")

    @validator('name')
    def name_cannot_be_null(cls, value):
        """
        Проверка, что имя проекта не пустое.
        """
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    """
    Схема для представления благотворительного проекта в базе данных.
    """
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        from_attributes = True
