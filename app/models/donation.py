# app/models/donation.py
from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseAbstractModel


class Donation(BaseAbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)