from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from delivery_service.application.exceptions import (
    DatabaseOperationException, SessionNotProvidedException)
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork

from .database import async_session_maker


class SQLAlchemyUnitOfWork(IUnitOfWork):
    """
    SQLAlchemy implementation of unit of work pattern.
    """

    def __init__(self) -> None:
        if not async_session_maker:
            raise SessionNotProvidedException("Session is not initialized")
        self._sessionmaker = async_session_maker
        self._session: AsyncSession | None = None

    @property
    def session(self) -> AsyncSession | None:
        """
        Returns current database session.
        """
        return self._session

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        """
        Opens new session context.
        """
        self._session = self._sessionmaker()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Commits or rolls back session on exit.
        """
        try:
            if exc_type is None:
                await self.commit()
            else:
                raise Exception
        except Exception:
            await self.rollback()
            raise DatabaseOperationException(
                f"Error the database operation: {exc_val}"
            )
        finally:
            if self._session:
                await self._session.close()
            else:
                raise SessionNotProvidedException("Session is not initialized")

    async def commit(self) -> None:
        """
        Commits session changes.
        """
        if self._session:
            await self._session.commit()
        else:
            raise SessionNotProvidedException("Session is not initialized")

    async def rollback(self) -> None:
        """
        Rolls back session changes.
        """
        if self._session:
            await self._session.rollback()
        else:
            raise SessionNotProvidedException("Session is not initialized")
