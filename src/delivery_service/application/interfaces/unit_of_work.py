from types import TracebackType
from typing import Protocol


class IUnitOfWork(Protocol):
    """
    Interface for managing transactions.
    """

    async def __aenter__(self) -> "IUnitOfWork":
        """
        Begins a unit of work context.
        """
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Ends the unit of work, commits or rolls back on error.
        """
        ...

    async def commit(self) -> None:
        """
        Commits all changes.
        """
        ...

    async def rollback(self) -> None:
        """
        Rolls back all changes.
        """
        ...
