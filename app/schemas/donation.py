# app/schemas/donation.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    """
    Базовая схема для пожертвований.
    """
    full_amount: PositiveInt = Field(..., example=100, description="Полная сумма пожертвования")
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    """
    Схема для создания пожертвования.
    """
    pass


class DonationDB(DonationBase):
    """
    Схема для представления пожертвования в базе данных.
    """
    id: int
    create_date: datetime

    class Config:
        form_attributes = True


class DonationAdminDB(DonationDB):
    """
    Схема для представления пожертвования в административной панели.
    """
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
