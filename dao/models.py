from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, ForeignKey
from dao.database import Base

class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger,unique=True,nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"

class Tariff(Base):
    __tablename__='tariffs'

    title: Mapped[str]
    description: Mapped[str]
    cost: Mapped[int]
