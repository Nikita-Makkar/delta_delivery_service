from typing import Any, Generic, Protocol, TypeVar

from delivery_service.application.interfaces.unit_of_work import IUnitOfWork

T = TypeVar("T")


class IRepository(Protocol, Generic[T]):
    """
    Generic async repository interface for basic operations.
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        """
        Initializes repository with unit of work.
        """
        ...

    async def add(self, entity: T) -> T | None:
        """
        Adds an entity to the storage.
        """
        ...

    async def get_by_id(self, id: int) -> T | None:
        """
        Returns entity by ID or None.
        """
        ...

    async def find_all(self, **filter_by: Any) -> list[T]:
        """
        Returns list of entities matching filters.
        """
        ...
