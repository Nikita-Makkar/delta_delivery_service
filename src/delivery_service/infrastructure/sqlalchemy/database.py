from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from delivery_service.infrastructure.config import settings

"""
SQLAlchemy engine and session setup.
"""

engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    """
    Base class for models
    """
