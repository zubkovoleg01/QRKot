# app/models/base.py
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class BaseAbstractModel(Base):

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)