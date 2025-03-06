from datetime import datetime
from core.constants import database_url
from sqlalchemy import func, TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

# Создание асинхронного движка для подключения к БД
engine = create_async_engine(url=database_url)

# Создание фабрики сессий
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

# Базовый класс для моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Этот класс не будет создавать отдельную таблицу

    # Общее поле "id" для всех таблиц
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Поля времени создания и обновления записи
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    # Автоматическое определение имени таблицы
    @classmethod
    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'