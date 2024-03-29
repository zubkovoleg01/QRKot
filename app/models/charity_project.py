# app/models/charity_project.py
from sqlalchemy import Column, String, Text

from app.models.base import BaseAbstractModel


class CharityProject(BaseAbstractModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)